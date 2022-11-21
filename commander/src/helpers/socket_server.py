import json
import socket
import threading

from decouple import config

import settings


class SocketServer:
    """Socket Server"""

    HEADER = settings.HEADER
    PORT = settings.PORT
    SERVER = settings.SOCKET_SERVER
    ADDR = (SERVER, PORT)
    FORMAT = settings.FORMAT

    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

    def __handle_client(self, conn, addr):
        while True:
            try:
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    # Receive message from Client
                    msg = json.loads(conn.recv(msg_length).decode(self.FORMAT))
                    print(f"Received:\n{msg}")
                elif msg_length == "":
                    print("Client disconnected.")
                    break
            except:
                break
        conn.close()
        print(f"[DISCONNECTED] {addr}.")

    def start(self):
        print("[STARTING] server is starting...")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()
            threading.Thread(
                target=self.__handle_client,
                args=(conn, addr),
                daemon=True,
                name=f"thread_{conn}",
            ).start()
            print(f"[NEW CONNECTION] {addr} connected.")
