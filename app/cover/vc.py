from pydub import AudioSegment
from audio_separator.separator import Separator
from TTS.api import TTS
import os

class VoiceCover():
    def __init__(self):
        self.source_file = None
        self.instrumental_file = None
        self.output_file = None
        self.vocal_files = []
        self.cover_files = []

        self.__instrumental_separator = None
        self.__tts = None
    
    @staticmethod
    def get_filename(filepath):
        name = os.path.splitext(os.path.basename(filepath))[0]
        extension = os.path.splitext(filepath)[1][1:]
        return name, extension
    
    @staticmethod
    def get_audio(filepath, type):
        match type:
            case "mp3":
                return AudioSegment.from_mp3(filepath)
            case "wav":
                return AudioSegment.from_wav(filepath) 
        
        return None
    
    def load_from_source_file(self, filepath):
        if not os.path.isfile(filepath):
            raise Exception(f"Invalid file path: {filepath}")
        
        self.source_file = filepath
    
    def is_preprocessed(self):
        return len(self.vocal_files) > 0
    
    def is_covered(self):
        return len(self.cover_files) > 0
    
    def is_merged(self):
        return self.output_file is not None
    
    def reset(self):
        self.instrumental_file = None
        self.vocal_files = []
        self.reset_cover()
    
    def reset_cover(self):
        self.cover_files = []
        self.reset_merge()
    
    def reset_merge(self):
        self.output_file = None
    
    def preprocess(self, output_dir, max_split_size = 90):
        if self.source_file is None:
            raise Exception("Not loaded")

        if not os.path.isdir(output_dir):
            raise Exception(f"Invalid output directory: {output_dir}")
        
        if self.__instrumental_separator is None:
            self.__instrumental_separator = Separator()
            self.__instrumental_separator.load_model()
        
        self.reset()
       
        instrumental_output_file = os.path.join(output_dir, f"Instrumentals.wav")
        vocal_output_file = os.path.join(output_dir, f"Vocals.wav")

        output_files = self.__instrumental_separator.separate(self.source_file)
        os.rename(output_files[0], instrumental_output_file)
        os.rename(output_files[1], vocal_output_file)

        self.instrumental_file = instrumental_output_file
        vocal_audio = VoiceCover.get_audio(vocal_output_file, "wav")
        audio_len = vocal_audio.duration_seconds
        start = 0.0
        end = 0.0

        while start < audio_len:
            end = start + (max_split_size if start + max_split_size <= audio_len else audio_len - start)
            vocal_part_file = os.path.join(output_dir, f"Vocals_{start}.wav")

            vocal_part = vocal_audio[start * 1000:end * 1000]
            vocal_part.export(vocal_part_file, format="wav")
            self.vocal_files.append((vocal_part_file, start))

            start = end
    
    def merge(self, output_dir, vocal_bonus_db = 0):
        if not self.is_covered():
            raise Exception("Not covered")

        if not os.path.isdir(output_dir):
            raise Exception(f"Invalid output directory: {output_dir}")
        
        self.reset_merge()

        output_file = os.path.join(output_dir, f"Output.wav")
        output = self.get_audio(self.instrumental_file, "wav")
        output -= vocal_bonus_db

        for file, start_sec in self.cover_files:
            output = output.overlay(self.get_audio(file, "wav"), position=start_sec * 1000)

        output.export(output_file, format="wav")
        self.output_file = output_file
    
    def cover(self, voice_sample_file, output_dir):
        if not self.is_preprocessed():
            raise Exception("Not preprocessed")

        if not os.path.isdir(output_dir):
            raise Exception(f"Invalid output directory: {output_dir}")

        if not os.path.isfile(voice_sample_file) or VoiceCover.get_filename(voice_sample_file)[1] != "wav":
            raise Exception(f"Invalid sample file: {voice_sample_file}")

        if self.__tts is None:
            self.__tts = TTS(model_name="voice_conversion_models/multilingual/vctk/freevc24", progress_bar=True)
        
        self.reset_cover()

        for file, start_sec in self.vocal_files:
            cover_file = os.path.join(output_dir, f"Cover_{start_sec}.wav")
            self.__tts.voice_conversion_to_file(source_wav=file, target_wav=voice_sample_file, file_path=cover_file)
            self.cover_files.append((cover_file, start_sec))
