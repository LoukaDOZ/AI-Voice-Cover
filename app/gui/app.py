from gui.gui import GUI
from gui.thread import JoinNonBlockingThread
from gui.coroutine import Couroutine
from cover.vc import VoiceCover
from cover.audio import AudioFile, AudioPath
import shutil

class VoiceCoverApp():
    def __init__(self):
        self.__dropdown_values_source_only = ["Source audio"]
        self.__dropdown_values_all = ["Source audio", "Vocals cover", "Final output"]

        self.__vc = VoiceCover(".tmp/")
        self.__gui = GUI()
        self.__gui.source_file_form.on_submit.add_listener(self.__preprocess__)
        self.__gui.cover_form.on_submit.add_listener(self.__cover__)
        self.__gui.save_as_form.on_submit.add_listener(self.__save_as__)
        self.__gui.audio_player_dropdown.on_value_changed.add_listener(self.__on_audio_dropdown_changed__)

        self.__gui.cover_form.enable(False)
        self.__gui.save_as_form.enable(False)
        self.__gui.audio_player.enable(False)
        self.__gui.audio_player_dropdown.enable(False)
        self.__gui.audio_player_dropdown.set_values(self.__dropdown_values_source_only)

        self.__vc_data = None
    
    def run(self):
        self.__gui.show()
    
    def __preprocess__(self, *args):
        self.__gui.cover_form.enable(False)
        self.__gui.save_as_form.enable(False)
        self.__gui.audio_player.enable(False)
        self.__gui.audio_player_dropdown.enable(False)
        self.__gui.audio_player_dropdown.set_values(self.__dropdown_values_source_only)
        self.__gui.audio_player_dropdown.set_value(self.__dropdown_values_source_only[0])

        source_file = args[0][0]
        print("PREPROCESS "+source_file)

        self.__vc_data = VoiceCover.from_source_file(source_file)
        self.__vc.reset_progress(self.__vc_data, preprocess=True)
        self.__run_long_process__(lambda: self.__vc.preprocess(self.__vc_data), self.__after_preprocess__)
    
    def __after_preprocess__(self):
        self.__gui.cover_form.enable(True)
        self.__gui.audio_player.enable(True)
        self.__gui.audio_player_dropdown.enable(True)
        self.__gui.audio_player.set_audio(self.__vc_data.source_path.fullpath)
        self.__on_audio_dropdown_changed__(self.__gui.audio_player_dropdown.get_value())

    def __cover__(self, *args):
        self.__gui.save_as_form.enable(False)
        
        voice_sample, vocals_bonus_db = args[0]
        print("COVER "+voice_sample)

        self.__vc.reset_progress(self.__vc_data, cover=True, merge=True)
        self.__run_long_process__(lambda: self.__vc.cover(voice_sample, self.__vc_data), lambda *args: self.__merge__(vocals_bonus_db))

    def __merge__(self, vocals_bonus_db):
            print("MERGE")
            self.__run_long_process__(lambda: self.__vc.merge(self.__vc_data, vocal_bonus_db=vocals_bonus_db), self.__after_merge__)
    
    def __after_merge__(self, *args):
        self.__gui.save_as_form.enable(True)
        self.__gui.audio_player_dropdown.enable(True)
        self.__gui.audio_player_dropdown.set_values(self.__dropdown_values_all)
        self.__on_audio_dropdown_changed__(self.__gui.audio_player_dropdown.get_value())
    
    def __save_as__(self, *args):
        if self.__vc_data.is_merged:
            shutil.copy(self.__vc_data.output, args[0][0])
    
    def __run_long_process__(self, process, callback):
            self.__gui.progress_bar.set_value(0.0)

            t = JoinNonBlockingThread(target=process)
            t.start()

            Couroutine.instance.start("update progress", self.__update_progress__, 1, t.join, callback)
    
    def __update_progress__(self, stop_func, callback):
        self.__gui.progress_bar.set_value(self.__vc.progress.get())

        if stop_func():
            Couroutine.instance.stop("update progress")
            callback()
    
    def __on_audio_dropdown_changed__(self, *args):
        match args[0][0]:
            case "Source audio":
                if self.__vc_data:
                    self.__gui.audio_player.set_audio(self.__vc_data.source_path.fullpath)
            case "Vocals cover":
                if self.__vc_data and self.__vc_data.is_merged:
                    self.__gui.audio_player.set_audio(self.__vc_data.cover)
            case "Final output":
                if self.__vc_data and self.__vc_data.is_merged:
                    self.__gui.audio_player.set_audio(self.__vc_data.output)