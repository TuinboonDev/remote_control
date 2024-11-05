import customtkinter as ctk
import threading
from tkinter import Listbox, END
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from login import *

        # {"text": "Launch Game", "command": "LAUNCH_GAME"},
        # {"text": "Leave Game", "command": "LEAVE_GAME"},
        # {"text": "Close Game", "command": "CLOSE_GAME"},
        # {"text": "Search Match", "command": "SEARCH_MATCH"},
        # {"text": "Load Multiplayer", "command": "LOAD_MULTIPLAYER"}
        
def send_command(socket, command):
    socket.send(command.encode())
            
def get_selected_client():
    selected_indices = clients_listbox.curselection()
    if selected_indices:
        return clients_listbox.get(selected_indices[0])
    return None

def update_clients_display(clients):
    if clients_listbox:
        clients_listbox.delete(0, END)
        for client in clients:
            clients_listbox.insert(END, client)

def create_login_window(socket, root):
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
        command=lambda: threading.Thread(target=do_login, args=(username_entry.get(), password_entry.get(), "MASTER", socket)).start(),
        fg_color="#1E88E5", 
        hover_color="#1565C0", 
        corner_radius=8
    )
    login_button.pack(pady=20)

    login_window.mainloop()

def open_main_gui(socket, root):
    global console_output, clients_listbox, button_frame

    root = ctk.CTkToplevel(root)
    root.title("Command Terminal")
    root.geometry("1000x300")

    button_frame = ctk.CTkFrame(root)
    button_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill=ctk.Y)

    button_config = [
        {"text": "Launch Game", "command": "LAUNCH_GAME"},
        {"text": "Leave Game", "command": "LEAVE_GAME"},
        {"text": "Close Game", "command": "CLOSE_GAME"},
        {"text": "Search Match", "command": "SEARCH_MATCH"},
        {"text": "Load Multiplayer", "command": "LOAD_MULTIPLAYER"}
    ]

    for i, config in enumerate(button_config):
        button = ctk.CTkButton(
            button_frame, 
            text=config["text"], 
            command=lambda cmd=config["command"]: send_command(socket, cmd),
            fg_color="#1E88E5", 
            hover_color="#1565C0", 
            corner_radius=8
        )
        button.configure(font=("Helvetica", 12))
        button.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")

    output_frame = ctk.CTkFrame(root)
    output_frame.pack(side=ctk.RIGHT, padx=10, pady=10, fill=ctk.BOTH, expand=True)

    clients_listbox = Listbox(output_frame, height=20, width=30, selectmode="single", bg="#333333", fg="white", selectbackground="#555555", selectforeground="white")
    clients_listbox.pack(side=ctk.LEFT, padx=10, pady=10, fill=ctk.BOTH, expand=True)
    
    console_output = ctk.CTkTextbox(output_frame, height=20, width=60, wrap="word")
    console_output.pack(side=ctk.RIGHT, padx=10, pady=10, fill=ctk.BOTH, expand=True)

    root.mainloop()