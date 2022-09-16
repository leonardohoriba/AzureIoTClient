import asyncio
import json
import signal
import socket
import os
import threading

from decouple import config

import settings
from src.helpers.azure_client import azure_client
from src.helpers.signal_handler import signal_handler


class StingrayDaemon:
    '''Socket Server'''
    HEADER = settings.HEADER
    PORT = settings.PORT
    SERVER = settings.SERVER
    ADDR = (SERVER, PORT)
    FORMAT = settings.FORMAT

    def __init__(self, device_scope, device_id, device_key) -> None:
        self.device_scope = device_scope
        self.device_id = device_id
        self.device_key = device_key
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        # Connect to Azure IoT Platform
        self.device_client = self.__start_connection()

    def __start_connection(self):
        """Function that calls the Azure Client coroutine"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            device_client = loop.run_until_complete(
                azure_client(self.device_scope, self.device_id, self.device_key)
            )
        except:
            # Run the service without Internet
            print("Failed to connect to Azure")
            os._exit(1)
        loop.close()
        return device_client

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
                    # Send message to Azure
                    # TODO Check this function if internet shuts down
                    await self.device_client.send_message(json.dumps(msg))
                    # await asyncio.sleep(settings.WAIT_TIME)
            except:
                break
        conn.close()
        print(f"[DISCONNECTED] {addr}.")

    def __call_client(self, conn, addr):
        """Function that calls the socket service coroutine"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.__handle_client(conn, addr))
        loop.close()

    def start(self):
        print("[STARTING] server is starting...")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()
            print(f"[NEW CONNECTION] {addr} connected.")
            thread = threading.Thread(target=self.__call_client, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    # Daemon SIGTERM
    signal.signal(signal.SIGTERM, signal_handler)

    # Start socket server
    StingrayDaemon(
        device_scope=config("SCOPE_ID"),
        device_id=config("DEVICE_ID"),
        device_key=config("DEVICE_KEY"),
    ).start()
