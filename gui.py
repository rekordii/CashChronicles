from tkinter import *

from pages import header, month_menu, starting_page
from pages.pages_config import bg_col, window_size
from config import icon_path

window = Tk()
window.geometry(window_size)
window.title("CashChronicles")
window.config(background=bg_col)
icon = PhotoImage(file=icon_path)
window.iconphoto(True, icon)

# Main Frame
main = Frame(window, bg=bg_col)
main.pack(fill="both", expand=True)

header = header.Header(main)

# Content Frame
content = Frame(main, bg=bg_col)
content.pack(fill="both", expand=True)
content.grid_rowconfigure(0, weight=1)
content.grid_columnconfigure(0, weight=1)

# Collect pages
pages = {}
pages["starting"] = starting_page.display_starting_page(content, pages, window)
pages["month_menu"] = month_menu.display_month_menu(content, pages, window)

# Start with Starting page
for page in pages.values():
    page.grid(row=0, column=0, sticky="nsew")

pages["starting"].tkraise()

window.mainloop()
