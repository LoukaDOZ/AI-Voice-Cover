from tkinter import Tk
from gui.event import Event
from gui.components import Button, ProgressBar, AudioPlayer, Dialogs, Dropdown
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
        Couroutine.init(self.__window.after)

        self.progress_bar = ProgressBar(self.__window, False, 0, 0, 1, 1)
        self.source_file_form = ChooseAudioFileForm(self.__window, "", 0, 1, 1, 1)
        self.voice_sample_form = ChooseAudioFileForm(self.__window, "", 0, 2, 1, 1)
        self.save_as_form = SaveAsFileForm(self.__window, "", 0, 3, 1, 1)
        self.audio_player = AudioPlayer(self.__window, 1.0, 0, 4, 1, 1)
        self.audio_player_dropdown = Dropdown(self.__window, ["Source audio", "Vocals cover", "Final output"], "Source audio", 0, 5, 1, 1)

    def show(self):        
        self.__window.mainloop()
    
    def set_audio_dropdown_values(self, source_only = False):
        if source_only:
            self.audio_player_dropdown.set_values(["Source audio"])
            self.audio_player_dropdown.set_value("Source audio")
        else:
            self.audio_player_dropdown.set_values(["Source audio", "Vocals cover", "Final output"])