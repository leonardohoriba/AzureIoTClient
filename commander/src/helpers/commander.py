import json

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod
from decouple import config

from src.helpers.eventhub_telemetry import EventHubTelemetry


class Commander(EventHubTelemetry):
    def __init__(self) -> None:
        super().__init__()
        # Create IoTHubRegistryManager
        self.registry_manager = IoTHubRegistryManager(
            config("AZURE_IOT_HUB_CONNECTION_STRING")
        )

    def iothub_devicemethod(self, device_id, method_name, payload):
        try:
            self.socket.send_all({
                "methodName": method_name,
                "payload": payload,
            })
            encodedPayload = json.dumps(payload).encode("utf-8")
            # Create the direct method.
            deviceMethod = CloudToDeviceMethod(
                method_name=method_name, payload=encodedPayload
            )
            # Call the direct method.
            response = self.registry_manager.invoke_device_method(
                device_id, deviceMethod
            )
            print(
                f"Response: {{'status': {response.status}, 'payload': {response.payload}}}"
            )

        except Exception as ex:
            print(ex)
