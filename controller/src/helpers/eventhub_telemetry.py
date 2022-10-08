import queue
import threading

from azure.eventhub import EventHubConsumerClient, TransportType
from decouple import config


class EventHubTelemetry:
    """
    Class to receive telemetry from Azure IoT Hub devices
    """

    def __init__(self) -> None:
        self.eventhub_client = EventHubConsumerClient.from_connection_string(
            conn_str=config("AZURE_IOT_EVENT_HUB_ENDPOINT", default=""),
            consumer_group="$default",
            transport_type=TransportType.AmqpOverWebsocket,
        )
        # self.partition_ids = self.eventhub_client.get_partition_ids()
        self.telemetry = queue.Queue()
        self.stop_thread = False

    def __on_event(self, partition_context, event):
        data = {
            "device_id": event.system_properties[
                "iothub-connection-device-id".encode()
            ].decode(),
            "body": event.body_as_json(),
        }
        self.eventhub_client.close()
        self.telemetry.put(data)
        print(data)
        # partition_context.update_checkpoint(event)

    def __listen(self):
        print("start thread")
        while not self.stop_thread:
            with self.eventhub_client:
                self.eventhub_client.receive(
                    on_event=self.__on_event,
                    max_wait_time=1,  # time in seconds
                    starting_position="-1",  # "-1" is from the beginning of the partition.
                    # partition_id=partition_ids[-1], # receive events from specified partition
                )

    def start(self):
        self._thread = threading.Thread(target=self.__listen, name=self.__listen.__name__)
        self._thread.start()

    def stop(self):
        self.stop_thread = True

    def getTelemetry(self):
        return self.telemetry.get(block=False)
