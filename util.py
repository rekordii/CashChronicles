import json
import sqlite3
from pathlib import Path

from config import config_file, file_path, reset_file

def load_config(file):
    with open(file, "r") as f:
        return json.load(f)
    
def save_config(config):
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)

def add_year(year: int):
    config = load_config(config_file)
    if not 15 < year < 50: raise ValueError(f"[✗] Year {year} is not a valid year.")
    if year not in config["years"]:
        config["years"].append(year)
        save_config(config)

def add_tag(tag: str):
    config = load_config(config_file)
    if tag not in config["tags"]:
        config["tags"].append(tag)
        save_config(config)

def get_value(key: str):
    config = load_config(config_file)
    return config.get(key, None)

def try_create() -> None: 
    config_path = Path(config_file)
    if not config_path.exists() or config_path.stat().st_size == 0:
        with open (config_file, "w") as f:
            json.dump({"months": [], "years": [], "tags": [], "types": []}, f, indent=4)

    try:
        with open(file_path, 'x') as file:
            pass
    except FileExistsError:
        pass

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
    con = sqlite3.connect(file_path)
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
    config = load_config(config_file)
    r_config = load_config(reset_file)
    for entry in config:
        config[entry] = r_config[entry]
    save_config(config)

def delete_year(year):
    config = load_config(config_file)
    config["years"].remove(year)
    save_config(config)
