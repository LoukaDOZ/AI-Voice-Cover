from tkinter import *
from tkinter import ttk
from gui.event import Event
from gui.components import FileBrowserForm, ProgressBar

class GUI():
    def __init__(self):
        self.__window = None
        self.after_func = None
        self.source_file_form = None
        self.voice_sample_form = None
        self.source_progress_bar = None
        self.voice_sample_progress_bar = None
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

    def show(self):        
        self.__window.mainloop()