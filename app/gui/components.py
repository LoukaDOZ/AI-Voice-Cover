from tkinter import *
from tkinter import ttk, filedialog
from gui.event import Event
import os

class FileBrowser():
    def __init__(self, parent, column = 0, row = 0, columnspan = 1, rowspan = 1):
        self.on_value_changed = Event()
        self.filepath_var = StringVar(value="")
        self.filepath_var.trace_add("write", self.on_value_changed.invoke)
        self.error_var = StringVar(value="")
        self.__filepath_field = None
        self.__browse_btn = None
        self.__init_gui__(parent, column, row, columnspan, rowspan)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan):
        frame = ttk.Frame(parent)
        frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=(N, W, E, S))

        self.__filepath_field = ttk.Entry(frame, textvariable=self.filepath_var)
        self.__filepath_field.grid(column=0, row=0, columnspan=4, rowspan=1, sticky=(N, W, E, S))

        self.__browse_btn = ttk.Button(frame, text="Browse", command=self.__browse_files__)
        self.__browse_btn.grid(column=4, row=0, columnspan=1, rowspan=1, sticky=(N, W, E, S))

        error = ttk.Label(frame, textvariable=self.error_var)
        error.grid(column=0, row=1, columnspan=5, rowspan=1, sticky=(N, W, E, S))
    
    def __browse_files__(self):
        start_dir = os.getcwd() if not self.filepath_var.get() else os.path.dirname(self.filepath_var.get())
        filename = filedialog.askopenfilename(initialdir = start_dir, title = "Select a File",
            filetypes = (("All files", "*.*"), ("MP3", "*.mp3*"), ("WAV", "*.wav*")))
        
        if len(filename) > 0:
            self.filepath_var.set(filename)
    
    def is_valid(self):
        return os.path.isfile(self.filepath_var.get())
    
    def value(self):
        return self.filepath_var.get()
    
    def set_error(self, message):
        self.error_var.set(message)
    
    def clear_error(self):
        self.error_var.set("")
    
    def enable(self, enable):
        if enable:
            self.__filepath_field.state(["!disabled"])
            self.__browse_btn.state(["!disabled"])
        else:
            self.__filepath_field.state(["disabled"])
            self.__browse_btn.state(["disabled"])

class FileBrowserForm():
    def __init__(self, parent, label, column = 0, row = 0, columnspan = 1, rowspan = 1):
        self.__file_browser = None
        self.__submit_btn = None
        self.on_submit = Event()
        self.__init_gui__(parent, label, column, row, columnspan, rowspan)
    
    def __init_gui__(self, parent, label, column, row, columnspan, rowspan):
        frame = ttk.Frame(parent)
        frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=(N, W, E, S))
        frame['borderwidth'] = 2
        frame['relief'] = 'sunken'

        self.__file_browser = FileBrowser(frame, column, row, columnspan, rowspan)
        self.__file_browser.on_value_changed.add_listener(self.__check_value__)

        self.__submit_btn = ttk.Button(frame, text="Next", command=self.__validate__)
        self.__submit_btn.grid(column=1, row=0, columnspan=1, rowspan=1, sticky=(N, W, E, S))
    
    def __check_value__(self, *args):
        self.__file_browser.clear_error()

        if not self.is_valid():
            self.__file_browser.set_error("invalid path")

    def __validate__(self, *args):
        if self.is_valid():
            self.on_submit.invoke()
    
    def is_valid(self):
        return self.__file_browser.is_valid()
    
    def value(self):
        return self.__file_browser.value()
    
    def enable(self, enable):
        self.__file_browser.enable(enable)

        if enable:
            self.__submit_btn.state(["!disabled"])
        else:
            self.__submit_btn.state(["disabled"])