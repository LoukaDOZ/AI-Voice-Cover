from tkinter import *
from tkinter import Tk, ttk
from gui.event import Event
from gui.components import Component, Frame, LabelledFrame, Button, ProgressBar, AudioPlayer, Dialogs, Dropdown
from gui.forms import ChooseAudioFileForm, CoverForm, SaveAsFileForm
from gui.coroutine import Couroutine
import os

class GUI(Frame):
    def __init__(self):
        self.on_request_preprocess = Event()
        self.on_request_cover = Event()
        self.on_request_save_as = Event()

        self.__window = None
        self.progress_bar = None
        self.source_file_form = None
        self.cover_form = None
        self.save_as_form = None
        self.audio_player = None
        self.audio_player_dropdown = None

        super().__init__(self, None)

    def __init_gui__(self, *args):
        self.__window = Tk()
        self.__window.title("Voice Cover")
        self.__window.geometry("700x500")
        self.__center_window__(self.__window)
        Couroutine.init(self.__window.after)

        self.tkframe = self.__window
        self.configure(1, columns="all", rows="all")
        self.configure(2, columns=0)

        lpart = Frame(self.__window, 0, 0, 1, 1)
        lpart.configure(1, columns="all", rows="all")

        self.source_file_form = ChooseAudioFileForm(lpart.tkframe, "", 0, 0, 1, 1)
        self.cover_form = CoverForm(lpart.tkframe, "", 0, 1, 1, 1)
        self.save_as_form = SaveAsFileForm(lpart.tkframe, "", 0, 2, 1, 1)

        rpart = Frame(self.__window, 1, 0, 1, 1)
        rpart.configure(1, columns="all", rows="all")

        self.progress_bar = ProgressBar(rpart.tkframe, False, 1, 0, 1, 1)
        self.audio_player_dropdown = Dropdown(rpart.tkframe, ["Source audio", "Vocals cover", "Final output"], "Source audio", 1, 1, 1, 1)
        self.audio_player = AudioPlayer(rpart.tkframe, 1.0, 1, 2, 1, 1)

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