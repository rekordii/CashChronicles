from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont

from .pages_config import *
from .pages_util import update_page
from .month_overview import display_month_overview
from src.util import execute_sql

def display_month_menu(parent, pages, window):
    frame = Frame(parent, bg=BG_COL)

    # Header Label
    header_font = tkFont.Font(family="Arial", size=20, weight="bold")
    Label(frame, text="Select a Month", font=header_font, bg=BG_COL, fg=FG_COL).pack(pady=40)

    tables = [row[0] for row in execute_sql("SELECT name FROM sqlite_master WHERE type='table';")]
    try:
        tables.remove("sqlite_sequence")
    except ValueError:
        pass

    month_order = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }

    def parse_table_name(name: str):
        try:
            month, year = name.split("_")
            return (int(year), month_order.get(month, 0))
        except ValueError:
            return (0,0)
        
    tables.sort(key=lambda n: (-parse_table_name(n)[0], parse_table_name(n)[1]))

    # Custom font
    combo_font = tkFont.Font(family="Arial", size=16)

    # Style for entry box
    style = ttk.Style()
    style.theme_use("default")  # make sure we're on a theme that allows customization

    style.configure(
        "Custom.TCombobox",
        fieldbackground=BG_COL,     # background inside entry box
        background=BG_HEADER,       # dropdown button background
        foreground=FG_COL,          # text color in entry
        arrowcolor=FG_COL,          # color of dropdown arrow
        selectforeground=FG_COL_ACTIVE,
        selectbackground=BG_HEADER,
        font=combo_font,
        padding=5
    )
    window.option_add("*TCombobox*Listbox.background", BG_COL)
    window.option_add("*TCombobox*Listbox.foreground", FG_COL)
    window.option_add("*TCombobox*Listbox.selectBackground", BG_HEADER)
    window.option_add("*TCombobox*Listbox.selectForeground", FG_COL_ACTIVE)
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
        "bg": BG_HEADER,
        "fg": FG_COL,
        "font": button_font,
        "relief": FLAT,
        "activebackground": BG_COL,
        "activeforeground": FG_COL_ACTIVE,
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
        update_page("month_overview", pages, display_month_overview(parent, pages, selected_month, window))
        window.geometry("")

    conf_btn_style = button_style.copy()
    conf_btn_style["bg"] = "green"
    conf_btn_style["fg"] = "black"
    conf_btn = Button(frame, text="⤷ Confirm", command=on_confirm, **conf_btn_style)
    conf_btn.pack(pady=15)

    back_btn = Button(frame, text="◄ Back", command=on_back, **button_style)
    back_btn.pack(pady=15)

    return frame
