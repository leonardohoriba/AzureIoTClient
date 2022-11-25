import json
import threading
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from src.helpers.socket_client import SocketClient

class StingrayConsumer(WebsocketConsumer):
    REFRESH_RATE = 1
    # socket_client = SocketClient()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket_client = SocketClient()
        self._message_thread = None
        self._message_thread = threading.Thread(target=self.__message, name='message_thread')
        self.is_running = True

    def __message(self):
        while self.is_running:
            data = self.socket_client.get_data()
            if data:
                self.send(text_data=json.dumps(data))

    def connect(self):
        self.room_group_name = "test"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        self._message_thread.start()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.is_running = False
        self.socket_client.client.close()
        print("DISCONNECT CODE: ",code)
