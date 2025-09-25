import os
import platform

if platform.system() == "Windows":
    user_data_dir = os.path.join(os.environ["APPDATA"], "CashChronicles")
else:
    user_data_dir = os.path.join(os.path.expanduser("~"), ".cash_chronicles")

os.makedirs(user_data_dir, exist_ok=True)

# ---------- Data Paths ----------
base_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(base_path, "data")
config_source = os.path.join(data_path, "config.json")
reset_file = os.path.join(data_path, "config_to_reset.json")
db_source = os.path.join(data_path, "cash_chronicles.db")

file_path = os.path.join(user_data_dir, "cash_chronicles.db")
config_file = os.path.join(user_data_dir, "config.json")

def atomic_copy(src, dest):
    """Copy file safely to dest using a temp file and atomic replace."""
    if not os.path.exists(dest):
        temp_dest = dest + ".tmp"
        with open(src, "rb") as fsrc:
            data = fsrc.read()
        with open(temp_dest, "wb") as fdst:
            fdst.write(data)
        os.replace(temp_dest, dest)  # atomic move

# Copy DB and config files
atomic_copy(db_source, file_path)
atomic_copy(config_source, config_file)

resources_path = os.path.join(base_path, "resources")
icon_png = os.path.join(resources_path, "icon_120px.png")
icon_ico = os.path.join(resources_path, "icon_120px.ico")
icon_path = icon_ico if platform.system() == "Windows" else icon_png
