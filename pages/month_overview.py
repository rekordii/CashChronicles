from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from .pages_config import *
from util import execute_sql, get_value

def display_month_overview(parent, pages, month_to_display, window):
    frame = Frame(parent, bg=BG_COL)

    # ---------- Top Summary Bar ----------
    summary_frame = Frame(frame, bg=BG_HEADER, height=80)
    summary_frame.pack(fill="x", pady=5)
    summary_font = tkFont.Font(family="Arial", size=14, weight="bold")

    income, expense, balance = get_summary(month_to_display)

    selected_month_label = Label(summary_frame, text=f"Month: {month_to_display}",
                             font=summary_font, bg=BG_HEADER, fg=FG_COL)
    selected_month_label.pack(side="right", padx=20)

    total_income_label = Label(summary_frame, text=f"Total income: {income:.2f}",
                               font=summary_font, bg=BG_HEADER, fg=FG_COL)
    total_income_label.pack(side="left", padx=20)

    total_expense_label = Label(summary_frame, text=f"Total expense: {expense:.2f}",
                                font=summary_font, bg=BG_HEADER, fg=FG_COL)
    total_expense_label.pack(side="left", padx=20)

    balance_label = Label(summary_frame, text=f"Balance: {balance:.2f}",
                          font=summary_font, bg=BG_HEADER, fg=FG_COL)
    balance_label.pack(side="left", padx=20)

    def refresh_summary():
        income, expense, balance = get_summary(month_to_display)
        total_income_label.config(text=f"Total income: {income:.2f}")
        total_expense_label.config(text=f"Total expense: {expense:.2f}")
        balance_label.config(text=f"Balance: {balance:.2f}")

    # ---------- Main Content ----------
    content_frame = Frame(frame, bg=BG_COL)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    content_frame.columnconfigure(0, weight=2)  # left
    content_frame.columnconfigure(1, weight=1)  # right
    content_frame.rowconfigure(0, weight=1)

    # Left Frame for Transaction List
    transactions_frame = Frame(content_frame, bg=BG_COL)
    transactions_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))

    tree_columns = ("Tag", "Amount", "Descripion", "Type")
    transaction_tree = ttk.Treeview(transactions_frame, columns=tree_columns, show="headings")
    for col in tree_columns:
        transaction_tree.heading(col, text=col)
        transaction_tree.column(col, anchor="center", width=100)
    transaction_tree.pack(fill="both", expand=True)

    transactions = get_transactions(month_to_display)
    for t in transactions:
        transaction_tree.insert("", "end", values=t)

    # Right Frame for Pie Chart and Buttons
    right_frame = Frame(content_frame, bg=BG_COL)
    right_frame.grid(row=0, column=1, sticky="nsew")

    right_frame.rowconfigure(0, weight=1)
    right_frame.rowconfigure(1, weight=0)
    right_frame.columnconfigure(0, weight=1)

    # ---------- Pie chart Frame ----------
    chart_frame = Frame(right_frame, bg=BG_COL)
    chart_frame.grid(row=0, column=0, sticky="nsew")

    def refresh_pie_chart():
        for widget in chart_frame.winfo_children():
            widget.destroy()
        tags, amounts = get_exp_dist(month_to_display)
        fig, ax = plt.subplots(figsize=(4,4))
        ax.pie(amounts, labels=tags, autopct="%1.1f%%")
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
    refresh_pie_chart()

    # ---------- Bottom buttons ----------
    button_frame = Frame(right_frame, bg=BG_COL)
    button_frame.grid(row=1, column=0, sticky="ew", pady=10)

    btn_font = tkFont.Font(family="Arial", size=14, weight="bold")
    button_style = {
        "bg": BG_HEADER,
        "fg": FG_COL,
        "font": btn_font,
        "relief": FLAT,
        "activebackground": BG_COL,
        "activeforeground": FG_COL_ACTIVE,
        "width": 20,
        "height": 2,
        "highlightthickness": 0,
        "bd": 1
    }

    def add_transaction():
        popup = Toplevel(frame)
        popup.title("Add transaction")
        popup_width = 300
        popup_height = 350
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.config(bg=BG_COL)

        Label(popup, text="Tag:", bg=BG_COL, fg=FG_COL).pack(pady=5)
        tag_var=StringVar()
        predef_tags = get_value("tags")
        tag_dropdown = ttk.Combobox(popup, textvariable=tag_var,
                                    values=predef_tags, state="readonly")
        tag_dropdown.pack(pady=5)

        Label(popup, text="Amount:", bg=BG_COL, fg=FG_COL).pack(pady=5)
        amount_entry = Entry(popup)
        amount_entry.pack(pady=5)

        Label(popup, text="Description:", bg=BG_COL, fg=FG_COL).pack(pady=5)
        desc_entry = Entry(popup)
        desc_entry.pack(pady=5)

        Label(popup, text="Type:", bg=BG_COL, fg=FG_COL).pack(pady=5)
        type_var = StringVar()
        predef_types = get_value("types")
        type_dropdown = ttk.Combobox(popup, textvariable=type_var,
                                    values=predef_types, state="readonly")
        type_dropdown.pack(pady=5)

        def confirm_add(event=None):
            tag = tag_var.get()
            try:
                amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Invalid input", "Amount must be a number")
                return

            if "." in amount_entry.get():
                decimals = amount_entry.get().split(".")[1]
                if len(decimals) > 2:
                    messagebox.showerror("Invalid amount", "Amount cannot have 3 or more digits after decimal point")
                    return

            if len(amount_entry.get()) > 10:
                messagebox.showerror("Please think", "You dont have that much money")
                return

            description = desc_entry.get()
            t_type = type_var.get()
            if not all([tag, description, t_type]):
                messagebox.showerror("Missing input", "Fill all fields to add transaction")
                return

            query = f"INSERT INTO {month_to_display} (tag, amount, description, type) VALUES ('{tag}', '{amount}', '{description}', '{t_type}')"
            execute_sql(query)

            transaction_tree.insert("", "end", values=(tag, amount, description, t_type))
            refresh_pie_chart()
            refresh_summary()
            popup.destroy()

        popup.bind("<Return>", confirm_add)
        popup.bind_all("<Escape>", lambda e: popup.destroy())
        Button(popup, text="Add", command=confirm_add, **button_style).pack(pady=10)

    add_btn = Button(button_frame, text="Add Transaction",
                     command=add_transaction, **button_style)
    add_btn.pack(fill="x", pady=(0,10))

    def remove_transaction():
        selected = transaction_tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a transaction to remove")
            return
        for item in selected:
            values = transaction_tree.item(item, "values")
            tag, amount, description, t_type = values
            try:
                amount = float(amount)
            except ValueError:
                amount = 0
            query = f"DELETE FROM {month_to_display} WHERE tag='{tag}' AND amount='{amount}' AND description='{description}' AND type='{t_type}'"
            execute_sql(query)
            transaction_tree.delete(item)
        refresh_pie_chart()
        refresh_summary()

    remove_btn = Button(button_frame, text="Remove Transaction",
                        command=remove_transaction, **button_style)
    remove_btn.pack(fill="x", pady=(0,10))

    def on_back():
        W_WIDTH = int(window.winfo_screenwidth() * 0.3)
        W_HEIGHT = int(window.winfo_screenheight() * 0.6)
        WINDOW_SIZE = f"{W_WIDTH}x{W_HEIGHT}"
        plt.close("all")
        pages["month_menu"].tkraise()
        window.geometry(WINDOW_SIZE)

    def on_exit():
        plt.close("all")
        window.destroy()

    side_by_side_frame = Frame(button_frame, bg=BG_COL)
    side_by_side_frame.pack(fill="x")

    back_btn = Button(side_by_side_frame, text="◄ Back", command=on_back, **button_style)
    back_btn.pack(side="left", fill="x", expand=True, padx=(0,5))

    exit_btn = Button(side_by_side_frame, text="⤷ Exit", command=on_exit, **button_style)
    exit_btn.pack(side="left", fill="x", expand=True, padx=(5,0))

    window.protocol("WM_DELETE_WINDOW", on_exit)

    return frame

def get_transactions(month_name):
    query = f"SELECT tag, amount, description, type FROM {month_name}"
    rows = execute_sql(query)
    return rows

def get_exp_dist(month_name):
    query = f"SELECT tag, SUM(amount) FROM {month_name} WHERE type='expense' GROUP BY tag"
    rows = execute_sql(query)
    if not rows:
        return ["No data"], [1]
    return zip(*rows)

def get_summary(month_name):
    income_query = f"SELECT SUM(amount) FROM {month_name} WHERE type='income'"
    expense_query = f"SELECT SUM(amount) FROM {month_name} WHERE type='expense'"
    income = execute_sql(income_query)[0][0] or 0
    expense = execute_sql(expense_query)[0][0] or 0
    balance = income - expense
    return income, expense, balance
