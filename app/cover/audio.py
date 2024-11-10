from pydub import AudioSegment
import os

class AudioFile():
    def __init__(self, audio_path):        
        self.path = audio_path
        self.audio = AudioFile.get_audio(self.path.fullpath, self.path.type)
        self.length = self.audio.duration_seconds
    
    @staticmethod
    def get_audio(filepath, type):
        match type:
            case "mp3":
                return AudioSegment.from_mp3(filepath)
            case "wav":
                return AudioSegment.from_wav(filepath) 
        
        return None

class AudioPath():
    def __init__(self, path):        
        self.fullpath = os.path.abspath(path)
        self.dirname = os.path.dirname(self.fullpath)
        self.basename = os.path.basename(self.fullpath)
        self.filename = os.path.splitext(self.basename)[0]
        self.type = os.path.splitext(self.basename)[1][1:]
        self.extension = '.' + self.type