import os
import platform
import sys

APP_VERSION = 1.1

# ---------- Create data dirs ----------
if platform.system() == "Windows":
    USER_DATA_DIR = os.path.join(os.environ["APPDATA"], "CashChronicles")
else:
    USER_DATA_DIR = os.path.join(os.path.expanduser("~"), ".cash_chronicles")

os.makedirs(USER_DATA_DIR, exist_ok=True)

# ---------- Data Paths ----------
if hasattr(sys, "_MEIPASS"):
    BASE_PATH = sys._MEIPASS
else:
    BASE = os.path.abspath(os.path.dirname(__file__))
    BASE_PATH = os.path.join(BASE, "..")
DATA_PATH = os.path.join(BASE_PATH, "data")
RESET_PATH = os.path.join(DATA_PATH, "config_to_reset.json")
DB_SOURCE = os.path.join(DATA_PATH, "cash_chronicles.db")
DB_PATH = os.path.join(USER_DATA_DIR, "cash_chronicles.db")
CONFIG_PATH = os.path.join(USER_DATA_DIR, "config.json")
ICON_PATH = os.path.join(DATA_PATH, "icon_120px.png")

# ---------- Copy DB and config files ----------
def atomic_copy(src, dest) -> None:
    """Copy file safely to dest using a temp file and atomic replace."""
    if not os.path.exists(dest):
        temp_dest = dest + ".tmp"
        with open(src, "rb") as fsrc:
            data = fsrc.read()
        with open(temp_dest, "wb") as fdst:
            fdst.write(data)
        os.replace(temp_dest, dest)  # atomic move

atomic_copy(DB_SOURCE, DB_PATH)
atomic_copy(RESET_PATH, CONFIG_PATH)
