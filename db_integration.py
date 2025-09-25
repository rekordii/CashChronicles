import sqlite3

from config import DB_PATH
from util import check_db_table_ident, execute_sql, get_value, try_create

def prepare_cash_chronicles() -> None:
    try_create()
    months = get_value("months")
    years = get_value("years")
    skipped: int = 0
    created: int = 0

    #Database Connection and addition of tables
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    for month in months:
        for year in years:
            table_name = f"{month}_{str(year)}"
            try:
                cur.execute(f"""CREATE TABLE {table_name}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag TEXT, 
                    amount REAL, 
                    description TEXT, 
                    type TEXT
                    )""")
                created += 1
            except sqlite3.OperationalError:
                skipped += 1
    con.commit()
    con.close()

    #Checking
    print(f"[✓] Created {created} tables.")
    print(f"[✓] Skipped the creation of {skipped} tables.")

def edit_db(month: str, year: int, mode: bool = 0) -> None:
    """Interface to add or drop tables inside the database

    Args:
        month (str): _description_
        year (int): _description_
        mode (bool): 0 for adding elements to db, 1 for removing them
    """
    table_name: str = check_db_table_ident(month, year)
    if mode:
        execute_sql(f"DROP TABLE IF EXISTS {table_name}")
    else:
        execute_sql(f"""CREATE TABLE {table_name}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag TEXT, 
                    amount REAL, 
                    description TEXT, 
                    type TEXT
                    )""")

def delete_table_entries(month: str, year: int) -> None:
    table_name: str = check_db_table_ident(month, year)
    execute_sql(f"DELETE FROM {table_name}")

def add_table_entry(
    month: str, 
    year: int, 
    tag: str, 
    amount: float, 
    description: str, 
    type: str
) -> None:
    # Check for tag and type
    tags = get_value("tags")
    if tag not in tags:
        raise ValueError(f"Couldn't find tag {tag}.")
    types = get_value("types")
    if type not in types:
        raise ValueError(f"Couldn't find type {type}.")
    
    table_name: str = check_db_table_ident(month, year)
    stmt = f"""
    INSERT INTO {table_name} (tag, amount, description, type)
    VALUES ('{tag}', '{amount}', '{description}', '{type}')
    """
    execute_sql(stmt)

def display_tables() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    if not tables:
        print("[✓] Database is empty (no tables).")
    else:
        print("\n[✓] Database has tables:", tables)
    con.commit()
    con.close()
