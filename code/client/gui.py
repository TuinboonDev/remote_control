import customtkinter as ctk
import threading
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from login import *


def create_login_window(client_socket, root):
    global login_window, username_entry, password_entry, remember_me_var

    login_window = ctk.CTkToplevel(root)
    login_window.title("Login")
    login_window.geometry("300x300")

    saved_username, saved_password = client_load_credentials()

    ctk.CTkLabel(login_window, text="Username:", text_color="white").pack(pady=10)
    username_entry = ctk.CTkEntry(login_window)
    username_entry.insert(0, saved_username)
    username_entry.pack(pady=5)

    ctk.CTkLabel(login_window, text="Password:", text_color="white").pack(pady=10)
    password_entry = ctk.CTkEntry(login_window, show="*")
    password_entry.insert(0, saved_password)
    password_entry.pack(pady=5)

    remember_me_var = ctk.IntVar(value=1 if saved_username and saved_password else 0)
    remember_me_checkbox = ctk.CTkCheckBox(login_window, text="Remember Me", variable=remember_me_var, text_color="white")
    remember_me_checkbox.pack(pady=10)

    login_button = ctk.CTkButton(
        login_window, 
        text="Login", 
        command=lambda: threading.Thread(target=do_login, args=(username_entry.get(), password_entry.get(), "CLIENT", client_socket)).start(),
        fg_color="#1E88E5", 
        hover_color="#1565C0", 
        corner_radius=8
    )
    login_button.pack(pady=20)

    login_window.mainloop()