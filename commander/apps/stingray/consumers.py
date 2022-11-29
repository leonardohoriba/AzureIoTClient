import json
import threading
import queue
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from src.helpers.socket_client import SocketClient

class StingrayConsumer(WebsocketConsumer):
    REFRESH_RATE = 1
    socket_client = SocketClient()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket_client = SocketClient()
        self._message_thread = None
        self._message_thread = threading.Thread(target=self.__message, name='message_thread')
        self.is_running = True
        # Data to plot graphs
        self.left_wheel_position = self.__queue_filled_with_zero(100)
        self.right_wheel_position = self.__queue_filled_with_zero(100)
        self.left_wheel_speed = self.__queue_filled_with_zero(100)
        self.right_wheel_speed = self.__queue_filled_with_zero(100)
        self.sonar_distance = self.__queue_filled_with_zero(100)

    def __queue_filled_with_zero(self, max: int):
        q = queue.Queue()
        for i in range(max):
            q.put(0)
        return q

    def __message(self):
        while self.is_running:
            data = self.socket_client.get_data()
            if data:
                body = data["body"]["body"]
                self.left_wheel_position.get()
                self.right_wheel_position.get()
                self.left_wheel_speed.get()
                self.right_wheel_speed.get()
                self.sonar_distance.get()
                self.left_wheel_position.put(round(body["leftWheelPosition"], 2))
                self.right_wheel_position.put(round(body["rightWheelPosition"], 2))
                self.left_wheel_speed.put(round(body["leftWheelSpeed"], 2))
                self.right_wheel_speed.put(round(body["rightWheelSpeed"], 2))
                self.sonar_distance.put(round(body["sonarDistance"], 2))
                data["body"]["body"]["queues"] = {
                    "leftWheelPosition": list(self.left_wheel_position.queue),
                    "rightWheelPosition": list(self.right_wheel_position.queue),
                    "leftWheelSpeed": list(self.left_wheel_speed.queue),
                    "rightWheelSpeed": list(self.right_wheel_speed.queue),
                    "sonarDistance": list(self.sonar_distance.queue),
                }
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
