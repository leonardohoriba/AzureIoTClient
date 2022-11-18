import datetime
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
        self.partition_ids = self.eventhub_client.get_partition_ids()
        self.telemetry = queue.Queue()

    def __on_event(self, partition_context, event):
        if event:
            # Condition for not send old message stored in Azure Event Hub
            now = datetime.datetime.now(datetime.timezone.utc)
            delta = now - event.enqueued_time
            print(delta)
            if delta < datetime.timedelta(seconds=5):
                data = {
                    "deviceID": event.system_properties[
                        "iothub-connection-device-id".encode()
                    ].decode(),
                    "delta": delta,
                    "body": event.body_as_json(),
                }
                self.telemetry.put(data)
                # print(data["body"])
                # partition_context.update_checkpoint(event)

    def __listen(self):
        print("Listening telemetry from Azure IoT Event Hub...")
        with self.eventhub_client:
            self.eventhub_client.receive(
                on_event=self.__on_event,
                max_wait_time=1,  # time in seconds
                starting_position=datetime.datetime.now(
                    datetime.timezone.utc
                ),  # "-1" is from the beginning of the partition.
                # partition_id=self.partition_ids[-1], # receive events from specified partition
            )

    def start(self):
        """Start listening Azure Event Hub telemetry."""
        self._thread = threading.Thread(
            target=self.__listen, name=self.__listen.__name__
        )
        self._thread.start()

    def stop(self):
        """Stop listening Azure Event Hub telemetry."""
        self.eventhub_client.close()

    def getTelemetry(self):
        """Return the last telemetry stored in the telemetry received queue. If the queue is empty, return None."""
        try:
            telemetry = self.telemetry.get(block=False)
            return telemetry
        except queue.Empty:
            return None
