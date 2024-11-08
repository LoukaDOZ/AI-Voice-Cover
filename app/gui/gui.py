from tkinter import *
from tkinter import ttk
from gui.event import Event
from gui.components import FileBrowser, DirBrowser, SaveAsFileBrowser, ProgressBar, AudioPlayer, YesNoDialog
import os

class GUI():
    def __init__(self):
        self.__window = None
        self.after_func = None

        self.progress_bar = None
        self.source_browser = None
        self.voice_browser = None
        self.save_as_browser = None
        self.audio_player = None

        self.__FILE_TYPES = [("WAV", ".wav")]
        self.__SAVE_FILE_TYPES = [("WAV", ".wav")]
        self.__init_gui_()

    def __center_window__(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        frm_width = window.winfo_rootx() - window.winfo_x()
        win_width = width + 2 * frm_width
        height = window.winfo_height()
        titlebar_height = window.winfo_rooty() - window.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = window.winfo_screenwidth() // 2 - win_width // 2
        y = window.winfo_screenheight() // 2 - win_height // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        window.deiconify()

    def __init_gui_(self):
        self.__window = Tk()
        self.__window.title("Voice Cover")
        self.__window.geometry("500x500")
        self.__center_window__(self.__window)

        self.after_func = self.__window.after
        
        progress_bar = ProgressBar(self.__window, 0, 0, 10, 1)
        self.progress_bar = ProgressBarManager(progress_bar)
        
        source_file_browser = FileBrowser(self.__window, "Select source audio", self.__FILE_TYPES, column=0, row=1, columnspan=1, rowspan=1)
        self.source_browser = FileBrowserManager(source_file_browser)

        voice_sample_browser = FileBrowser(self.__window, "Select voice sample", self.__FILE_TYPES, column=0, row=2, columnspan=1, rowspan=1)
        self.voice_browser = FileBrowserManager(voice_sample_browser)

        default_save_dir = os.path.join(os.getcwd(), "outputs")
        save_browser = SaveAsFileBrowser(self.__window, "Save output", self.__SAVE_FILE_TYPES, default_save_dir, "Output.wav", 0, 3, 1, 1)
        self.save_as_browser = SaveAsFileBrowserManager(self.__window, save_browser)

        player = AudioPlayer(self.__window, "Player", 0, 4, 1, 1)
        self.audio_player = AudioPlayerManager(self.__window, player)
        self.audio_player.set_audio("/home/doz/Bureau/python/AI-Voice-Cover/.tmp/Instrumentals.wav")

    def show(self):        
        self.__window.mainloop()

class BrowserManager():
    def __init__(self, browser, error_message = "Invalid path"):
        self.__browser = browser
        self.error_message = error_message
        self.on_submit = Event()

        if self.__browser.on_value_changed is not None:
            self.__browser.on_value_changed.add_listener(self.__on_value_changed__)
        self.__browser.on_submit.add_listener(self.__on_submit__)
    
    def enable(self, enbale):
        self.__browser.enable(enbale)
    
    def is_valid(self):
        return self.__validate__(self.__browser.value())
    
    def value(self):
        return self.__browser.value()
    
    def __on_value_changed__(self, *args):
        self.__browser.clear_error()

        if not self.__validate__(self.value()):
            self.__browser.set_error(self.error_message)
    
    def __on_submit__(self, *args):
        if self.__validate__(self.value()):
            self.on_submit.invoke(self.value())
        else:
            self.__browser.set_error(self.error_message)
    
    def __validate__(self, path):
        pass

class FileBrowserManager(BrowserManager):
    def __init__(self, file_browser):
        super().__init__(file_browser)
    
    def __validate__(self, path):
        return os.path.isfile(path)

class SaveAsFileBrowserManager(BrowserManager):
    def __init__(self, window, dir_browser):
        super().__init__(dir_browser)
        self.__window = window
    
    def __validate__(self, path):
        return os.path.isdir(os.path.dirname(path))

class ProgressBarManager():
    def __init__(self, progress_bar):
        self.__progress_bar = progress_bar
    
    def reset(self):
        self.__progress_bar.reset()
    
    def set_progress(self, progress, text = ""):
        self.__progress_bar.set_progress(progress)
        self.__progress_bar.set_text(text)

class AudioPlayerManager():
    def __init__(self, window, audio_player):
        self.__after = window.after
        self.__player = audio_player
        
        self.__player.on_play.add_listener(self.__on_play__)
        self.__player.on_pause.add_listener(self.__on_pause__)
        self.__player.on_rewind.add_listener(self.__on_rewind__)
        self.__player.on_seek.add_listener(self.__on_seek__)
        self.__player.on_music_ends.add_listener(self.__on_music_ends__)
        self.__player.on_volume_changed.add_listener(self.__on_volume_changed__)
    
    def set_audio(self, audio_file):
        self.__player.load(audio_file)
    
    def __on_play__(self, *args):
        if self.__player.is_paused():
            self.__player.pause(False)
        elif not self.__player.is_playing():
            self.__player.play()

        self.__update_gui__()
    
    def __on_pause__(self, *args):
        if not self.__player.is_paused():
            self.__player.pause(True)
    
    def __on_rewind__(self, *args):
        self.__player.rewind()
        self.__player.pause(True)
        self.__update_gui__()
    
    def __on_seek__(self, *args):
        self.__player.seek(args[0][0])
        self.__player.pause(True)
        self.__update_gui__()
    
    def __on_music_ends__(self, *args):
        self.__player.play()
        self.__player.rewind()
        self.__player.pause(True)
        self.__update_gui__()
    
    def __on_volume_changed__(self, *args):
        self.__player.set_volume(args[0][0])
    
    def __update_gui__(self, timeout = 1):
        self.__player.update_progress()

        if self.__player.is_playing() and not self.__player.is_paused():
            self.__after(timeout, lambda: self.__update_gui__(timeout))