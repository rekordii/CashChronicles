from tkinter import *

from pages import header, month_menu, starting_page
from pages.pages_config import BG_COL, WINDOW_SIZE
from config import ICON_PATH

window = Tk()
window.geometry(WINDOW_SIZE)
window.title("CashChronicles")
window.config(background=BG_COL)
icon = PhotoImage(file=ICON_PATH)
window.iconphoto(True, icon)

# ---------- Main Frame ----------
main = Frame(window, bg=BG_COL)
main.pack(fill="both", expand=True)

header = header.Header(main)

# ---------- Content Frame ----------
content = Frame(main, bg=BG_COL)
content.pack(fill="both", expand=True)
content.grid_rowconfigure(0, weight=1)
content.grid_columnconfigure(0, weight=1)

# ---------- Collect pages ----------
pages = {}
pages["starting"] = starting_page.display_starting_page(content, pages, window)
pages["month_menu"] = month_menu.display_month_menu(content, pages, window)

# ---------- Start with Starting page ----------
for page in pages.values():
    page.grid(row=0, column=0, sticky="nsew")

pages["starting"].tkraise()

window.mainloop()
