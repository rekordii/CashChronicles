from tkinter import *
import tkinter.font as tkFont
import tkinter as tk

from .pages_config import BG_HEADER
from config import ICON_PATH

class Header(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_HEADER, height=120)
        self.pack(side="top", fill="x")
        self.pack_propagate(False)

        # ---------- Icon ----------
        self.photo = tk.PhotoImage(file=ICON_PATH)

        icon_label = Label(self, image=self.photo, bg=BG_HEADER)
        icon_label.pack(side="left", padx=20)

        # ---------- Title ----------
        width = parent.winfo_screenwidth()
        title_size = 20 if width < 1900 else 24
        title = "CashChronicles" if width < 1900 else "Your CashChronicles"
        title_font = tkFont.Font(family="Arial", size=title_size, weight="bold")
        title_label = Label(self, text=title,
                            font=title_font, fg="#f3c669", bg=BG_HEADER)
        title_label.pack(anchor="center", expand=True)
