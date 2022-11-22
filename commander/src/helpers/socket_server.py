import json
import socket
import threading

import settings


class SocketServer:
    """Socket Server"""

    HEADER = settings.HEADER
    PORT = settings.PORT
    SERVER = settings.SOCKET_SERVER
    ADDR = (SERVER, PORT)
    FORMAT = settings.FORMAT

    def __init__(self) -> None:
        # Server configuration
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        # Start listening clients
        self._start_thread = threading.Thread(target=self.__start, name="start_thread")
        self._start_thread.start()
        self.client_list = []

    def __start(self):
        print("[STARTING] server is starting...")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()
            self.client_list.append((conn, addr))
            print(f"[NEW CONNECTION] {addr} connected.")

    def send_all(self, msg: dict) -> None:
        """Function to send a json message to Sockets"""
        message = json.dumps(msg).encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b" " * (self.HEADER - len(send_length))
        for cl in self.client_list:
            try:
                cl[0].send(send_length)
                cl[0].send(message)
            except ConnectionResetError:
                self.client_list.remove(cl)
                print(f"[CONNECTION CLOSED] {cl[1]}")
            except:
                try:
                    self._start_thread = threading.Thread(
                        target=self.__start, name="start_thread"
                    )
                    self._start_thread.start()
                except:
                    pass
