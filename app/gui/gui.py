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

        s = ttk.Style()
        s.configure('mGreen.TFrame', background='green')
        s.configure('mRed.TFrame', background='red')
        s.configure('mBlue.TFrame', background='blue')

        self.tkframe = self.__window
        self.configure(10, columns=0, rows=0)
        self.configure(1, columns=1)

        lframe = Frame(self.__window, 0, 0, 1, 1)
        lframe.configure(1, columns=0)

        self.source_file_form = ChooseAudioFileForm(lframe.tkframe, "", 0, 0, 1, 1)
        self.cover_form = CoverForm(lframe.tkframe, "", 0, 1, 1, 1)
        self.save_as_form = SaveAsFileForm(lframe.tkframe, "", 0, 2, 1, 1)

        rframe = Frame(self.__window, 1, 0, 1, 1)
        rframe.configure(1, columns=0)

        self.progress_bar = ProgressBar(rframe.tkframe, False, 0, 0, 1, 1)
        self.audio_player_dropdown = Dropdown(rframe.tkframe, [], "", 0, 1, 1, 1)
        self.audio_player = AudioPlayer(rframe.tkframe, 1.0, 0, 2, 1, 1)

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