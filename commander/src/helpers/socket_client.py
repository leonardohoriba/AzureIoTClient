import json
import os
import socket

import settings


class SocketClient:
    HEADER = settings.HEADER
    PORT = settings.PORT
    FORMAT = settings.FORMAT
    SERVER = settings.SOCKET_SERVER
    ADDR = (SERVER, PORT)

    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(self.ADDR)
            print(f"[NEW CONNECTION] {self.ADDR}")
        except ConnectionRefusedError:
            print("Socket Server offline.")
            os._exit(1)

    def send(self, msg: dict) -> None:
        """Function to send a json message to Socket Server"""
        message = json.dumps(msg).encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b" " * (self.HEADER - len(send_length))
        try:
            self.client.send(send_length)
            self.client.send(message)
        except ConnectionResetError:
            print("Lost connection to socket server.")
            self.client.close()
            print("[CONNECTION CLOSED]")
        except:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect(self.ADDR)
                print(f"[NEW CONNECTION] {self.ADDR}")
            except:
                pass
