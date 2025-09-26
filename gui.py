from tkinter import *

from pages import header, starting_page
from pages.pages_config import BG_COL
from config import ICON_PATH

window = Tk()
W_WIDTH = int(window.winfo_screenwidth() * 0.3)
W_HEIGHT = int(window.winfo_screenheight() * 0.8)
WINDOW_SIZE = f"{W_WIDTH}x{W_HEIGHT}"
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

# ---------- Start with Starting page ----------
for page in pages.values():
    page.grid(row=0, column=0, sticky="nsew")

pages["starting"].tkraise()

window.mainloop()
