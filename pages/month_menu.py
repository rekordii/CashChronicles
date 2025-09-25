from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont

from .pages_config import *
from .month_overview import display_month_overview
from util import execute_sql

def display_month_menu(parent, pages, window):
    frame = Frame(parent, bg=bg_col)

    # Header Label
    header_font = tkFont.Font(family="Arial", size=20, weight="bold")
    Label(frame, text="Select a Month", font=header_font, bg=bg_col, fg=fg_col).pack(pady=40)

    tables = [row[0] for row in execute_sql("SELECT name FROM sqlite_master WHERE type='table';")]
    try:
        tables.remove("sqlite_sequence")
    except ValueError:
        pass

    # Custom font
    combo_font = tkFont.Font(family="Arial", size=16)

    # Style for entry box
    style = ttk.Style()
    style.theme_use("default")  # make sure we're on a theme that allows customization

    style.configure(
        "Custom.TCombobox",
        fieldbackground=bg_col,     # background inside entry box
        background=bg_header,       # dropdown button background
        foreground=fg_col,          # text color in entry
        arrowcolor=fg_col,          # color of dropdown arrow
        selectforeground=fg_col_active,
        selectbackground=bg_header,
        font=combo_font,
        padding=5
    )
    window.option_add("*TCombobox*Listbox.background", bg_col)
    window.option_add("*TCombobox*Listbox.foreground", fg_col)
    window.option_add("*TCombobox*Listbox.selectBackground", bg_header)
    window.option_add("*TCombobox*Listbox.selectForeground", fg_col_active)
    window.option_add("*TCombobox*Listbox.font", combo_font)

    # Dropdown Var
    table_var = StringVar()
    dropdown = ttk.Combobox(
        frame,
        textvariable=table_var,
        values=tables,
        state="readonly",
        style="Custom.TCombobox"
    )
    dropdown.pack(pady=20)

    button_font = tkFont.Font(family="Arial", size=18, weight="bold")
    button_style = {
        "bg": bg_header,
        "fg": fg_col,
        "font": button_font,
        "relief": FLAT,
        "activebackground": bg_col,
        "activeforeground": fg_col_active,
        "width": 15,
        "height": 2,
        "highlightthickness": 0,
        "bd": 1
    }

    def on_back():
        pages["starting"].tkraise()

    def on_confirm():
        selected_month = table_var.get()
        if not selected_month:
            messagebox.showwarning(
                title="Nothing selected",
                message="Please choose a month to review!"
                )
            return
        if "month_overview" in pages:
            pages["month_overview"].destroy()
            del pages["month_overview"]

        pages["month_overview"] = display_month_overview(parent, pages, selected_month, window)
        pages["month_overview"].grid(row=0, column=0, sticky="nsew")
        pages["month_overview"].tkraise()
        window.geometry("")

    conf_btn_style = button_style.copy()
    conf_btn_style["bg"] = "green"
    conf_btn_style["fg"] = "black"
    conf_btn = Button(frame, text="⤷ Confirm", command=on_confirm, **conf_btn_style)
    conf_btn.pack(pady=15)

    back_btn = Button(frame, text="◄ Back", command=on_back, **button_style)
    back_btn.pack(pady=15)

    return frame
