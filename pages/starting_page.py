from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkFont

from .pages_config import *
from .month_menu import display_month_menu
from util import add_tag, add_year, delete_year, execute_sql, get_value
from db_integration import prepare_cash_chronicles

def display_starting_page(parent, pages, window):
    frame = Frame(parent, bg=BG_COL)

    width = window.winfo_screenwidth()
    W_WIDTH = int(width * 0.3)
    if width < 1900:
        header_size = 18
        button_size = 16
        button_width = int(W_WIDTH * 0.03)
    else:
        header_size = 20
        button_size = 18
        button_width = int(W_WIDTH * 0.025)

    # Header Label
    header_font = tkFont.Font(family="Arial", size=header_size, weight="bold")
    Label(frame, text="What do you plan to do?", font=header_font, bg=BG_COL, fg=FG_COL).pack(pady=40)

    button_font = tkFont.Font(family="Arial", size=button_size, weight="bold")
    button_style = {
        "bg": BG_HEADER,
        "fg": FG_COL,
        "font": button_font,
        "relief": FLAT,
        "activebackground": BG_COL,
        "activeforeground": FG_COL_ACTIVE,
        "width": button_width,
        "highlightthickness": 0,
        "bd": 1,
        "anchor": "w"
    }

    def on_add_year():
        popup = Toplevel(frame)
        popup.title("Add Year")
        popup_width = 300
        popup_height = 150
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.config(bg=BG_COL)

        Label(popup, text="Year (15-50):", bg=BG_COL, fg=FG_COL).pack(pady=5)
        year_var = StringVar()
        Entry(popup, textvariable=year_var).pack(pady=5)

        def confirm_year(event=None):
            year = year_var.get().strip()

            if not year.isdigit():
                messagebox.showerror("Error", "Must be a number")
                return

            year_num = int(year)
            if year_num in get_value("years"):
                messagebox.showerror("Error", "Year already exists")
                return

            if not (15 <= year_num <= 50):
                messagebox.showerror("Error", "Year must be between 15 and 50")
                return

            add_year(year_num)
            prepare_cash_chronicles()
            messagebox.showinfo("Success", f"Year {year_num} added!")
            popup.destroy()

        popup.bind("<Return>", confirm_year)
        popup.bind_all("<Escape>", lambda e: popup.destroy())
        Button(popup, text="Add", command=confirm_year, **button_style).pack(pady=10)

    def on_view_month():
        if "month_menu" in pages:
            pages["month_menu"].destroy()
            del pages["month_menu"]
        pages["month_menu"] = display_month_menu(parent, pages, window)
        pages["month_menu"].grid(row=0, column=0, sticky="nsew")
        pages["month_menu"].tkraise()

    def on_add_tag():
        popup = Toplevel(frame)
        popup.title("Add Tag")
        popup_width = 300
        popup_height = 150
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.config(bg=BG_COL)

        Label(popup, text="Tag:", bg=BG_COL, fg=FG_COL).pack(pady=5)
        tag_var = StringVar()
        Entry(popup, textvariable=tag_var).pack(pady=5)

        def confirm_tag(event=None):
            tag = tag_var.get().strip()

            if tag == "":
                messagebox.showerror("Error", "Tag cant be empty")
                return

            if tag in get_value("tags"):
                messagebox.showerror("Error", "Tag already exists")
                return

            if len(tag) > 20:
                messagebox.showerror("Error", "Tag too long")
                return

            add_tag(tag)
            messagebox.showinfo("Success", f"Tag {tag} added!")
            popup.destroy()

        popup.bind("<Return>", confirm_tag)
        popup.bind_all("<Escape>", lambda e: popup.destroy())
        Button(popup, text="Add", command=confirm_tag, **button_style).pack(pady=10)

    def on_delete_year():
        popup = Toplevel(frame)
        popup.title("Delete Year")
        popup_width = 300
        popup_height = 200
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.config(bg=BG_COL)

        year_values = [str(y) for y in get_value("years")]

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
        popup.option_add("*TCombobox*Listbox.background", BG_COL)
        popup.option_add("*TCombobox*Listbox.foreground", FG_COL)
        popup.option_add("*TCombobox*Listbox.selectBackground", BG_HEADER)
        popup.option_add("*TCombobox*Listbox.selectForeground", FG_COL_ACTIVE)
        popup.option_add("*TCombobox*Listbox.font", combo_font)

        Label(popup, text="Year to delete:", bg=BG_COL, fg=FG_COL).pack(pady=5)
        del_var = StringVar()
        dropdown = ttk.Combobox(
            popup,
            textvariable=del_var,
            values=year_values,
            state="readonly",
            style="Custom.TCombobox"
        )
        dropdown.pack(pady=20)

        def confirm_delete(event=None):
            year = del_var.get().strip()
            if year == "":
                messagebox.showerror("Error", "Please choose a year")
                return

            year_num = int(year)
            if not (15 <= year_num <= 50):
                messagebox.showerror("Error", "Year must be between 15 and 50")
                return

            if year not in year_values:
                messagebox.showerror("Error", "Year does not exist.")
                return

            delete_year(year_num)
            year_tables = execute_sql(f"""
                SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE'%_{year_num}');
            """)
            for row in year_tables:
                table_name = row[0]
                execute_sql(f"DROP TABLE IF EXISTS {table_name}")

            messagebox.showinfo("Success", f"Tables for {year_num} removed")
            popup.destroy()

        popup.bind("<Return>", confirm_delete)
        popup.bind_all("<Escape>", lambda e: popup.destroy())
        Button(popup, text="Delete", command=confirm_delete, **button_style).pack(pady=10)

    view_btn = Button(frame, text="► View month", command=on_view_month, **button_style)
    view_btn.pack(fill="y", pady=15, expand=True)

    month_btn = Button(frame, text="► Add year", command=on_add_year, **button_style)
    month_btn.pack(fill="y", pady=15, expand=True)

    tag_btn = Button(frame, text="► Add tag", command=on_add_tag, **button_style)
    tag_btn.pack(fill="y", pady=15, expand=True)

    delete_btn = Button(frame, text="► Delete Year", command=on_delete_year, **button_style)
    delete_btn.pack(fill="y", pady=15, expand=True)

    exit_btn = Button(frame, text="⤷ Exit", command=window.destroy, **button_style)
    exit_btn.pack(fill="y", pady=(15, 50), expand=True)

    return frame
