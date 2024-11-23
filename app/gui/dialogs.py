from tkinter import *
from tkinter import ttk, filedialog, simpledialog
from gui.event import Event
from gui.coroutine import Couroutine
from gui.components import ChangeableComponent, Frame, LabelledFrame, Label, Button, TextEntry, FloatEntry, ProgressBar, Dropdown
from gui.audio_player import AudioPlayer
from gui.thread import JoinNonBlockingThread
from gui.styles import Styles
from cover.result import Result
from cover.recorder import Recorder
from cover.audio import AudioPath
import os
import shutil

class ExplorerEntry(ChangeableComponent):
    def __init__(self, parent, value = "", button_text = "Browse", title = None, initial_dir = None, change_timeout = 0, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        self.__entry = None
        self.__title = title
        self.__initial_dir = initial_dir
        super().__init__(parent, column, row, columnspan, rowspan, sticky, value, button_text, change_timeout)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, value, button_text, change_timeout):
        frame = Frame(parent, column, row, columnspan, rowspan, sticky)
        frame.configure(1, rows=0)
        frame.configure(4, columns=0)

        self.__entry = TextEntry(frame.tkframe, value, change_timeout, None, 0, 0, 1, 1)
        self.__entry.on_value_changed.add_listener(self.on_value_changed.invoke)
        self.__add_enable_component__(self.__entry)

        button = Button(frame.tkframe, button_text, 1, 0, 1, 1)
        button.on_click.add_listener(self.__on_browse__)
        self.__add_enable_component__(button)
    
    def __build_kwargs__(self):
        kwargs = {}

        if self.__title is not None:
            kwargs["title"] = self.__title

        if self.__initial_dir is not None:
            kwargs["initial_dir"] = self.__initial_dir
        
        return kwargs
    
    def __on_browse__(self, *args):
        value = self.__open_browser__(**self.__build_kwargs__())

        if value:
            self.__entry.set_value(value)

    def __open_browser__(self, **kwargs):
        pass
    
    def get_value(self):
        return self.__entry.get_value()
    
    def set_value(self, value, trigger_event = True):
        self.__entry.set_value(value, trigger_event)
    
    def set_initial_dir(self, initial_dir):
        self.__initial_dir = initial_dir

class FileExplorerEntry(ExplorerEntry):
    def __init__(self, parent, value = "", button_text = "Browse", title = None, initial_dir = None, file_types = None, change_timeout = 0, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        self.__file_types = file_types
        super().__init__(parent, value, button_text, title, initial_dir, change_timeout, column, row, columnspan, rowspan, sticky)
    
    def __build_kwargs__(self):
        kwargs = super().__build_kwargs__()

        if self.__file_types is not None:
            kwargs["file_types"] = self.__file_types
    
        return kwargs

    def __open_browser__(self, **kwargs):
        return Dialogs.choose_file(**kwargs)

class DirExplorerEntry(ExplorerEntry):
    def __init__(self, parent, value = "", button_text = "Browse", title = None, initial_dir = None, change_timeout = 0, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        super().__init__(parent, value, button_text, title, initial_dir, change_timeout, column, row, columnspan, rowspan, sticky)

    def __open_browser__(self, **kwargs):
        return Dialogs.choose_dir(**kwargs)

class SaveFileExplorerEntry(ExplorerEntry):
    def __init__(self, parent, value = "", button_text = "Browse", title = None, initial_dir = None, initial_file = None, file_types = None, confirm_overwrite = True, change_timeout = 0, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        self.__file_types = file_types
        self.__initial_file = initial_file
        self.__confirm_overwrite = confirm_overwrite
        super().__init__(parent, value, button_text, title, initial_dir, change_timeout, column, row, columnspan, rowspan, sticky)
    
    def __build_kwargs__(self):
        kwargs = super().__build_kwargs__()

        if self.__file_types is not None:
            kwargs["initial_file"] = self.__initial_file

        if self.__file_types is not None:
            kwargs["file_types"] = self.__file_types

        if self.__file_types is not None:
            kwargs["confirm_overwrite"] = self.__confirm_overwrite
    
        return kwargs

    def __open_browser__(self, **kwargs):
        return Dialogs.save_as_file(**kwargs)

class Dialogs():
    WINDOW = None

    def __init__(self):
        raise Exception("Static class")
    
    @staticmethod
    def init(window):
        Dialogs.WINDOW = window
    
    @staticmethod
    def choose_file(title = "Open file", initial_dir = None, file_types = [("All", ".*")]):
        initial_dir = os.getcwd() if initial_dir is None else initial_dir
        return filedialog.askopenfilename(initialdir = initial_dir, title = title, filetypes = file_types)
    
    @staticmethod
    def choose_dir(title = "Open directory", initial_dir = None):
        initial_dir = os.getcwd() if initial_dir is None else initial_dir
        return filedialog.askdirectory(initialdir = initial_dir, title = title)
    
    @staticmethod
    def save_as_file(title = "Save as file", initial_dir = None, initial_file = "", file_types = [("All", ".*")], confirm_overwrite = True):
        initial_dir = os.getcwd() if initial_dir is None else initial_dir
        return filedialog.asksaveasfilename(initialdir = initial_dir, title = title, filetypes=file_types, initialfile=initial_file, confirmoverwrite=confirm_overwrite)
    
    @staticmethod
    def record_voice_sample():
        return RecordVoiceDialog(Dialogs.WINDOW, "test", 6).result

class BaseDialog(simpledialog.Dialog):
    def __init__(self, parent, title, cancel_text = "Cancel", ok_text = "OK"):
        self.__cancel_text = cancel_text
        self.__ok_text = ok_text
        self.root = None
        self.__ok_btn = None
        self.__cancel_btn = None
        super().__init__(parent, title)
    
    def body(self, master):
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.root = Frame(master)
        return self.root.tkframe
    
    def buttonbox(self):
        box = ttk.Frame(self)

        self.__cancel_btn = ttk.Button(box, text=self.__cancel_text, width=10, command=self.__cancel__, default=ACTIVE)
        self.__cancel_btn.pack(side=LEFT, padx=5, pady=5)
        self.__add_enable_component__(self.__cancel_btn)

        self.__ok_btn = ttk.Button(box, text=self.__ok_text, width=10, command=self.__ok__)
        self.__ok_btn.pack(side=LEFT, padx=5, pady=5)
        self.__add_enable_component__(self.__ok_btn)

        box.pack()
    
    def apply(self):
        pass
    
    def __ok__(self, *args):
        self.ok()
    
    def __cancel__(self, *args):
        self.cancel()
    
    def __add_enable_component__(self, component):
        self.root.__add_enable_component__(component)
    
    def enable(self, enable):
        self.root.enable(enable)
    
    def enable_ok(self, enable):
        self.__ok_btn.state(["!disabled"] if enable else ["disabled"])
    
    def enable_cancel(self, enable):
        self.__cancel_btn.state(["!disabled"] if enable else ["disabled"])

class RecordVoiceDialog(BaseDialog):
    def __init__(self, parent, title, record_duration):
        self.__result = None
        self.__progress_bar = None
        self.__record_btn = None
        self.__audio_player = None
        self.__devices_dropdown = None
        self.__record_error = None
        self.__record_duration = record_duration
        self.__initial_file = AudioPath("voice_samples/my_voice.wav")
        self.__record_file = AudioPath(".tmp/Record.wav")
        self.__devices = []
        self.__save_file = None
        super().__init__(parent, title)
    
    def body(self, master):
        tkframe = super().body(master)
        self.root.configure(1, columns=0, rows=[0,1])

        topframe = Frame(tkframe, 0, 0, 1, 1, (N,E,W))
        topframe.configure(1, columns=0, rows=[0,1,2])

        label = Label(topframe.tkframe, f"Record your voice for {self.__record_duration} seconds", "center", column=0, row=0, columnspan=2, rowspan=1, sticky=(E,W))
        self.__add_enable_component__(label)

        self.__progress_bar = ProgressBar(topframe.tkframe, False, 0, 1, 1, 1, (E,W))
        self.__add_enable_component__(self.__progress_bar)

        self.__progress_entry = FloatEntry(topframe.tkframe, 0.0, float(self.__record_duration), 0.0, 1, column=1, row=1, columnspan=1, rowspan=1, sticky=(E,W))
        self.__progress_entry.enable(False)

        recordframe = Frame(topframe.tkframe, 0, 2, 2, 1)
        recordframe.configure(1, columns=0, rows=0)

        self.__devices_dropdown = Dropdown(recordframe.tkframe, column=0, row=0, columnspan=1, rowspan=1, sticky=(E,W))
        self.__add_enable_component__(self.__devices_dropdown)

        self.__record_btn = Button(recordframe.tkframe, "Record", 1, 0, 1, 1, (E,W))
        self.__record_btn.on_click.add_listener(self.__record__)
        self.__add_enable_component__(self.__record_btn)

        self.__record_error = Label(recordframe.tkframe, column=0, row=1, columnspan=1, rowspan=2, sticky=(E,W), style=Styles.ERROR_LABEL)
        self.__add_enable_component__(self.__record_error)

        midframe = Frame(tkframe, 0, 1, 1, 1, (E,W))
        midframe.configure(1, columns=0)
        midframe.padding(pady=(10,0))

        self.__audio_player = AudioPlayer(midframe.tkframe, 1.0, column=0, row=2, columnspan=1, rowspan=1)
        self.__audio_player.enable(False)
        self.__add_enable_component__(self.__audio_player)

        self.__update_devices__()
        return tkframe
    
    def buttonbox(self):
        super().buttonbox()
        self.enable_ok(False)

    def apply(self):
        shutil.copy(self.__record_file.fullpath, self.__save_file)
        self.result = self.__save_file
    
    def __ok__(self, *args):
        self.__audio_player.pause()
        save_file = Dialogs.save_as_file(initial_dir=self.__initial_file.dirname, initial_file=self.__initial_file.basename, file_types=[("WAV", ".wav")])

        if save_file and os.path.isdir(os.path.dirname(save_file)):
            self.__save_file = save_file
            self.ok()
        else:
            self.__save_file = None
    
    def __cancel__(self, *args):
        Couroutine.instance.stop("record")
        self.__audio_player.pause()
        self.__save_file = None
        self.cancel()
    
    def __get_working_devices__(self):
        self.__devices = Recorder.get_available_devices()
        return self.__devices
    
    def __update_devices__(self):
        devices = [name for _, name in self.__get_working_devices__()]
        value = devices[0] if len(devices) > 0 else "No microphone found"

        self.__record_btn.enable(len(devices) > 0)
        self.__devices_dropdown.set_values(devices)

        if not self.__devices_dropdown.get_value() or len(devices) == 0:
            self.__devices_dropdown.set_value(value)
    
    def __record__(self, *args):
        mic = self.__devices_dropdown.get_value()
        res = Result()
        self.__record_btn.enable(False)
        self.__devices_dropdown.enable(False)
        self.__record_error.enable(False)
        self.__audio_player.enable(False)
        self.__audio_player.pause()
        self.enable_ok(False)
        self.enable_cancel(False)

        for index, name in self.__devices:
            if name == mic:
                thread = JoinNonBlockingThread(target=Recorder.record, args=(self.__record_duration, self.__record_file.fullpath, index, res))
                thread.start()

                Couroutine.instance.start(self.__update_progress__, name="record", args=(thread, res))
                break
    
    def __update_progress__(self, thread, res):
        progress = Recorder.PROGRESS.get()
        self.__progress_bar.set_value(progress)
        self.__progress_entry.set_value(progress * self.__record_duration)

        if thread.join():
            Couroutine.instance.stop("record")
            self.__audio_player.set_audio(self.__record_file.fullpath)
            self.__record_btn.enable(True)
            self.__devices_dropdown.enable(True)
            self.__record_error.enable(True)
            self.__audio_player.enable(True)
            self.enable_ok(True)
            self.enable_cancel(True)
            self.__record_error.set_value("" if res.result else "Unable to record with this microphone")