from decouple import config
from azure.iot.device.aio import IoTHubDeviceClient


async def iot_hub_client():
    # Connect
    device_client = IoTHubDeviceClient.create_from_connection_string(config("CONNECTION_STRING"))
    await device_client.connect()
    return device_client
