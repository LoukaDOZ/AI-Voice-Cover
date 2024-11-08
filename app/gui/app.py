from gui.gui import GUI
from cover.vc import VoiceCover
from gui.thread import JoinNonBlockingThread
import shutil

class VoiceCoverApp():
    def __init__(self):
        self.__vc = VoiceCover()
        self.__gui = GUI()
        self.__gui.source_browser.on_submit.add_listener(self.__preprocess__)
        self.__gui.voice_browser.on_submit.add_listener(self.__cover__)
        self.__gui.save_as_browser.on_submit.add_listener(self.__save_as__)

        self.__gui.voice_browser.enable(False)
        self.__gui.save_as_browser.enable(True)
        self.after = self.__gui.after_func
    
    def run(self):
        self.__gui.show()
    
    def __preprocess__(self, *args):
        self.__gui.voice_browser.enable(False)
        self.__gui.save_as_browser.enable(False)

        if self.__gui.source_browser.is_valid():
            audio_file = self.__gui.source_browser.value()
            print("PREPROCESS "+audio_file)

            self.__vc.load_from_source_file(audio_file)
            self.__vc.reset_progress(preprocess=True)
            self.__run_long_process__(lambda: self.__vc.preprocess(".tmp/", "Vocals", "Instrumentals"), lambda: self.__gui.voice_browser.enable(True))

    def __cover__(self, *args):
        if self.__gui.voice_browser.is_valid():
            voice_sample = self.__gui.voice_browser.value()
            print("COVER "+voice_sample)

            self.__vc.reset_progress(cover=True, merge=True)
            self.__run_long_process__(lambda: self.__vc.cover(voice_sample, ".tmp/", "Cover"), self.__merge__)

    def __merge__(self, *args):
            print("MERGE")
            self.__run_long_process__(lambda: self.__vc.merge(".tmp/", "Output", vocal_bonus_db=6), lambda: self.__gui.save_as_browser.enable(True))
    
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
    
    def __save_as__(self, *args):
        shutil.copy(".tmp/Output.wav", args[0][0])