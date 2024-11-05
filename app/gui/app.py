from gui.gui import GUI
from cover.vc import VoiceCover

class VoiceCoverApp():
    def __init__(self):
        self.__vc = VoiceCover()
        self.__gui = GUI()
        self.__gui.source_file_form.on_submit.add_listener(self.__preprocess__)
        self.__gui.voice_sample_form.on_submit.add_listener(self.__cover__)
        self.__gui.voice_sample_form.enable(False)
    
    def run(self):
        self.__gui.show()

    def __preprocess__(self, *args):
        self.__gui.voice_sample_form.enable(False)

        if self.__gui.source_file_form.is_valid():
            audio_file = self.__gui.source_file_form.value()
            print("PREPROCESS "+audio_file)
            
            self.__vc.load_from_source_file(audio_file)
            self.__vc.preprocess(".tmp/")
            self.__gui.voice_sample_form.enable(True)

    def __cover__(self, *args):
        if self.__gui.voice_sample_form.is_valid():
            voice_sample = self.__gui.voice_sample_form.value()
            print("COVER "+voice_sample)

            self.__vc.cover(voice_sample, ".tmp/")
            self.__vc.merge(".tmp/", 6)