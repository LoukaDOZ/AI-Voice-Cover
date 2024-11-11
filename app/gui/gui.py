from tkinter import *
from tkinter import Tk, ttk
from gui.event import Event
from gui.components import Component, Button, ProgressBar, AudioPlayer, Dialogs, Dropdown
from gui.forms import ChooseAudioFileForm, SaveAsFileForm
from gui.coroutine import Couroutine
import os

class GUI():
    def __init__(self):
        self.on_request_preprocess = Event()
        self.on_request_cover = Event()
        self.on_request_save_as = Event()

        self.__window = None
        self.progress_bar = None
        self.source_file_form = None
        self.voice_sample_form = None
        self.save_as_form = None
        self.audio_player = None
        self.audio_player_dropdown = None

        self.__init_gui_()

    def __init_gui_(self):
        self.__window = Tk()
        self.__window.title("Voice Cover")
        self.__window.geometry("700x500")
        self.__center_window__(self.__window)

        Component.configure(self.__window, 1, columns="all", rows="all")
        Component.configure(self.__window, 3, columns=0)
        Couroutine.init(self.__window.after)

        lpart = ttk.Frame(self.__window)
        lpart.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=(N, W, E, S))
        Component.configure(lpart, 1, columns="all", rows="all")

        self.source_file_form = ChooseAudioFileForm(lpart, "", 0, 0, 1, 1)
        self.voice_sample_form = ChooseAudioFileForm(lpart, "", 0, 1, 1, 1)
        self.save_as_form = SaveAsFileForm(lpart, "", 0, 2, 1, 1)

        rpart = ttk.Frame(self.__window)
        rpart.grid(column=1, row=0, columnspan=1, rowspan=1, sticky=(N, W, E, S))
        Component.configure(rpart, 1, columns="all", rows="all")

        self.progress_bar = ProgressBar(rpart, False, 1, 0, 1, 1)
        self.audio_player_dropdown = Dropdown(rpart, ["Source audio", "Vocals cover", "Final output"], "Source audio", 1, 1, 1, 1)
        self.audio_player = AudioPlayer(rpart, 1.0, 1, 2, 1, 1)

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

    def show(self):        
        self.__window.mainloop()