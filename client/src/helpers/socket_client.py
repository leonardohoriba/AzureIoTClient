import json
import os
import queue
import socket
import threading

import settings


class SocketClient:
    HEADER = settings.HEADER
    PORT = settings.PORT
    FORMAT = settings.FORMAT
    SERVER = settings.SERVER
    ADDR = (SERVER, PORT)

    _finished = False

    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.direct_method = queue.Queue()
        try:
            self.client.connect(self.ADDR)
            self.threadDirectMethod = threading.Thread(
                target=self.__listen_stingrayd,
                args=(self.client, self.ADDR),
                name="directMethod",
            )
            self.threadDirectMethod.start()
            # self.__listen_stingrayd(self.client, self.ADDR)
            print(f"[NEW CONNECTION] {self.ADDR}")
        except ConnectionRefusedError:
            # Socket Server (Stingrayd) is offline when SocketClient starts.
            print("Socket Server offline.")
            os._exit(1)

    def deinit(self):
        self._finished = True
        self.client.shutdown(socket.SHUT_RDWR)
        self.threadDirectMethod.join()

    def __listen_stingrayd(self, conn, addr):
        """Receive a direct method from stingrayd."""
        while not self._finished:
            try:
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    # Receive message from Stingrayd
                    message = conn.recv(msg_length).decode(self.FORMAT)
                    msg = json.loads(message)
                    print(f"Direct method received:\n{msg}")
                    # Put message in direct method queue
                    self.direct_method.put(msg)
                elif msg_length == "":
                    print("Stingrayd disconnected.")
                    break
            except:
                break
        conn.close()
        print(f"[Error] Stingrayd disconnected: {addr}.")

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
            # Socket Server (Stingrayd) goes down.
            print("Lost connection to socket server (Stingrayd).")
            self.client.close()
            print("[CONNECTION CLOSED]")
        except:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect(self.ADDR)
                self.__listen_stingrayd(self.client, self.ADDR)
                print(f"[NEW CONNECTION] {self.ADDR}")
            except:
                pass
