from tkinter import *
from tkinter import ttk
from gui.event import Event
from gui.components import Component, Frame, LabelledFrame, Button, Label, LabelledTextualScale
from gui.dialogs import Dialogs, FileExplorerEntry
from gui.styles import Styles
import os

class Form(LabelledFrame):
    def __init__(self, parent, label_text="", column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W), *args):
        self.on_submit = Event()
        super().__init__(parent, label_text, column, row, columnspan, rowspan, sticky, *args)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, label_text, *args):
        super().__init_gui__(parent, column, row, columnspan, rowspan, sticky, label_text)
        self.padding(3)
    
    def __validate__(self):
        pass
    
    def __build_submit_args__(self):
        return ()

    def __on_submit__(self, *args):
        if self.__validate__():
            self.on_submit.invoke(*self.__build_submit_args__())

class ChooseAudioFileForm(Form):
    def __init__(self, parent, label_text="", value = "", column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        self.__explorer = None
        self.__explorer_error = None
        self.__submit_btn = None
        super().__init__(parent, label_text, column, row, columnspan, rowspan, sticky, value)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, label_text, value):
        super().__init_gui__(parent, column, row, columnspan, rowspan, sticky, label_text)
        self.configure(1, columns=0, rows=2)

        self.__explorer = FileExplorerEntry(self.tkframe, value, file_types=[("WAV", ".wav")], column=0, row=0, columnspan=1, rowspan=1, sticky=(E,W))
        self.__explorer.on_value_changed.add_listener(self.__on_value_changed__)
        self.__add_enable_component__(self.__explorer)

        self.__explorer_error = Label(self.tkframe, column=0, row=1, columnspan=1, rowspan=1, sticky=(E,W), style=Styles.ERROR_LABEL)
        self.__add_enable_component__(self.__explorer_error)

        self.__submit_btn = Button(self.tkframe, "Submit", 0, 2, 1, 1, sticky=(S,E,W))
        self.__submit_btn.on_click.add_listener(self.__on_submit__)
        self.__add_enable_component__(self.__submit_btn)
        self.__submit_btn.enable(False)
    
    def __validate__(self):
        return os.path.isfile(self.__explorer.get_value())
    
    def __build_submit_args__(self):
        return (self.__explorer.get_value(),)
    
    def __on_value_changed__(self, *args):
        value = self.__explorer.get_value()

        if not value:
            self.__submit_btn.enable(False)
            self.__explorer_error.set_value("")
        elif not os.path.isfile(value):
            self.__explorer_error.set_value("Invalid path")
            self.__submit_btn.enable(False)
        else:
            self.__explorer_error.set_value("")
            self.__explorer.set_initial_dir(os.path.dirname(value))
            self.__submit_btn.enable(True)
    
    def enable(self, enable):
        super().enable(enable)

        if enable:
            self.__on_value_changed__()

class CoverForm(Form):
    def __init__(self, parent, label_text="", value = "", column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        self.__explorer = None
        self.__explorer_error = None
        self.__db_scale = None
        self.__submit_btn = None
        super().__init__(parent, label_text, column, row, columnspan, rowspan, sticky, value)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, label_text, value):
        super().__init_gui__(parent, column, row, columnspan, rowspan, sticky, label_text)
        self.configure(1, columns=0, rows=3)

        self.__explorer = FileExplorerEntry(self.tkframe, value, file_types=[("WAV", ".wav")], column=0, row=0, columnspan=1, rowspan=1, sticky=(E,W))
        self.__explorer.on_value_changed.add_listener(self.__on_value_changed__)
        self.__add_enable_component__(self.__explorer)

        button = Button(self.tkframe, "Record", 1, 0, 1, 1, sticky=(E,W))
        button.on_click.add_listener(self.__on_record__)
        self.__add_enable_component__(button)

        self.__explorer_error = Label(self.tkframe, "", column=0, row=1, columnspan=2, rowspan=1, sticky=(E,W), style=Styles.ERROR_LABEL)
        self.__add_enable_component__(self.__explorer_error)

        self.__db_scale = LabelledTextualScale(self.tkframe, -20.0, 20.0, 0.0, 1, "Vocals bonus volume", column=0, row=2, columnspan=2, rowspan=1, sticky=(E,W))
        self.__add_enable_component__(self.__db_scale)

        self.__submit_btn = Button(self.tkframe, "Submit", 0, 3, 2, 1, sticky=(S,E,W))
        self.__submit_btn.on_click.add_listener(self.__on_submit__)
        self.__add_enable_component__(self.__submit_btn)
        self.__submit_btn.enable(False)
    
    def __validate__(self):
        return os.path.isfile(self.__explorer.get_value())
    
    def __build_submit_args__(self):
        return (self.__explorer.get_value(), self.__db_scale.get_value())
    
    def __on_value_changed__(self, *args):
        value = self.__explorer.get_value()

        if not value:
            self.__submit_btn.enable(False)
            self.__explorer_error.set_value("")
        elif not os.path.isfile(value):
            self.__explorer_error.set_value("Invalid path")
            self.__submit_btn.enable(False)
        else:
            self.__explorer_error.set_value("")
            self.__explorer.set_initial_dir(os.path.dirname(value))
            self.__submit_btn.enable(True)
    
    def __on_record__(self, *args):
        self.__submit_btn.enable(False)
        value = Dialogs.record_voice_sample()
        value = value if value is not None else self.__explorer.get_value()
        self.__explorer.set_value(value)
    
    def enable(self, enable):
        super().enable(enable)

        if enable:
            self.__on_value_changed__()

class SaveAsFileForm(Form):
    def __init__(self, parent, label_text="", value = "", column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        self.__value = value
        super().__init__(parent, label_text, column, row, columnspan, rowspan, sticky, value)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, label_text, value):
        super().__init_gui__(parent, column, row, columnspan, rowspan, sticky, label_text)
        self.configure(1, columns=0, rows=0)

        button = Button(self.tkframe, "Save as", 0, 0, 1, 1, (N,E,W))
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