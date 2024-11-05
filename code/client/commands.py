import os

def launch_game():
    COD_PATH = f"C:\\Users\\{os.getlogin()}\\Desktop\\Call of Duty®.lnk"
    if os.path.exists(COD_PATH):
        os.startfile(COD_PATH)
    else:
        print("Call of Duty shortcut not found.")