from tkinter import *
from tkinter import ttk, filedialog
from gui.event import Event
import pygame as pg
import pygame.mixer as mixer
import os

class FileBrowser():
    def __init__(self, parent, title, column = 0, row = 0, columnspan = 1, rowspan = 1):
        self.on_value_changed = Event()
        self.filepath_var = StringVar(value="")
        self.filepath_var.trace_add("write", self.on_value_changed.invoke)
        self.error_var = StringVar(value="")
        self.__filepath_field = None
        self.__browse_btn = None
        self.__title = title
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
        filename = filedialog.askopenfilename(initialdir = start_dir, title = self.__title,
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

class DirBrowser():
    def __init__(self, parent, title, column = 0, row = 0, columnspan = 1, rowspan = 1):
        self.on_value_changed = Event()
        self.dirpath_var = StringVar(value="")
        self.dirpath_var.trace_add("write", self.on_value_changed.invoke)
        self.error_var = StringVar(value="")
        self.__dirpath_field = None
        self.__browse_btn = None
        self.__title = title
        self.__init_gui__(parent, column, row, columnspan, rowspan)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan):
        frame = ttk.Frame(parent)
        frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=(N, W, E, S))

        self.__dirpath_field = ttk.Entry(frame, textvariable=self.dirpath_var)
        self.__dirpath_field.grid(column=0, row=0, columnspan=4, rowspan=1, sticky=(N, W, E, S))

        self.__browse_btn = ttk.Button(frame, text="Browse", command=self.__browse_files__)
        self.__browse_btn.grid(column=4, row=0, columnspan=1, rowspan=1, sticky=(N, W, E, S))

        error = ttk.Label(frame, textvariable=self.error_var)
        error.grid(column=0, row=1, columnspan=5, rowspan=1, sticky=(N, W, E, S))
    
    def __browse_files__(self):
        start_dir = os.getcwd() if not self.dirpath_var.get() else os.path.dirname(self.dirpath_var.get())
        dirname = filedialog.askdirectory(initialdir = start_dir, title = self.__title)
        
        if len(dirname) > 0:
            self.dirpath_var.set(dirname)
    
    def is_valid(self):
        return os.path.isdir(self.dirpath_var.get())
    
    def value(self):
        return self.dirpath_var.get()
    
    def set_error(self, message):
        self.error_var.set(message)
    
    def clear_error(self):
        self.error_var.set("")
    
    def enable(self, enable):
        if enable:
            self.__dirpath_field.state(["!disabled"])
            self.__browse_btn.state(["!disabled"])
        else:
            self.__dirpath_field.state(["disabled"])
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

        self.__file_browser = FileBrowser(frame, label, column, row, columnspan, rowspan)
        self.__file_browser.on_value_changed.add_listener(self.__check_value__)

        self.__submit_btn = ttk.Button(frame, text="Next", command=self.__validate__)
        self.__submit_btn.grid(column=1, row=0, columnspan=1, rowspan=1, sticky=(N, W, E, S))
    
    def __check_value__(self, *args):
        self.__file_browser.clear_error()

        if not self.is_valid():
            self.__file_browser.set_error("Invalid path")

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

class DirBrowserForm():
    def __init__(self, parent, label, column = 0, row = 0, columnspan = 1, rowspan = 1):
        self.__dir_browser = None
        self.__submit_btn = None
        self.on_submit = Event()
        self.__init_gui__(parent, label, column, row, columnspan, rowspan)
    
    def __init_gui__(self, parent, label, column, row, columnspan, rowspan):
        frame = ttk.Frame(parent)
        frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=(N, W, E, S))

        self.__dir_browser = DirBrowser(frame, label, column, row, columnspan, rowspan)
        self.__dir_browser.on_value_changed.add_listener(self.__check_value__)

        self.__submit_btn = ttk.Button(frame, text="Next", command=self.__validate__)
        self.__submit_btn.grid(column=1, row=0, columnspan=1, rowspan=1, sticky=(N, W, E, S))
    
    def __check_value__(self, *args):
        self.__dir_browser.clear_error()

        if not self.is_valid():
            self.__dir_browser.set_error("Invalid path")

    def __validate__(self, *args):
        if self.is_valid():
            self.on_submit.invoke()
    
    def is_valid(self):
        return self.__dir_browser.is_valid()
    
    def value(self):
        return self.__dir_browser.value()
    
    def enable(self, enable):
        self.__dir_browser.enable(enable)

        if enable:
            self.__submit_btn.state(["!disabled"])
        else:
            self.__submit_btn.state(["disabled"])

class ProgressBar():
    def __init__(self, parent, column = 0, row = 0, columnspan = 1, rowspan = 1, limit = 100):
        self.__limit = limit
        self.__progress = IntVar(value=0)
        self.__progress_bar = None
        self.__init_gui__(parent, column, row, columnspan, rowspan)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan):
        self.__progress_bar = ttk.Progressbar(parent, maximum=self.__limit, variable=self.__progress, mode='determinate')
        self.__progress_bar.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=(N, W, E, S))

    def reset(self):
        self.set_progress(0)

    def set_progress(self, progress):
        if 0 > progress > self.end:
            raise Exception(f"Invalid progress value: {progress}")

        self.__progress.set(progress)

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
        print(self.__audio.get_length())
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