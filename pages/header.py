from tkinter import *
import tkinter.font as tkFont
import tkinter as tk

from .pages_config import bg_header
from config import icon_path

class Header(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=bg_header, height=120)
        self.pack(side="top", fill="x")
        self.pack_propagate(False)

        # Icon
        self.photo = tk.PhotoImage(file=icon_path)

        icon_label = Label(self, image=self.photo, bg=bg_header)
        icon_label.pack(side="left", padx=20)

        # Title
        title_font = tkFont.Font(family="Arial", size=24, weight="bold")
        title_label = Label(self, text="Your CashChronicles", 
                            font=title_font, fg="#f3c669", bg=bg_header)
        title_label.pack(anchor="center", expand=True)
