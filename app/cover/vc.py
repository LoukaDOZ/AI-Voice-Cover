from pydub import AudioSegment
from audio_separator.separator import Separator
from TTS.api import TTS
from math import ceil
from cover.progress import ProgressManager
from cover.audio import AudioFile, AudioPath
import os
import time

class VoiceCover():
    def __init__(self, output_dir = None, max_split_size = 90):
        if output_dir is not None:
            if not os.path.isdir(output_dir):
                raise Exception(f"Invalid output directory: {output_dir}")
        else:
            output_dir = os.getcwd()
        
        if max_split_size < 1:
            raise Exception(f"Invalid max split size: {max_split_size}")

        self.progress = ProgressManager()
        self.__max_split_size = max_split_size
        self.__instrumental_separator = None
        self.__tts = None

        self.__instrumentals_path = AudioPath(os.path.join(output_dir, "Instrumentals.wav"))
        self.__vocals_path = AudioPath(os.path.join(output_dir, "Vocals.wav"))
        self.__cover_path = AudioPath(os.path.join(output_dir, "Cover.wav"))
        self.__output_path = AudioPath(os.path.join(output_dir, "Output.wav"))
    
    @staticmethod
    def from_source_file(source_file):
        return VoiceCoverData(source_file)
    
    def reset_progress(self, data, preprocess = False, cover = False, merge = False):
        limit = 0
        split_count = ceil(AudioFile.get_audio(data.source_path.fullpath, data.source_path.type).duration_seconds / self.__max_split_size)

        if preprocess:
            limit += split_count + 3

        if cover:
            limit += split_count + 1

        if merge:
            limit += split_count + 3

        self.progress.reset(limit=limit)
    
    def preprocess(self, data):
        data.reset_for_preprocess()
        self.progress.set_label("Loading separator model")
        
        if self.__instrumental_separator is None:
            self.__instrumental_separator = Separator(log_level=0)
            self.__instrumental_separator.load_model()

        self.progress.step(label=f"Separating instrumentals and vocals")

        output_files = self.__instrumental_separator.separate(data.source_path.fullpath)
        os.rename(output_files[0], self.__instrumentals_path.fullpath)
        os.rename(output_files[1], self.__vocals_path.fullpath)
        data.instrumentals = self.__instrumentals_path.fullpath
        data.vocals = self.__vocals_path.fullpath

        self.progress.step(label=f"Loading vocals")

        audio = AudioFile(AudioPath(data.vocals))
        count = ceil(audio.length / self.__max_split_size)
        data.vocals_parts = []

        self.progress.step(label=f"Spliting vocals {int(float(1 / count) * 100.0)}% (1/{count})")

        for i in range(count):
            start = i * self.__max_split_size
            end = start + (self.__max_split_size if start + self.__max_split_size <= audio.length else audio.length - start)
            vocal_part_path = os.path.join(self.__vocals_path.dirname, f"{self.__vocals_path.filename}_{start}.{self.__vocals_path.type}")
            self.progress.set_label(label=f"Spliting vocals {int(float((i + 1) / count) * 100.0)}% ({i + 1}/{count})")

            vocal_part = audio.audio[start * 1000:end * 1000]
            vocal_part.export(vocal_part_path, format=audio.path.type)
            data.vocals_parts.append((vocal_part_path, start))

            start = end
            self.progress.step()
        
        data.is_preprocessed = True
    
    def cover(self, voice_sample, data):
        if not data.is_preprocessed:
            raise Exception("Not preprocessed")

        voice_sample = AudioPath(voice_sample)

        if voice_sample.type != "wav":
            raise Exception(f"Invalid sample file type: {voice_sample.fullpath}")

        data.reset_for_cover()
        self.progress.set_label("Loading voice conversion model")

        if self.__tts is None:
            self.__tts = TTS(model_name="voice_conversion_models/multilingual/vctk/freevc24", progress_bar=True)
        
        cover_parts = []
        count = len(data.vocals_parts)
        self.progress.step(label=f"Covering {int(float(1 / count) * 100.0)}% (1/{count})")

        for i, v in enumerate(data.vocals_parts):
            file, start_sec = v
            cover_file = os.path.join(self.__cover_path.dirname, f"{self.__cover_path.filename}_{start_sec}.{self.__cover_path.type}")
            self.progress.set_label(f"Covering {int(float((i + 1) / count) * 100.0)}% ({i + 1}/{count})")

            self.__tts.voice_conversion_to_file(source_wav=file, target_wav=voice_sample.fullpath, file_path=cover_file)
            cover_parts.append((cover_file, start_sec))
            self.progress.step()

        data.cover_parts = cover_parts
        data.is_covered = True
    
    def merge(self, data, output_extension="wav", vocal_bonus_db = 0):
        if not data.is_covered:
            raise Exception("Not covered")
        
        if output_extension not in ["wav"]:
            raise Exception(f"Invalid output extension: {output_extension}")

        count = len(data.cover_parts)
        self.progress.set_label(f"Merging {int(float(1 / count) * 100.0)}% (1/{count})")

        data.reset_for_merge()
        cover = AudioFile.get_audio(data.cover_parts[0][0], self.__cover_path.type)
        self.progress.step()

        for i in range(1, len(data.cover_parts)):
            file, start_sec = data.cover_parts[i]
            self.progress.set_label(f"Merging {int(float((i + 1) / count) * 100.0)}% ({i + 1}/{count})")

            cover = cover.append(AudioFile.get_audio(file, self.__cover_path.type))
            self.progress.step()
        
        self.progress.set_label(f"Exporting covered vocals")
        cover += vocal_bonus_db
        cover.export(self.__cover_path.fullpath, format=self.__cover_path.type)
        data.cover = self.__cover_path.fullpath
        self.progress.step(label=f"Merging instrumentals")

        output = cover.overlay(AudioFile.get_audio(data.instrumentals, self.__instrumentals_path.type))
        self.progress.step(label=f"Exporting output")

        output.export(self.__output_path.fullpath, format=output_extension)
        data.output = self.__output_path.fullpath
        data.is_merged = True
        self.progress.step()

class VoiceCoverData():
    def __init__(self, source_file):  
        if not os.path.isfile(source_file):
            raise Exception(f"Invalid path: {source_file}")
          
        self.source = source_file
        self.source_path = AudioPath(source_file)
        self.instrumentals = None
        self.vocals = None
        self.vocals_parts = None
        self.cover = None
        self.cover_parts = None
        self.output = None

        self.is_preprocessed = False
        self.is_covered = False
        self.is_merged = False
    
    def reset_for_preprocess(self):
        self.instrumentals = None
        self.vocals = None
        self.vocals_parts = None
        self.is_preprocessed = False
        self.reset_for_cover()
    
    def reset_for_cover(self):
        self.cover_parts = None
        self.is_covered = False
        self.reset_for_merge()
    
    def reset_for_merge(self):
        self.cover = None
        self.output = None
        self.is_merged = False