from tkinter import *
from tkinter import ttk
from gui.event import Event
from gui.components import FileBrowserForm, ProgressBar, AudioPlayer

class GUI():
    def __init__(self):
        self.__window = None
        self.after_func = None
        self.source_file_form = None
        self.voice_sample_form = None
        self.source_progress_bar = None
        self.voice_sample_progress_bar = None
        self.audio_player = None
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
        
        self.source_file_form = FileBrowserForm(self.__window, "Select source audio", 0, 0, 1, 1)
        self.source_progress_bar = ProgressBar(self.__window, 0, 1, 1, 1)

        self.voice_sample_form = FileBrowserForm(self.__window, "Select voice sample", 0, 2, 1, 1)
        self.voice_sample_progress_bar = ProgressBar(self.__window, 0, 3, 1, 1)

        player = AudioPlayer(self.__window, "Player", 0, 4, 1, 1)
        self.audio_player = AudioPlayerManager(self.__window, player)
        self.audio_player.set_audio("/home/doz/Bureau/python/AI-Voice-Cover/.tmp/Instrumentals.wav")

    def show(self):        
        self.__window.mainloop()

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