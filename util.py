import json
import sqlite3

from config import APP_VERSION, CONFIG_PATH, DB_PATH, RESET_PATH

def load_config(file) -> None:
    "Interface for loading a json file"
    with open(file, "r") as f:
        return json.load(f)
    
def save_config(config) -> None:
    "Interface for saving a json file"
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def add_year(year: int) -> None:
    """Interface to add a year to the config file

    Args:
        year (int): year [15,50]

    Raises:
        ValueError: if year wrong
    """
    config = load_config(CONFIG_PATH)
    if not 15 < year < 50: raise ValueError(f"[✗] Year {year} is not a valid year.")
    if year not in config["years"]:
        config["years"].append(year)
        save_config(config)

def add_tag(tag: str) -> None:
    config = load_config(CONFIG_PATH)
    if tag not in config["tags"]:
        config["tags"].append(tag)
        save_config(config)

def get_value(key: str) -> None:
    config = load_config(CONFIG_PATH)
    return config.get(key, None)

def check_db_table_ident(month: str, year: int) -> str:
    """_summary_

    Args:
        month (str): _description_
        year (int): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        str: the right table name
    """
    _month = month.capitalize()
    months = get_value("months")
    if _month not in months:
        raise ValueError(f"[✗] Month: {month} is not a valid identifier.")
    if not 15 < year < 50:
        raise ValueError(f"[✗] Year {year} is not a valid year.")
    
    return f"{_month}_{str(year)}"

def execute_sql(query: str) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(query)
    if query.strip().upper().startswith("SELECT"):
        rows = cur.fetchall()
    else:
        con.commit()
        rows = []
    con.close()
    return rows

def reset_config():
    config = load_config(CONFIG_PATH)
    r_config = load_config(RESET_PATH)
    for entry in config:
        config[entry] = r_config[entry]
    save_config(config)

def delete_year(year):
    config = load_config(CONFIG_PATH)
    config["years"].remove(year)
    save_config(config)

def import_csv():
    from tkinter import filedialog, messagebox
    import csv
    import os

    file_path = filedialog.askopenfilename(
        title="Select .csv file",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not file_path:
        return
    
    tags = get_value("tags")
    types = get_value("types")
    months = get_value("months")
    years = get_value("years")

    name = os.path.splitext(os.path.basename(file_path))[0]
    try:
        month, year = name.split("_")
        year = int(year)
    except ValueError:
        messagebox.showerror("Import Error", f"Filename {name} is not valid (expected Month_YY.csv).")
        return

    if month not in months or year not in years:
        messagebox.showerror("Import Error", f"Table {name} is not existing.")
        return

    inserted, skipped = 0, 0
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            req_cols = {"tag", "amount", "description", "type"}

            if not req_cols.issubset(reader.fieldnames):
                messagebox.showerror("Import error", f"CSV must contain columns: {', '.join(req_cols)}")
                return

            for row in reader:
                tag = row["tag"].strip()
                type = row["type"].strip()
                desc = row["description"].strip()
                try:
                    amount = float(row["amount"])
                except ValueError:
                    skipped += 1
                    continue

                if tag not in tags or type not in types:
                    skipped += 1
                    continue

                try:
                    amount = round(amount, 2)
                except ValueError:
                    skipped += 1
                    continue

                execute_sql(f"""
                    INSERT INTO {name} (tag, amount, description, type)
                    VALUES ('{tag}', '{amount}', '{desc}', '{type}')
                """)
                inserted += 1
        messagebox.showinfo("Import Finished", f"Imported {inserted} rows into {name}.\nSkipped {skipped} rows")
    
    except Exception as e:
        messagebox.showerror("Import Error", str(e))

def parse_version(v):
    return tuple(map(int, v.split(".")))

def check_for_updates():
    import requests
    import webbrowser
    from tkinter import messagebox
    REMOTE_URL = "https://raw.githubusercontent.com/rekordii/CashChronicles/main/VERSION"
    DOWNLOAD_URL = "https://rekordii.github.io/DownloadHub/"
    try:
        response = requests.get(REMOTE_URL, timeout=5)
        response.raise_for_status()
        latest = response.text.strip()

        if parse_version(latest) > parse_version(APP_VERSION):
            if messagebox.askyesno(
                "Update Available",
                f"A new version {latest} is available!\n"
                f"You are currently on {APP_VERSION}.\n\n"
                "Open download page?"
            ):
                webbrowser.open(DOWNLOAD_URL)
            else:
                messagebox.showinfo("Up to Date", f"You are on the latest version ({APP_VERSION}).")
    except Exception as e:
        messagebox.showerror("Update Check Failed", f"Could not check for updates:\n{e}")
