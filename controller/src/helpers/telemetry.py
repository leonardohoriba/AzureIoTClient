from azure.eventhub import TransportType
from azure.eventhub import EventHubConsumerClient  # This is async API. For sync API, remove ".aio" 
import logging
from decouple import config


client = EventHubConsumerClient.from_connection_string(
    conn_str=config("AZURE_IOT_EVENT_HUB_ENDPOINT"),
    consumer_group="$default",
    transport_type=TransportType.AmqpOverWebsocket,
    # http_proxy={
    #     'proxy_hostname': '<proxy host>',
    #     'proxy_port': 3128, 
    #     'username': '<proxy user name>',
    #     'password': '<proxy password>'
    # }
)
partition_ids = client.get_partition_ids()

def on_event(partition_context, event):
    print(event.body_as_json())
    event_body = event.body_as_json()
    device_id = event.system_properties["iothub-connection-device-id".encode()].decode()
    partition_context.update_checkpoint(event)

with client:
    client.receive(
        on_event=on_event,
        starting_position=partition_ids[-1],  # "-1" is from the beginning of the partition.
        # starting_position="-1",  # "-1" is from the beginning of the partition.
    )
    # receive events from specified partition:
    # client.receive(on_event=on_event, partition_id='0')
pass