import socket, threading, time

HEADER = 64
PORT = 5051
FORMAT = 'utf-8'
DC_MSG= "/disconnect"
SERVER = "192.168.86.30"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' *(HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

def receive(): # receives update from the server every 0.1s
    while True:
        time.sleep(0.1)
        print(client.recv(64).decode(FORMAT))

def start():
    client.connect(ADDR)#connect to the server
    print(f"connected to server {ADDR}.")
    print(f"use {DC_MSG} to disconnect.")
    print("\nSay Something...\n")

    thread = threading.Thread(target=receive)
    thread.start()

    run = True
    while run:
        msg = input()
        if(msg == DC_MSG):
            print("disconnected from server")
            thread.join()
            run = False

        send(msg)

start()
