import socket
import pickle
import threading

HEADER = 64
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DC_MSG = "/disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)#anything connecting to ADDR will hit this socket

clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DC_MSG:
                connected = False
                print(f"[DISCONNECTED] {addr} has disconnected")
            else:
                update_chat(f"[{addr}] {msg}")

    conn.close()


def update_chat(msg):
    #send all connected clients the message
    for client in clients:
        client.send(msg.encode(FORMAT))
    print(f"{len(clients)} clients updated.")


def start():
    print("[STARTING] Server is starting...")
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

start()
