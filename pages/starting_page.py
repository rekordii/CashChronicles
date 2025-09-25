from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkFont

from .pages_config import *
from .month_menu import display_month_menu
from util import add_tag, add_year, delete_year, execute_sql, get_value
from db_integration import prepare_cash_chronicles

def display_starting_page(parent, pages, window):
    frame = Frame(parent, bg=bg_col)

    # Header Label
    header_font = tkFont.Font(family="Arial", size=20, weight="bold")
    Label(frame, text="What do you plan to do?", font=header_font, bg=bg_col, fg=fg_col).pack(pady=40)

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
        popup.config(bg=bg_col)

        Label(popup, text="Year (15-50):", bg=bg_col, fg=fg_col).pack(pady=5)
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
        popup.bind("<Escape>", lambda e: popup.destroy())
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
        popup.config(bg=bg_col)

        Label(popup, text="Tag:", bg=bg_col, fg=fg_col).pack(pady=5)
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
        popup.bind("<Escape>", lambda e: popup.destroy())
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
        popup.config(bg=bg_col)

        year_values = [str(y) for y in get_value("years")]

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
        popup.option_add("*TCombobox*Listbox.background", bg_col)
        popup.option_add("*TCombobox*Listbox.foreground", fg_col)
        popup.option_add("*TCombobox*Listbox.selectBackground", bg_header)
        popup.option_add("*TCombobox*Listbox.selectForeground", fg_col_active)
        popup.option_add("*TCombobox*Listbox.font", combo_font)

        Label(popup, text="Year to delete:", bg=bg_col, fg=fg_col).pack(pady=5)
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
        popup.bind("<Escape>", lambda e: popup.destroy())
        Button(popup, text="Delete", command=confirm_delete, **button_style).pack(pady=10)

    view_btn = Button(frame, text="► View month", command=on_view_month, **button_style)
    view_btn.pack(pady=15)

    month_btn = Button(frame, text="► Add year", command=on_add_year, **button_style)
    month_btn.pack(pady=15)

    tag_btn = Button(frame, text="► Add tag", command=on_add_tag, **button_style)
    tag_btn.pack(pady=15)

    delete_btn = Button(frame, text="► Delete Year", command=on_delete_year, **button_style)
    delete_btn.pack(pady=15)

    exit_btn = Button(frame, text="⤷ Exit", command=window.destroy, **button_style)
    exit_btn.pack(pady=15)

    return frame
