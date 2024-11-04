from tkinter import *
from tkinter import ttk
from gui.event import Event
from gui.components import FileBrowserForm

class GUI():
    def __init__(self):
        self.__window__ = None
        self.source_file_form = None
        self.voice_sample_form = None
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
        self.__init_window__()
        self.__init_load_frame__()
        self.__init_cover_frame__()

    def __init_window__(self):
        self.__window__ = Tk()
        self.__window__.title("Voice Cover")
        self.__window__.geometry("500x500")
        self.__center_window__(self.__window__)

    def __init_load_frame__(self):
        self.source_file_form = FileBrowserForm(self.__window__, "Select source audio", 0, 0, 1, 1)

    def __init_cover_frame__(self):
        self.voice_sample_form = FileBrowserForm(self.__window__, "Select voice sample", 0, 1, 1, 1)

    def show(self):        
        self.__window__.mainloop()