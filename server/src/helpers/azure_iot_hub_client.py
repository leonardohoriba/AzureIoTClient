from azure.iot.device.aio import IoTHubDeviceClient
from decouple import config


async def iot_hub_client():
    # Connect
    device_client = IoTHubDeviceClient.create_from_connection_string(
        config("CONNECTION_STRING")
    )
    await device_client.connect()
    return device_client
