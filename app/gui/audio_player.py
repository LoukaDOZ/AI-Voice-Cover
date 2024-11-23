from tkinter import *
from tkinter import ttk
from gui.components import Component, Frame, Button, Scale, TextualProgressBar
from gui.coroutine import Couroutine
from gui.event import Event
import pygame as pg
import pygame.mixer as mixer
import os

class Player():
    def __init__(self, audio_file = None):
        self.audio_file = None
        self.audio = None
        self.audio_len = 0
        self.volume = 1.0
        self.start_pos = 0.0
        self.on_update = Event()

class Mixer():
    __PLAYERS = []
    __CURRENT = None
    __POS_0 = 0.0
    __END_EVENT = None
    __CO_ID = None
    __IGNORE_STOP = 0

    @staticmethod
    def register(update_listener = None):
        player = Player()

        if update_listener is not None:
            player.on_update.add_listener(update_listener)

        if Mixer.__END_EVENT is None:
            Mixer.__END_EVENT = pg.USEREVENT + 1
            mixer.music.set_endevent(Mixer.__END_EVENT)

        Mixer.__PLAYERS.append(player)
        return len(Mixer.__PLAYERS) - 1
    
    @staticmethod
    def is_playing(pid):
        if pid < 0 or pid >= len(Mixer.__PLAYERS):
            raise Exception(f"Invalid player id: {pid}")

        return Mixer.__CURRENT == pid and mixer.music.get_busy()
    
    @staticmethod
    def get_audio_len(pid):
        if pid < 0 or pid >= len(Mixer.__PLAYERS):
            raise Exception(f"Invalid player id: {pid}")

        return Mixer.__PLAYERS[pid].audio_len
    
    @staticmethod
    def get_pos(pid):
        if pid < 0 or pid >= len(Mixer.__PLAYERS):
            raise Exception(f"Invalid player id: {pid}")
        
        if Mixer.__CURRENT == pid:
            return Mixer.__PLAYERS[pid].start_pos + (mixer.music.get_pos() / 1000.0) - Mixer.__POS_0
        
        return Mixer.__PLAYERS[pid].start_pos
    
    @staticmethod
    def get_volume(pid):
        if pid < 0 or pid >= len(Mixer.__PLAYERS):
            raise Exception(f"Invalid player id: {pid}")

        return Mixer.__PLAYERS[pid].volume

    @staticmethod
    def load(pid, audio_file):
        if not os.path.isfile(audio_file):
            raise Exception(f"Invalid audio file: {audio_file}")

        if pid < 0 or pid >= len(Mixer.__PLAYERS):
            raise Exception(f"Invalid player id: {pid}")
        
        Mixer.__PLAYERS[pid].audio_file = audio_file
        Mixer.__PLAYERS[pid].audio = mixer.Sound(audio_file)
        Mixer.__PLAYERS[pid].audio_len = Mixer.__PLAYERS[pid].audio.get_length()
        Mixer.__PLAYERS[pid].start_pos = 0.0

        if Mixer.__CURRENT == pid:
            Couroutine.instance.stop(Mixer.__CO_ID)
            mixer.music.unpause()
            mixer.music.stop()
            Mixer.__CURRENT = None
            Mixer.__IGNORE_STOP += 1
        
        Mixer.__PLAYERS[pid].on_update.invoke()
    
    @staticmethod
    def play(pid):
        if pid < 0 or pid >= len(Mixer.__PLAYERS):
            raise Exception(f"Invalid player id: {pid}")

        Couroutine.instance.stop(Mixer.__CO_ID)
        
        if Mixer.__CURRENT == pid:
            mixer.music.unpause()
        else:
            if Mixer.__CURRENT is not None:
                Mixer.__PLAYERS[Mixer.__CURRENT].start_pos = Mixer.get_pos(Mixer.__CURRENT)

            mixer.music.load(Mixer.__PLAYERS[pid].audio_file)
            mixer.music.play()

            mixer.music.set_pos(Mixer.get_pos(pid))
            mixer.music.set_volume(Mixer.__PLAYERS[pid].volume)
            Mixer.__update_pos_0__()
            Mixer.__CURRENT = pid
        
        Mixer.__CO_ID = Couroutine.instance.start(Mixer.__update__)
    
    @staticmethod
    def pause(pid):
        if pid < 0 or pid >= len(Mixer.__PLAYERS):
            raise Exception(f"Invalid player id: {pid}")
        
        if Mixer.__CURRENT == pid:
            mixer.music.pause()
            Couroutine.instance.stop(Mixer.__CO_ID)
    
    @staticmethod
    def rewind(pid):
        Mixer.seek(pid, 0.0)
    
    def seek(pid, pos):
        if pid < 0 or pid >= len(Mixer.__PLAYERS):
            raise Exception(f"Invalid player id: {pid}")
        
        if pos < 0.0 or pos > Mixer.__PLAYERS[pid].audio_len:
            raise Exception(f"Invalid audio position: 0.0 <= {pos} <= {Mixer.__PLAYERS[pid].audio_len}")
        
        if Mixer.__CURRENT == pid:
            mixer.music.pause()
            mixer.music.rewind()
            Mixer.__update_pos_0__()

            mixer.music.set_pos(pos)
            Couroutine.instance.stop(Mixer.__CO_ID)

        Mixer.__PLAYERS[pid].start_pos = pos
        Mixer.__PLAYERS[pid].on_update.invoke()
    
    @staticmethod
    def set_volume(pid, volume):
        if pid < 0 or pid >= len(Mixer.__PLAYERS):
            raise Exception(f"Invalid player id: {pid}")
        
        if volume < 0.0 or volume > 1.0:
            raise Exception(f"Invalid volume: 0.0 <= {volume} <= 1.0")

        if Mixer.__CURRENT == pid:
            mixer.music.set_volume(volume)

        Mixer.__PLAYERS[pid].volume = volume
    
    @staticmethod
    def __update__(*args):
        if Mixer.__CURRENT is not None:
            Mixer.__PLAYERS[Mixer.__CURRENT].on_update.invoke()

        for e in pg.event.get():
            if e.type == Mixer.__END_EVENT:
                if Mixer.__IGNORE_STOP > 0:
                    Mixer.__IGNORE_STOP -= 1
                elif Mixer.__CURRENT is not None:
                    Couroutine.instance.stop(Mixer.__CO_ID)
                    Mixer.__PLAYERS[Mixer.__CURRENT].start_pos = 0.0
                    Mixer.__PLAYERS[Mixer.__CURRENT].on_update.invoke()
                    Mixer.__CURRENT = None
    
    @staticmethod
    def __update_pos_0__():
        Mixer.__POS_0 = mixer.music.get_pos() / 1000.0

class AudioPlayer(Component):
    def __init__(self, parent, inital_volume = 1.0, change_timeout = 300, column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = (N,S,E,W)):
        self.__progress_bar = None
        self.__volume = None
        self.__pid = Mixer.register(self.__update__)
        Mixer.set_volume(self.__pid ,inital_volume)

        super().__init__(parent, column, row, columnspan, rowspan, sticky, inital_volume, change_timeout)
    
    def __init_gui__(self, parent, column, row, columnspan, rowspan, sticky, inital_volume, change_timeout):
        frame = Frame(parent, column, row, columnspan, rowspan, sticky)
        frame.configure(1, rows=[0, 1])
        frame.configure(3, columns=3)

        play = Button(frame.tkframe, "Play", 0, 0, 1, 1)
        play.on_click.add_listener(self.__play__)
        self.__add_enable_component__(play)

        pause = Button(frame.tkframe, "Pause", 1, 0, 1, 1)
        pause.on_click.add_listener(self.__pause__)
        self.__add_enable_component__(pause)

        rewind = Button(frame.tkframe, "Rewind", 2, 0, 1, 1)
        rewind.on_click.add_listener(self.__rewind__)
        self.__add_enable_component__(rewind)

        self.__volume = Scale(frame.tkframe, value=inital_volume, column=3, row=0, columnspan=3, rowspan=1)
        self.__volume.on_value_changed.add_listener(self.__on_volume_changed__)
        self.__add_enable_component__(self.__volume)

        self.__progress_bar = TextualProgressBar(frame.tkframe, max_decimals=3, change_timeout=change_timeout, column=0, row=1, columnspan=4, rowspan=1)
        self.__progress_bar.on_value_changed.add_listener(self.__seek__)
        self.__add_enable_component__(self.__progress_bar)
    
    def set_audio(self, audio_file):
        Mixer.load(self.__pid, audio_file)
        self.__progress_bar.set_maximum(Mixer.get_audio_len(self.__pid))
    
    def set_volume(self, volume):
        self.__volume.set_value(volume)
    
    def pause(self):
        self.__pause__()
    
    def __play__(self, *args):
        Mixer.play(self.__pid)
    
    def __pause__(self, *args):
        Mixer.pause(self.__pid)

    def __rewind__(self, *args):
        Mixer.rewind(self.__pid)

    def __seek__(self, *args):
        Mixer.seek(self.__pid, args[0][0])
    
    def __on_volume_changed__(self, *args):
        Mixer.set_volume(self.__pid, args[0][0])

    def __update__(self, *args):
        audio_len = Mixer.get_audio_len(self.__pid)
        pos = max(min(Mixer.get_pos(self.__pid), audio_len), 0.0)
        self.__progress_bar.set_value(pos, trigger_event=False)