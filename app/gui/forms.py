from tkinter import *
from tkinter import ttk
from gui.event import Event
from gui.components import Component, Frame, LabelledFrame, Button, Label, FileExplorerEntry, Dialogs, LabelledTextualScale
import os

class Form(Component):
    def __init__(self, parent, column = 0, row = 0, columnspan = 1, rowspan = 1, *args):
        self.on_submit = Event()
        super().__init__(parent, column, row, columnspan, rowspan, *args)
    
    def __validate__(self):
        pass
    
    def __build_submit_args__(self):
        return ()

    def __on_submit__(self, *args):
        if self.__validate__():
            self.on_submit.invoke(*self.__build_submit_args__())

class ChooseAudioFileForm(Form):
    def __init__(self, parent, value = "", column = 0, row = 0, columnspan = 1, rowspan = 1):
        self.__explorer = None
        self.__explorer_error = None
        super().__init__(parent, column, row, columnspan, rowspan, value)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, value):
        frame = Frame(parent, column, row, columnspan, rowspan)
        frame.configure(1, columns="all", rows="all")
        frame.configure(5, columns=0)

        self.__explorer = FileExplorerEntry(frame.tkframe, value, file_types=[("WAV", ".wav")], column=0, row=0, columnspan=5, rowspan=1)
        self.__explorer.on_value_changed.add_listener(self.__on_value_changed__)
        self.__add_enable_component__(self.__explorer)

        button = Button(frame.tkframe, "Submit", 5, 0, 1, 1)
        button.on_click.add_listener(self.__on_submit__)
        self.__add_enable_component__(button)

        self.__explorer_error = Label(frame.tkframe, column=0, row=1, columnspan=6, rowspan=1)
        self.__add_enable_component__(self.__explorer_error)
    
    def __validate__(self):
        return os.path.isfile(self.__explorer.get_value())
    
    def __build_submit_args__(self):
        return (self.__explorer.get_value(),)
    
    def __on_value_changed__(self, *args):
        value = self.__explorer.get_value()

        if not os.path.isfile(value):
            self.__explorer_error.set_value("Invalid path")
        else:
            self.__explorer_error.set_value("")
            self.__explorer.set_initial_dir(os.path.dirname(value))

class CoverForm(Form):
    def __init__(self, parent, value = "", column = 0, row = 0, columnspan = 1, rowspan = 1):
        self.__explorer = None
        self.__explorer_error = None
        self.__db_scale = None
        super().__init__(parent, column, row, columnspan, rowspan, value)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, value):
        s = ttk.Style()
        s.configure('mGreen.TFrame', background='green')
        s.configure('mRed.TFrame', background='red')
        s.configure('mBlue.TFrame', background='blue')
        frame = Frame(parent, column, row, columnspan, rowspan)
        frame.configure(1, columns="all", rows="all")
        frame.configure(5, columns=0)

        self.__explorer = FileExplorerEntry(frame.tkframe, value, file_types=[("WAV", ".wav")], column=0, row=0, columnspan=5, rowspan=1)
        self.__explorer.on_value_changed.add_listener(self.__on_value_changed__)
        self.__add_enable_component__(self.__explorer)

        self.__explorer_error = Label(frame.tkframe, "ae", column=0, row=1, columnspan=6, rowspan=1)
        self.__add_enable_component__(self.__explorer_error)

        self.__db_scale = LabelledTextualScale(frame.tkframe, -20.0, 20.0, 0.0, 3, "Vocals bonus volume", 0, 2, 5, 2)
        self.__add_enable_component__(self.__db_scale)

        button = Button(frame.tkframe, "Submit", 0, 4, 1, 1)
        button.on_click.add_listener(self.__on_submit__)
        self.__add_enable_component__(button)
    
    def __validate__(self):
        return os.path.isfile(self.__explorer.get_value())
    
    def __build_submit_args__(self):
        return (self.__explorer.get_value(), self.__db_scale.get_value())
    
    def __on_value_changed__(self, *args):
        value = self.__explorer.get_value()

        if not os.path.isfile(value):
            self.__explorer_error.set_value("Invalid path")
        else:
            self.__explorer_error.set_value("")
            self.__explorer.set_initial_dir(os.path.dirname(value))

class SaveAsFileForm(Form):
    def __init__(self, parent, value = "", column = 0, row = 0, columnspan = 1, rowspan = 1):
        self.__value = value
        super().__init__(parent, column, row, columnspan, rowspan, value)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, value):
        button = Button(parent, "Save", column, row, columnspan, rowspan)
        button.on_click.add_listener(self.__on_click__)
        self.__add_enable_component__(button)
    
    def __on_click__(self, *args):
        initial_dir = None
        initial_file = ""

        if self.__value:
            initial_dir = os.path.dirname(self.__value)
            initial_file = os.path.basename(self.__value)

        value = Dialogs.save_as_file(initial_dir=initial_dir, initial_file=initial_file, file_types = [("WAV", ".wav")])

        if value:
            self.__value = value
            self.on_submit.invoke(value)