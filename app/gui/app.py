from gui.gui import GUI

class VoiceCoverApp():
    def __init__(self):
        self.vc_data = None
        self.gui = GUI()
        self.gui.source_file_form.on_submit.add_listener(self.__preprocess__)
        self.gui.voice_sample_form.on_submit.add_listener(self.__cover__)
        self.gui.voice_sample_form.enable(False)
    
    def run(self):
        self.gui.show()

    def __preprocess__(self, *args):
        if self.gui.source_file_form.is_valid():
            print("PREPROCESS "+self.gui.source_file_form.value())
            self.gui.voice_sample_form.enable(True)

    def __cover__(self, *args):
        if self.gui.voice_sample_form.is_valid():
            print("COVER "+self.gui.voice_sample_form.value())