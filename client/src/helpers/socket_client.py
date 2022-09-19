import socket
import os
import json

import settings


class SocketClient:
    HEADER = settings.HEADER
    PORT = settings.PORT
    FORMAT = settings.FORMAT
    SERVER = settings.SERVER
    ADDR = (SERVER, PORT)

    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(self.ADDR)
            print(f"[NEW CONNECTION] {self.ADDR}")
        except ConnectionRefusedError:
            # Socket Server (Stingrayd) is offline when SocketClient starts.
            print("Socket Server offline.")
            os._exit(1)

    def send(self, msg: dict) -> None:
        """Function to send a json message to Azure IoT Central"""
        message = json.dumps(msg).encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b" " * (self.HEADER - len(send_length))
        try:
            self.client.send(send_length)
            self.client.send(message)
        except ConnectionResetError:
            # Socket Server (Stingrayd) goes down.
            print("Lost connection to socket server (Stingrayd).")
            self.client.close()
            print("[CONNECTION CLOSED]")
        except:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect(self.ADDR)
                print(f"[NEW CONNECTION] {self.ADDR}")
            except:
                pass
