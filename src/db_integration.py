import sqlite3

from src.config import DB_PATH
from src.util import get_value

def prepare_cash_chronicles() -> None:
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
