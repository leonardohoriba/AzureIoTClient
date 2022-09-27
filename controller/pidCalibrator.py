import asyncio
import json
import socket

from decouple import config

class StingrayDaemon:
    """Socket Server"""

    HEADER = 64
    PORT = 2323
    SERVER = "0.0.0.0"
    ADDR = (SERVER, PORT)
    FORMAT = "utf-8"

    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def __del__(self):
        self.loop.close()
        self.server.close()

    async def __handle_client(self, conn, addr):
        """Receive a json message from Client and send to Azure IoT Central"""
        while True:
            try:
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    # Receive message from Client
                    msg = json.loads(conn.recv(msg_length).decode(self.FORMAT))
                    print(f"Sending data:\n{msg}")
                elif msg_length == '':
                    print("Client disconnected.")
                    break
            except:
                break
        conn.close()
        print(f"[DISCONNECTED] {addr}.")

    def __call_client(self, conn, addr):
        """Function that calls the socket service coroutine"""
        self.loop.run_until_complete(self.__handle_client(conn, addr))

    def start(self):
        print("[STARTING] server is starting...")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()
            print(f"[NEW CONNECTION] {addr} connected.")
            self.__call_client(conn, addr)


if __name__ == "__main__":

    # Start socket server
    StingrayDaemon().start()
