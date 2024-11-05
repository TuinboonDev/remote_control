import os
import json
import platform
import socket
from tkinter import messagebox
import threading

def server_create_user(username, password):
    with open("credentials.json", "w") as f:
        data = json.load(f)
        data["users"].append([username, password])
        f.write(data)

def server_delete_credentials():
    if os.path.exists("credentials.json"):
        os.remove("credentials.json")

def server_load_credentials():
    if os.path.exists("credentials.json"):
        with open("credentials.json", "r") as f:
            return json.load(f)
    return "", ""

def client_save_credentials(username, password):
    with open("credentials.txt", "w") as f:
        f.write(f"{username}\n{password}")

def client_delete_credentials():
    if os.path.exists("credentials.txt"):
        os.remove("credentials.txt")

def client_load_credentials():
    if os.path.exists("credentials.txt"):
        with open("credentials.txt", "r") as f:
            username = f.readline().strip()
            password = f.readline().strip()
            return username, password
    return "", ""

def do_login(username, password, perm, client_socket):
    local_ip = socket.gethostbyname(socket.gethostname())
    login_info = f"LOGIN_{perm} {username} {password} {platform.system()} {platform.release()} {local_ip}"
    client_socket.sendall(login_info.encode())
