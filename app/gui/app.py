from gui.gui import GUI
from cover.vc import VoiceCover
from gui.thread import JoinNonBlockingThread

class VoiceCoverApp():
    def __init__(self):
        self.__vc = VoiceCover()
        self.__gui = GUI()
        self.__gui.source_file_form.on_submit.add_listener(self.__preprocess__)
        self.__gui.voice_sample_form.on_submit.add_listener(self.__cover__)
        self.__gui.voice_sample_form.enable(False)
        self.after = self.__gui.after_func
    
    def run(self):
        self.__gui.show()
    
    def __preprocess__(self, *args):
        self.__gui.voice_sample_form.enable(False)

        if self.__gui.source_file_form.is_valid():
            audio_file = self.__gui.source_file_form.value()
            print("PREPROCESS "+audio_file)

            self.__vc.load_from_source_file(audio_file)
            self.__vc.reset_progress(preprocess=True)
            self.__run_long_process__(lambda: self.__vc.preprocess(".tmp/"), lambda: self.__gui.voice_sample_form.enable(True))

    def __cover__(self, *args):
        if self.__gui.voice_sample_form.is_valid():
            voice_sample = self.__gui.voice_sample_form.value()
            print("COVER "+voice_sample)

            self.__vc.reset_progress(cover=True, merge=True)
            self.__run_long_process__(lambda: self.__vc.cover(voice_sample, ".tmp/"), self.__merge__)

    def __merge__(self, *args):
            print("MERGE")
            self.__run_long_process__(lambda: self.__vc.merge(".tmp/", 6), self.__vc.progress, self.__gui.voice_sample_progress_bar, lambda: None)
    
    def __run_long_process__(self, process, callback):
            self.__gui.progress_bar.reset()

            t = JoinNonBlockingThread(target=process)
            t.start()

            self.__update_progress__(1, t.join, callback)
    
    def __update_progress__(self, timeout, stop_func, callback):
        self.__gui.progress_bar.set_progress(self.__vc.progress.get(), self.__vc.progress.get_label())

        if stop_func():
            callback()
        else:
            self.after(timeout, lambda: self.__update_progress__(timeout, stop_func, callback))