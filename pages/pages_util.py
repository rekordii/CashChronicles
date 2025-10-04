def get_curr_month() -> str:
    from datetime import datetime
    month = datetime.now().strftime("%B")
    year = datetime.now().strftime("%y")
    return f"{month}_{year}"

from tkinter import *
def update_page(page, pages, function):
    if page in pages:
        pages[page].destroy()
        del pages[page]
    pages[page] = function
    pages[page].grid(row=0, column=0, sticky="nsew")
    pages[page].tkraise()
    