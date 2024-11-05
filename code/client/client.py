import socket
import json
import threading
import customtkinter as ctk
import tkinter as tk
import time

from commands import *
from gui import *

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def find_login_window():
    root = tk._default_root
    if root is None:
        messagebox.showerror("Exiting", "Root is None")
        os._exit(1)
        return None
    for widget in root.winfo_children():
        if isinstance(widget, ctk.CTkToplevel):
            return widget
    return None

def listen_for_clients():
    global client_socket
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            handle_response(data)
        except OSError as e:
            messagebox.showerror("Socket Error", f"{e}")
            os._exit(1)
            break

def get_login_data():
    login_window = find_login_window()
    
    if login_window is None:
        messagebox.showerror("Exiting", "Login window not available")
        os._exit(1)
        return

    data = []
    for widget in login_window.winfo_children():
        if isinstance(widget, ctk.CTkEntry):
            data.append(widget.get())
        elif isinstance(widget, ctk.CTkCheckBox):
            data.append(widget.get())
            
    return login_window, data

def handle_response(response):
    split = response.split(" ")
    
    match split[0]:
        case "AUTHENTICATED":
            login_window, data = get_login_data()
            client_save_credentials(data[0], data[1]) if data[2] == 1 else client_delete_credentials()
            print("Login successful")
            if login_window:
                login_window.destroy()
        case "FAIL":
            messagebox.showerror("Login Failed", "Invalid Username/Password, please try again.")
        case "LAUNCH_GAME":
            launch_game()
        case _:
            # ["LAUNCH_GAME", "LEAVE_GAME", "CLOSE_GAME", "SEARCH_MATCH", "LOAD_MULTIPLAYER"]
            print(response)

def start_client(root):
    with open('config.json', 'r') as file:
        data = json.load(file)
        
    try:
        client_socket.connect((data["host"], data["port"]))
        print("Connected to server")
    except socket.error as e:
        # TODO: try again
        print(f"Failed to connect to server: {e}")
        return
    
    root.after(0, create_login_window, client_socket, root)
    threading.Thread(target=listen_for_clients, daemon=True).start()
    threading.Thread(target=keep_alive).start()
    
def keep_alive():
    while True:
        client_socket.send("HEARTBEAT".encode())
        time.sleep(45)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.withdraw()
    start_client(root)
    root.mainloop()
