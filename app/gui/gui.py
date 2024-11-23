from tkinter import *
from tkinter import Tk, ttk
from gui.event import Event
from gui.components import Component, Frame, LabelledFrame, MarginFrame, Button, ProgressBar, LabelledProgressBar, Dropdown, TextEntry
from gui.forms import ChooseAudioFileForm, CoverForm, SaveAsFileForm
from gui.audio_player import AudioPlayer
from gui.coroutine import Couroutine
from gui.dialogs import Dialogs
from gui.styles import Styles
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
        self.__window.geometry("625x325")
        self.__center_window__(self.__window)
        Couroutine.init(self.__window.after)
        Dialogs.init(self.__window)
        Styles.init()

        self.tkframe = self.__window
        self.padding(5)
        self.configure(1, columns=0, rows=[1,2])

        pbmargin = MarginFrame(self.__window, marginy=(0,10), column=0, row=0, columnspan=2, rowspan=1, sticky=(N,E,W))
        self.progress_bar = ProgressBar(pbmargin.tkframe, False, 0, 0, 1, 1)

        lframe = Frame(self.__window, 0, 1, 1, 1, (N,S,W))
        lframe.configure(1, columns=0, rows=[0,1])
        smargin = MarginFrame(lframe.tkframe, marginy=(0,10))
        self.source_file_form = ChooseAudioFileForm(smargin.tkframe, "Source audio", "", 0, 0, 1, 1)
        self.save_as_form = SaveAsFileForm(lframe.tkframe, "Save output", "", 0, 1, 1, 1)

        rframe = Frame(self.__window, 1, 1, 1, 1, (N,S,E))
        rframe.configure(1, columns=0, rows=0)
        self.cover_form = CoverForm(rframe.tkframe, "Voice cover", "", 0, 0, 1, 1)

        pmargin = MarginFrame(self.__window, marginy=(5,0), column=0, row=2, columnspan=2, rowspan=1, sticky=(S,E,W))
        pframe = LabelledFrame(pmargin.tkframe, "Audio player", 0, 0, 1, 1)
        pframe.configure(1, columns=0)
        pframe.padding(3)

        self.audio_player_dropdown = Dropdown(pframe.tkframe, [], "", 0, 0, 1, 1, sticky=(N,W,E))
        self.audio_player = AudioPlayer(pframe.tkframe, 1.0, column=0, row=1, columnspan=1, rowspan=1, sticky=(S,W,E))

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
    
    def padding(self, padding = 0, padx = None, pady = None):
        padx = padx if padx is not None else padding
        pady = pady if pady is not None else padding
        self.tkframe.config(padx=padx, pady=pady)