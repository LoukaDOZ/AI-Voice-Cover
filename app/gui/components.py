from tkinter import *
from tkinter import ttk, filedialog, simpledialog
from gui.event import Event
import pygame as pg
import pygame.mixer as mixer
import os

class Browser():
    def __init__(self, parent, title, start_dir = None, default = None, column = 0, row = 0, columnspan = 1, rowspan = 1):
        if start_dir is not None and not os.path.isdir(start_dir):
            raise Exception(f"Invalid directory: {start_dir}")

        self.on_value_changed = Event()
        self.on_submit = Event()

        self.__error_var = StringVar(value="")
        self.__path_var = StringVar(value="")
        self.__path_var.trace_add("write", self.on_value_changed.invoke)

        if default is not None:
            self.__path_var.set(default)
        
        self.__path_field = None
        self.__browse_btn = None
        self.__submit_btn = None

        self.__title = title
        self.__start_dir = start_dir if start_dir is not None else os.getcwd()
        self.__init_gui__(parent, column, row, columnspan, rowspan)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan):
        frame = ttk.Frame(parent)
        frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=(N, W, E, S))

        self.__path_field = ttk.Entry(frame, textvariable=self.__path_var)
        self.__path_field.grid(column=0, row=0, columnspan=4, rowspan=1, sticky=(N, W, E, S))

        self.__browse_btn = ttk.Button(frame, text="Browse", command=self.__browse_files__)
        self.__browse_btn.grid(column=4, row=0, columnspan=1, rowspan=1, sticky=(N, W, E, S))

        self.__submit_btn = ttk.Button(frame, text="Submit", command=self.on_submit.invoke)
        self.__submit_btn.grid(column=5, row=0, columnspan=1, rowspan=1, sticky=(N, W, E, S))

        error = ttk.Label(frame, textvariable=self.__error_var)
        error.grid(column=0, row=1, columnspan=5, rowspan=1, sticky=(N, W, E, S))
    
    def __browse_files__(self):
        path = self.__open_browser__(self.__title, self.__start_dir)
        
        if path and len(path) > 0:
            self.__path_var.set(path)
    
    def __open_browser__(self, title, start_dir):
        pass
    
    def value(self):
        return self.__path_var.get()
    
    def set_error(self, message):
        self.__error_var.set(message)
    
    def clear_error(self):
        self.__error_var.set("")
    
    def enable(self, enable):
        if enable:
            self.__path_field.state(["!disabled"])
            self.__browse_btn.state(["!disabled"])
            self.__submit_btn.state(["!disabled"])
        else:
            self.__path_field.state(["disabled"])
            self.__browse_btn.state(["disabled"])
            self.__submit_btn.state(["disabled"])

class FileBrowser(Browser):
    def __init__(self, parent, title, file_types, start_dir = None, default = None, column = 0, row = 0, columnspan = 1, rowspan = 1):
        super().__init__(parent, title, start_dir, default, column, row, columnspan, rowspan)
        self.file_types = file_types

    def __open_browser__(self, title, start_dir):
        start_dir = start_dir if not self.value() else os.path.dirname(self.value())
        return filedialog.askopenfilename(initialdir = start_dir, title = title, filetypes = self.file_types)

class DirBrowser(Browser):
    def __init__(self, parent, title, start_dir = None, default = None, column = 0, row = 0, columnspan = 1, rowspan = 1):
        super().__init__(parent, title, start_dir, default, column, row, columnspan, rowspan)

    def __open_browser__(self, title, start_dir):
        start_dir = start_dir if not self.value() else self.value()
        return filedialog.askdirectory(initialdir = start_dir, title = title)

class SaveAsFileBrowser(Browser):
    def __init__(self, parent, title, file_types, start_dir = None, default = None, column = 0, row = 0, columnspan = 1, rowspan = 1):
        self.__file_types = file_types
        self.__default_file = default
        self.__save_btn = None
        super().__init__(parent, title, start_dir, None, column, row, columnspan, rowspan)
        self.on_value_changed.add_listener(self.on_submit.invoke)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan):
        self.__save_btn = ttk.Button(parent, text="Save", command=self.__browse_files__)
        self.__save_btn.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=(N, W, E, S))

    def __open_browser__(self, title, start_dir):
        start_dir = start_dir #if not self.value() else self.value()
        return filedialog.asksaveasfilename(initialdir = start_dir, title = title, filetypes=self.__file_types, initialfile=self.__default_file, confirmoverwrite=True)
    
    def set_error(self, message):
        pass
    
    def clear_error(self):
        pass
    
    def enable(self, enable):
        self.__save_btn.state(["!disabled"] if enable else ["disabled"])
    
    def set_default_file(self, path):
        if not os.path.isfile(path):
            raise Exception(f"Invalid file: {path}")
        
        self.__default_file = path

class ProgressBar():
    def __init__(self, parent, column = 0, row = 0, columnspan = 1, rowspan = 1, limit = 100):
        self.__limit = limit

        self.__progress = IntVar(value=0)
        self.__progress_bar = None

        self.__text = StringVar(value="")
        self.__text_label = None
        self.__init_gui__(parent, column, row, columnspan, rowspan)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan):
        frame = ttk.Frame(parent)
        frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=(N, W, E, S))

        self.__progress_bar = ttk.Progressbar(frame, maximum=self.__limit, variable=self.__progress, mode='determinate')
        self.__progress_bar.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=(N, W, E, S))

        self.__text_label = ttk.Label(frame, textvariable=self.__text)
        self.__text_label.grid(column=0, row=1, columnspan=1, rowspan=1, sticky=(N, W, E, S))

    def reset(self):
        self.set_progress(0)
        self.set_text("")

    def set_progress(self, progress):
        if 0 > progress > self.end:
            raise Exception(f"Invalid progress value: {progress}")

        self.__progress.set(progress)
    
    def set_text(self, text):
        self.__text.set(text)

class AudioPlayer():
    def __init__(self, parent, label, column = 0, row = 0, columnspan = 1, rowspan = 1):
        self.on_play = Event()
        self.on_pause = Event()
        self.on_rewind = Event()
        self.on_seek = Event()
        self.on_music_ends = Event()
        self.on_volume_changed = Event()

        self.__play_btn = None
        self.__pause_btn = None
        self.__rewind_btn = None
        self.__progress_bar = None
        self.__pos_field = None
        self.__volume_field = None

        self.__audio_loaded = False
        self.__paused = False
        self.__audio = None

        self.__progress = IntVar(value=0)
        self.__pos_var = StringVar(value="0.0")
        self.__volume_var = StringVar(value="1.0")
        self.__volume_var.trace_add("write", self.__on_volume_changed__)
        self.__start_pos = 0.0
        self.__pos_0 = 0.0
        
        self.__MUSIC_END = MUSIC_END = pg.USEREVENT + 1
        mixer.music.set_endevent(self.__MUSIC_END)
        self.__init_gui__(parent, label, column, row, columnspan, rowspan)
    
    def __init_gui__(self, parent, label, column, row, columnspan, rowspan):
        frame = ttk.Frame(parent)
        frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=(N, W, E, S))
        frame['borderwidth'] = 2
        frame['relief'] = 'sunken'

        labell = ttk.Label(frame, text=label)
        labell.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=(N, W, E, S))

        self.__play_btn = ttk.Button(frame, text="Play", command=self.on_play.invoke)
        self.__play_btn.grid(column=0, row=1, columnspan=1, rowspan=1, sticky=(N, W, E, S))

        self.__pause_btn = ttk.Button(frame, text="Pause", command=self.on_pause.invoke)
        self.__pause_btn.grid(column=1, row=1, columnspan=1, rowspan=1, sticky=(N, W, E, S))

        self.__rewind_btn = ttk.Button(frame, text="Rewind", command=self.on_rewind.invoke)
        self.__rewind_btn.grid(column=2, row=1, columnspan=1, rowspan=1, sticky=(N, W, E, S))

        self.__volume_field = ttk.Scale(frame, orient=HORIZONTAL, from_=0.0, to=1.0, variable=self.__volume_var)
        self.__volume_field.grid(column=3, row=1, columnspan=4, rowspan=1, sticky=(N, W, E, S))

        self.__progress_bar = ttk.Progressbar(frame, maximum=100, variable=self.__progress, mode='determinate')
        self.__progress_bar.grid(column=0, row=2, columnspan=4, rowspan=1, sticky=(N, W, E, S))
        self.__progress_bar.bind("<Button 1>", self.__on_click_pos__)

        self.__pos_field = ttk.Entry(frame, textvariable=self.__pos_var)
        self.__pos_field.grid(column=4, row=2, columnspan=1, rowspan=1, sticky=(N, W, E, S))
        self.__pos_field.bind("<Return>", self.__on_submit_pos__)
        self.__pos_field.bind("<FocusOut>", self.__on_submit_pos__)
    
    def get_audio_len(self):
        return self.__audio.get_length() if self.__audio_loaded else 0.0
    
    def get_pos(self):
        return self.__start_pos + mixer.music.get_pos() / 1000.0 - self.__pos_0 if self.__audio_loaded else 0.0

    def is_playing(self):
        return mixer.music.get_busy() if self.__audio_loaded else False
    
    def is_paused(self):
        return self.__paused if self.__audio_loaded else False
    
    def load(self, audio_file):
        if not os.path.isfile(audio_file):
            raise Exception(f"Invalid audio file: {audio_file}")
        
        mixer.music.load(audio_file)
        self.__audio = mixer.Sound(audio_file)
        self.__audio_loaded = True
    
    def play(self):
        if self.__audio_loaded:
            mixer.music.play()
    
    def pause(self, pause):
        if self.__audio_loaded:
            if pause:
                mixer.music.pause()
            else:
                mixer.music.unpause()
        
            self.__paused = pause
    
    def rewind(self):
        self.seek(0.0)

    def seek(self, pos):
        if not self.__audio_loaded:
            return
        
        if 0.0 > pos > self.get_audio_len():
            raise Exception(f"Invalid seek pos: {pos}")
        
        mixer.music.rewind()
        mixer.music.set_pos(pos)
        self.__start_pos = pos
        self.__pos_0 = mixer.music.get_pos() / 1000
    
    def set_volume(self, volume):
        if not self.__audio_loaded:
            return

        if 0.0 > volume > 1.0:
            raise Exception(f"Invalid volume: {volume}")
        
        mixer.music.set_volume(volume)
        self.__volume_field.set(str(volume))

    def update_progress(self):
        if self.__audio_loaded:
            audio_len = self.get_audio_len()
            pos = max(min(self.get_pos(), audio_len), 0.0)
            self.__progress.set(pos / audio_len * 100)
            self.__pos_var.set(round(pos, 3))

            for e in pg.event.get():
                if e.type == self.__MUSIC_END:
                    self.on_music_ends.invoke()
    
    def __on_submit_pos__(self, *args):
        if not self.__audio_loaded or self.is_playing():
            return

        l = self.get_audio_len()
        v = self.__pos_var.get()
        vf = 0.0

        if not v:
            return
        
        try:
            vf = float(v)
        except:
            return
        
        if vf < 0.0:
            vf = 0.0
        elif vf > l:
            vf = l

        self.on_seek.invoke(round(vf, 3))
    
    def __on_click_pos__(self, e):
        self.on_seek.invoke(round(float(e.x / self.__progress_bar.winfo_width() * self.get_audio_len()), 3))
    
    def __on_volume_changed__(self, *args):
        self.on_volume_changed.invoke(float(self.__volume_field.get()))

class YesNoDialog(simpledialog.Dialog):
    def __init__(self, parent, title, question, yes_btn = "Yes", no_btn = "No"):
        self.__question = question
        self.__yes_btn = yes_btn
        self.__no_btn = no_btn
        self.__result = False
        super().__init__(parent, title)
    
    def body(self, master):
        label = ttk.Label(master, text=self.__question)
        label.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=(N, W, E, S))
        label.pack()
        return label
    
    def buttonbox(self):
        box = ttk.Frame(self)
        ttk.Button(box, text=self.__no_btn, width=10, command=self.__no__, default=ACTIVE).pack(side=LEFT, padx=5, pady=5)
        ttk.Button(box, text=self.__yes_btn, width=10, command=self.__yes__).pack(side=LEFT, padx=5, pady=5)
        box.pack()
    
    def apply(self):
        self.result = self.__result
    
    def __yes__(self, *args):
        self.__result = True
        self.ok()
    
    def __no__(self, *args):
        self.__result = False
        self.ok()