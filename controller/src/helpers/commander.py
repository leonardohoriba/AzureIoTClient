import json

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod
from decouple import config


class Commander:
    def __init__(self) -> None:
        # Create IoTHubRegistryManager
        self.registry_manager = IoTHubRegistryManager(
            config("AZURE_IOT_HUB_CONNECTION_STRING")
        )

    def iothub_devicemethod(self, device_id, method_name, payload):
        try:
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
