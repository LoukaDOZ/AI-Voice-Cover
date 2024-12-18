from tkinter import *
from tkinter import ttk
from gui.event import Event
from gui.coroutine import Couroutine
from gui.styles import Styles
import math
import time

class Component():
    def __init__(self, parent, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W), *args):
        self.enabled = True
        self.__enable_components = []
        self.__enable_multi_components = []
        self.__init_gui__(parent, column, row, columnspan, rowspan, sticky, *args)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, *args):
        pass
    
    def __add_enable_component__(self, component):
        if isinstance(component, Component):
            self.__enable_multi_components.append(component)
        else:
            self.__enable_components.append(component)
    
    def enable(self, enable):
        self.enabled = enable
        flag = ["!disabled"] if enable else ["disabled"]

        for component in self.__enable_components:
            component.state(flag)

        for component in self.__enable_multi_components:
            component.enable(enable)

class ClickableComponent(Component):
    def __init__(self, parent, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W), *args):
        self.on_click = Event()
        super().__init__(parent, column, row, columnspan, rowspan, sticky, *args)

class ChangeableComponent(Component):
    def __init__(self, parent, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W), *args):
        self.on_value_changed = Event()
        super().__init__(parent, column, row, columnspan, rowspan, sticky, *args)

class VariableComponent(ChangeableComponent):
    def __init__(self, parent, var, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W), *args):
        self.__trigger_event = True
        self.__var = var
        self.__var.trace_add("write", self.__on_value_changed__)
        super().__init__(parent, column, row, columnspan, rowspan, sticky, self.__var, *args)
    
    def get_value(self):
        return self.__var.get()
    
    def set_value(self, value, trigger_event = True):
        self.__trigger_event = trigger_event
        self.__var.set(value)
    
    def __on_value_changed__(self, *args):
        accepted = self.__before_on_value_changed__(self.__trigger_event)

        if accepted and self.__trigger_event:
            self.on_value_changed.invoke(self.get_value())

        self.__trigger_event = True
    
    def __before_on_value_changed__(self, trigger_event):
        return True

class StringVariableComponent(VariableComponent):
    def __init__(self, parent, value="", column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W), *args):
        super().__init__(parent, StringVar(value=value), column, row, columnspan, rowspan, sticky, *args)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, var, *args):
        pass

class FloatVariableComponent(VariableComponent):
    def __init__(self, parent, value=0.0, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W), *args):
        super().__init__(parent, DoubleVar(value=value), column, row, columnspan, rowspan, *args)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, var, *args):
        pass

class Frame(Component):
    def __init__(self, parent, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W), *args):
        self.tkframe = None
        super().__init__(parent, column, row, columnspan, rowspan, sticky, *args)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, *args):
        self.tkframe = self.__init_frame__(parent, *args)
        self.tkframe.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        self.__add_enable_component__(self.tkframe)
    
    def __init_frame__(self, parent, *args):
        return ttk.Frame(parent)
    
    def configure(self, weight, columns = None, rows = None):
        if columns is not None:
            self.tkframe.columnconfigure(columns, weight=weight)

        if rows is not None:
            self.tkframe.rowconfigure(rows, weight=weight)
    
    def padding(self, padding = 0, padx = None, pady = None):
        pad = [0, 0, 0, 0]

        if isinstance(padding, (list, tuple)) and len(padding) == 4:
            pad = padding
        elif isinstance(padding, int):
            pad[0] = pad[1] = pad[2] = pad[3] = padding
        else:
            raise Exception(f"Invalid padding: {padding}")
        
        if padx is not None:
            if isinstance(padx, (list, tuple)) and len(padx) == 2:
                pad[0] = padx[0]
                pad[2] = padx[1]
            elif isinstance(padx, int):
                pad[0] = pad[1] = padx
            else:
                raise Exception(f"Invalid padx: {padx}")
        
        if pady is not None:
            if isinstance(pady, (list, tuple)) and len(pady) == 2:
                pad[1] = pady[0]
                pad[3] = pady[1]
            elif isinstance(pady, int):
                pad[0] = pad[1] = pady
            else:
                raise Exception(f"Invalid pady: {pady}")
        
        self.tkframe.config(padding=pad)

class LabelledFrame(Frame):
    def __init__(self, parent, label_text="", column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W), *args):
        super().__init__(parent, column, row, columnspan, rowspan, sticky, label_text, *args)
    
    def __init_frame__(self, parent, label_text, *args):
        return ttk.LabelFrame(parent, text=" " + label_text + " ")

class MarginFrame(Frame):
    def __init__(self, parent, margin = 0, marginx = None, marginy = None, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W), *args):
        super().__init__(parent, column, row, columnspan, rowspan, sticky, margin, marginx, marginy, *args)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, margin, marginx, marginy, *args):
        super().__init_gui__(parent, column, row, columnspan, rowspan, sticky, *args)
        self.configure(1, columns=0, rows=0)
        self.margin(margin, marginx, marginy)
    
    def margin(self, margin = 0, marginx = None, marginy = None):
        self.padding(margin, marginx, marginy)

class Label(StringVariableComponent):
    def __init__(self, parent, value="", anchor="w", column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W), style = None):
        super().__init__(parent, value, column, row, columnspan, rowspan, sticky, anchor, style)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, var, anchor, style):
        label = ttk.Label(parent, textvariable=var, anchor=anchor, style=style)
        label.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        self.__add_enable_component__(label)
    
    def set_value(self, value, trigger_event = False):
        super().set_value(value, trigger_event)

class Button(ClickableComponent):
    def __init__(self, parent, text, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        super().__init__(parent, column, row, columnspan, rowspan, sticky, text)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, text):
        button = ttk.Button(parent, text=text, command=self.on_click.invoke)
        button.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        self.__add_enable_component__(button)

class Dropdown(StringVariableComponent):
    def __init__(self, parent, values = [], default = "", column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        self.__box = None
        super().__init__(parent, default, column, row, columnspan, rowspan, sticky, values)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, var, values):
        self.__box = ttk.Combobox(parent, textvariable=var, values=values)
        self.__box.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        self.__box.state(["readonly"])
        self.__add_enable_component__(self.__box)
    
    def set_values(self, values):
        self.__box["values"] = values

class TextEntry(StringVariableComponent):
    def __init__(self, parent, value="", change_timeout = 0, width = 5, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        if change_timeout < 0:
            raise Exception(f"Invalid change timeout: 0 < {change_timeout}")

        self.on_enter = Event()
        self.on_focus_lost = Event()
        self.__change_timeout = change_timeout
        self.__co_id = None
        super().__init__(parent, value, column, row, columnspan, rowspan, sticky, width)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, var, width):
        entry = ttk.Entry(parent, textvariable=var, width=width)
        entry.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        entry.bind("<Return>", self.__on_enter__)
        entry.bind("<FocusOut>", self.__on_focus_lost__)
        self.on_value_changed.add_listener(self.__kill_co__)
        self.__add_enable_component__(entry)
    
    def __before_on_value_changed__(self, trigger_event):
        if not trigger_event:
            return True

        self.__kill_co__()
        if self.__change_timeout > 0:
            self.__co_id = Couroutine.instance.timeout(self.__trigger_value_changed__, self.__change_timeout)
            return False
        
        return True
    
    def __trigger_value_changed__(self, *args):
        if self.__co_id is not None:
            self.__kill_co__()
            self.on_value_changed.invoke(self.get_value())
    
    def __kill_co__(self, *args):
        if self.__co_id is not None:
            Couroutine.instance.stop(self.__co_id)
            self.__co_id = None
    
    def __on_enter__(self, *args):
        self.on_enter.invoke(self.get_value())
    
    def __on_focus_lost__(self, *args):
        self.on_focus_lost.invoke(self.get_value())

class FloatEntry(TextEntry):
    def __init__(self, parent, minimum=0.0, maximum=1.0, value=0.0, max_decimals=None, change_timeout = 0, width = 5, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        if minimum > maximum:
            raise Exception(f"Invalid minimum: {minimum} < {maximum}")
            
        if max_decimals is not None and max_decimals < 0:
            raise Exception(f"Invalid max decimals: {max_decimals}")

        super().__init__(parent, change_timeout=change_timeout, width=width, column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        self.__round = max_decimals
        self.minimum = None
        self.maximum = None

        self.set_minimum(minimum)
        self.set_maximum(maximum)
        self.set_value(value)
    
    def __round__(self, value):
        return math.floor(value * 10 ** self.__round) / 10 ** self.__round
    
    def __trigger_value_changed__(self, *args):
        v = super().get_value()

        if not v:
            v = self.minimum
        
        try:
            v = float(v)
        except:
            v = self.minimum
        
        if v < self.minimum:
            v = self.minimum
        elif v > self.maximum:
            v = self.maximum

        v = self.__round__(v)
        self.set_value(v, False)
        super().__trigger_value_changed__(*args)
    
    def __on_enter__(self, *args):
        self.on_enter.invoke(self.get_value())
    
    def __on_focus_lost__(self, *args):
        self.on_focus_lost.invoke(self.get_value())
    
    def get_value(self):
        return float(super().get_value())
    
    def set_value(self, value, trigger_event = True):
        value = min(max(float(value), self.minimum), self.maximum)
        super().set_value(str(self.__round__(value)), trigger_event)
    
    def set_minimum(self, minimum):
        self.minimum = self.__round__(minimum)
    
    def set_maximum(self, maximum):
        self.maximum = self.__round__(maximum)

class Scale(FloatVariableComponent):
    def __init__(self, parent, minimum=0.0, maximum=1.0, value=0.0, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        if minimum > maximum:
            raise Exception(f"Invalid minimum: {minimum} < {maximum}")

        self.minimum = minimum
        self.maximum = maximum
        super().__init__(parent, value, column, row, columnspan, rowspan, sticky)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, var):
        scale = ttk.Scale(parent, orient=HORIZONTAL, from_=self.minimum, to=self.maximum, variable=var)
        scale.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        self.__add_enable_component__(scale)
    
    def set_value(self, value, trigger_event = True):
        value = min(max(float(value), self.minimum), self.maximum)
        super().set_value(value, trigger_event)

class ProgressBar(ClickableComponent):
    def __init__(self, parent, clickable = False, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        self.__progress_bar = None
        self.__progress = IntVar(value=0)
        self.__clickable = clickable
        super().__init__(parent, column, row, columnspan, rowspan, sticky)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky):
        self.__progress_bar = ttk.Progressbar(parent, maximum=100, variable=self.__progress, mode='determinate')
        self.__progress_bar.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        self.__progress_bar.bind("<Button 1>", self.__on_click__)
        self.__add_enable_component__(self.__progress_bar)
    
    def __on_click__(self, event):
        if self.enabled and self.__clickable:
            self.on_click.invoke(float(event.x / self.__progress_bar.winfo_width()))
    
    def get_value(self):
        return float(self.__progress.get() / 100.0)
    
    def set_value(self, value):
        value = float(value)
        
        if value < 0.0 or value > 1.0:
            raise Exception(f"Invalid value: 0.0 <= {value} <= 1.0")
        
        self.__progress.set(int(value * 100))

class LabelledProgressBar(ClickableComponent):
    def __init__(self, parent, clickable = False, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        self.__progress_bar = None
        self.__label = None
        super().__init__(parent, column, row, columnspan, rowspan, sticky, clickable)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, clickable):
        frame = Frame(parent, column, row, columnspan, rowspan, sticky)
        frame.configure(1, columns=0, rows=[0, 1])

        self.__progress_bar = ProgressBar(frame.tkframe, clickable, 0, 0, 1, 1)
        self.__progress_bar.on_click.add_listener(self.on_click.invoke)
        self.__add_enable_component__(self.__progress_bar)

        self.__label = Label(frame.tkframe, "", 0, 1, 1, 1)
        self.__add_enable_component__(self.__label)
    
    def __on_click__(self, event):
        if self.enabled and self.__clickable:
            self.on_click.invoke(float(event.x / self.__progress_bar.winfo_width()))
    
    def get_value(self):
        return self.__progress_bar.get_value()
    
    def set_value(self, value, label = None):
        self.__progress_bar.set_value(value)

        if label is not None:
            self.set_label(label)
    
    def set_label(self, label):
        self.__label.set_value(label)

class TextualProgressBar(ChangeableComponent):
    def __init__(self, parent, minimum=0.0, maximum=1.0, value=0.0, max_decimals=None, change_timeout = 300, entry_width = 5, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        if maximum == 0.0:
            raise Exception(f"Invalid maximum: {maximum}")

        self.__progress_bar = None
        self.__entry = None
        super().__init__(parent, column, row, columnspan, rowspan, sticky, minimum, maximum, value, max_decimals, change_timeout, entry_width)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, minimum, maximum, value, max_decimals, change_timeout, entry_width):
        frame = Frame(parent, column, row, columnspan, rowspan, sticky)
        frame.configure(1, columns=1, rows=0)
        frame.configure(10, columns=0)

        self.__progress_bar = ProgressBar(frame.tkframe, True, 0, 0, 1, 1)
        self.__progress_bar.on_click.add_listener(self.__on_click_bar__)
        self.__add_enable_component__(self.__progress_bar)

        self.__entry = FloatEntry(frame.tkframe, minimum, maximum, value, max_decimals, change_timeout, entry_width, 1, 0, 1, 1)
        self.__entry.on_value_changed.add_listener(self.__on_entry_changed__)
        self.__entry.on_enter.add_listener(self.__on_entry_changed__)
        self.__entry.on_focus_lost.add_listener(self.__on_entry_changed__)
        self.__add_enable_component__(self.__entry)
    
    def __on_click_bar__(self, *args):
        self.__entry.set_value(float(args[0][0] * self.__entry.maximum), trigger_event=False)
        self.__progress_bar.set_value(float(self.__entry.get_value() / self.__entry.maximum))
        self.on_value_changed.invoke(self.__entry.get_value())
    
    def __on_entry_changed__(self, *args):
        value = args[0][0]
        self.__progress_bar.set_value(float(value / self.__entry.maximum))
        self.on_value_changed.invoke(value)
    
    def get_value(self):
        return self.__entry.get_value()
    
    def set_value(self, value, trigger_event = True):
        self.__entry.set_value(value, False)
        self.__progress_bar.set_value(float(self.__entry.get_value() / self.__entry.maximum))

        if trigger_event:
            self.on_value_changed.invoke(self.__entry.get_value())
    
    def set_maximum(self, maximum):
        self.__entry.set_maximum(maximum)

class TextualScale(ChangeableComponent):
    def __init__(self, parent, minimum=0.0, maximum=1.0, value=0.0, max_decimals=None, change_timeout = 300, entry_width = 5, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        self.__scale = None
        self.__entry = None
        super().__init__(parent, column, row, columnspan, rowspan, sticky, minimum, maximum, value, max_decimals, change_timeout, entry_width)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, minimum, maximum, value, max_decimals, change_timeout, entry_width):
        frame = Frame(parent, column, row, columnspan, rowspan, sticky)
        frame.configure(1, columns=1, rows=0)
        frame.configure(10, columns=0)
        
        self.__scale = Scale(frame.tkframe, minimum, maximum, value, 0, 0, 1, 1)
        self.__scale.on_value_changed.add_listener(self.__on_scale_changed__)
        self.__add_enable_component__(self.__scale)

        self.__entry = FloatEntry(frame.tkframe, minimum, maximum, value, max_decimals, change_timeout, entry_width, 1, 0, 1, 1)
        self.__entry.on_value_changed.add_listener(self.__on_entry_changed__)
        self.__entry.on_enter.add_listener(self.__on_entry_changed__)
        self.__entry.on_focus_lost.add_listener(self.__on_entry_changed__)
        self.__add_enable_component__(self.__entry)
    
    def __on_scale_changed__(self, *args):
        self.__entry.set_value(args[0][0])
    
    def __on_entry_changed__(self, *args):
        self.__scale.set_value(args[0][0], False)
        self.on_value_changed.invoke(self.get_value())
    
    def get_value(self):
        return self.__entry.get_value()
    
    def set_value(self, value, trigger_event = True):
        self.__entry.set_value(value, False)
        self.__scale.set_value(self.__entry.get_value(), False)

        if trigger_event:
            self.on_value_changed.invoke(self.__entry.get_value())

class LabelledTextualScale(ChangeableComponent):
    def __init__(self, parent, minimum=0.0, maximum=1.0, value=0.0, max_decimals=None, label="", change_timeout = 300, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        self.__scale = None
        super().__init__(parent, column, row, columnspan, rowspan, sticky, minimum, maximum, value, max_decimals, label, change_timeout)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, minimum, maximum, value, max_decimals, label_text, change_timeout):
        frame = LabelledFrame(parent, label_text, column, row, columnspan, rowspan, sticky)
        frame.configure(1, columns=0, rows=0)
        self.__add_enable_component__(frame)
        
        self.__scale = TextualScale(frame.tkframe, minimum, maximum, value, max_decimals, change_timeout, column=0, row=0, columnspan=1, rowspan=1)
        self.__scale.on_value_changed.add_listener(self.on_value_changed.invoke)
        self.__add_enable_component__(self.__scale)
    
    def get_value(self):
        return self.__scale.get_value()
    
    def set_value(self, value, trigger_event = True):
        self.__scale.set_value(self.__entry.get_value(), trigger_event)