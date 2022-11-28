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
        self._threadSocketServer = threading.Thread(target=self.__socketServer, name="socketServer")
        self._threadSocketServer.start()
        self.client_list = []
        self._interfaceButtons = {
            "start_button": False,
            "stop_button": False,
        }

    def __socketServer(self):
        print("[STARTING] server is starting...")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()
            self.client_list.append((conn, addr))
            print(f"[NEW CONNECTION] {addr} connected.")
            threading.Thread(target=self.__socketReceive, name="socketReceive", args=(conn, addr)).start()

    def __socketReceive(self, conn, addr):
        while True:
            try:
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    # Receive message from Stingrayd
                    message = conn.recv(msg_length).decode(self.FORMAT)
                    if "start_button" in message:
                        self._interfaceButtons["start_button"] = message["start_button"]
                    if "stop_button" in message:
                        self._interfaceButtons["stop_button"] = message["stop_button"]
                elif msg_length == "":
                    print("Interface disconnected.")
                    break
            except ConnectionResetError:
                print(f"[CONNECTION CLOSED] {addr}")
                break
            except Exception as ex:
                print(ex)

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

    def receive_all(self):
        interfaceButtonsLatch = self._interfaceButtons
        self._interfaceButtons = {
            "start_button": False,
            "stop_button": False,
        }
        return interfaceButtonsLatch