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
    SERVER = settings.SOCKET_SERVER
    ADDR = (SERVER, PORT)

    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = queue.Queue()
        self.client_thread = threading.Thread(
            target=self.__handle_client, name="client_thread"
        )
        try:
            self.client.connect(self.ADDR)
            self.client_thread.start()
            print(f"[NEW CONNECTION] {self.ADDR}")
        except ConnectionRefusedError:
            print("Socket Server offline.")
            os._exit(1)

    def __handle_client(self):
        while True:
            try:
                msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    # Receive message from Client
                    msg = json.loads(self.client.recv(msg_length).decode(self.FORMAT))
                    print(f"Received:\n{msg}")
                    self.data.put(msg)
                elif msg_length == "":
                    print("Client disconnected.")
                    break
            except:
                break
        self.client.close()
        print(f"[DISCONNECTED] {self.client}.")

    def get_data(self):
        """Return the last data stored in the data received queue. If the queue is empty, return None."""
        try:
            data = self.data.get(block=False)
            return data
        except queue.Empty:
            return None

    # TODO Try to reconnect if server crashes.
