import socket
import json
import threading
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from login import *

client_list = {}
master_online = (None, False)

def send_update():
    global client_list
    global master_online
    users = " ".join(str(i) for i in list(client_list.values()))
    master_online[0].send(f"UPDATE {users}".encode())
    
def authenticate(client_socket, username, password, user_type):
    global client_list
    global master_online
    if user_type == "users":
        for creds in server_load_credentials()["users"]:
            if username == creds[0] and password == creds[1]:
                client_socket.send("AUTHENTICATED".encode())
                client_list.update({client_socket: username})
                if master_online[1]:
                    send_update()
                return True
        client_socket.send("FAIL".encode())
        return False
    elif user_type == "master":
        creds = server_load_credentials()["master"]
        if username == creds[0] and password == creds[1]:
            client_socket.send("AUTHENTICATED".encode())
            master_online = (client_socket, True)
        else:
            client_socket.send("FAIL".encode())
            
def handle_client(client_socket):
    global client_list
    global master_online
    client_socket.settimeout(60)
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print("Received from client:", data)
            
            split = data.split(" ")
            
            match split[0]:
                case "LOGIN_CLIENT":
                    authenticate(client_socket, split[1], split[2], "users")
                case "LOGIN_MASTER":
                    authenticate(client_socket, split[1], split[2], "master")
                case "HEARTBEAT":
                    pass
                case _:
                    if split[0] in ["LAUNCH_GAME", "LEAVE_GAME", "CLOSE_GAME", "SEARCH_MATCH", "LOAD_MULTIPLAYER"]:
                        for item in list(client_list.keys()):
                            item.send(split[0].encode())
                    
        except socket.timeout:
            client_list.pop(client_socket)
            send_update()
            print("Client connection timed out")
            break
        except Exception as e:
            client_list.pop(client_socket)
            send_update()
            print(f"Error handling client: {str(e)}")
            break
    client_socket.close()


def start_server():
    with open('config.json', 'r') as file:
        data = json.load(file)
        
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((data["host"], data["port"]))

    server_socket.listen(data["max_connections"])
    print("Server is listening on port", data["port"])

    while True:
        client_socket, addr = server_socket.accept()
        print("Connected to:", addr)

        threading.Thread(target=handle_client, args=(client_socket, )).start()

if __name__ == "__main__":
    start_server()
#a