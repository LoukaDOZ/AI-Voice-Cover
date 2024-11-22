from tkinter import *
from tkinter import ttk

class Styles():
    ERROR_LABEL = "Custom.TLabel"

    def __init__(self):
        raise Exception("Static class")
    
    @staticmethod
    def init():
        style = ttk.Style()
        style.configure(Styles.ERROR_LABEL, foreground="#c80000")