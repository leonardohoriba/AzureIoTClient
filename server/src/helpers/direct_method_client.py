import json
import socket

from azure.iot.device import MethodResponse
from azure.iot.device.aio import IoTHubDeviceClient
from decouple import config


class DirectMethodClient:
    """
    Client to receive Direct Method from cloud and send to the socket client.
    """

    def __init__(self, socket: socket.socket) -> None:
        # Create an IoT Hub client
        self.socket = socket
        self.device_client = IoTHubDeviceClient.create_from_connection_string(
            config("CONNECTION_STRING")
        )

    # Define a method request handler
    async def __method_request_handler(self, method_request):
        # Define methods
        if method_request.name == "setMovement":
            try:
                # TODO error
                self.payload = method_request.payload
                # Send payload to socket client (robot)
                message = json.dumps(self.payload).encode(self.FORMAT)
                self.socket.send(message)

            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {
                    "Response": f"Executed direct method {method_request.name}"
                }
                response_status = 200
        else:
            response_payload = {
                "Response": f"Direct method {method_request.name} not defined"
            }
            response_status = 404

        method_response = MethodResponse.create_from_method_request(
            method_request, response_status, response_payload
        )
        await self.device_client.send_method_response(method_response)

    def getClient(self):
        try:
            # Attach the method request handler
            self.device_client.on_method_request_received = (
                self.__method_request_handler
            )
        except:
            # Clean up in the event of failure
            self.device_client.shutdown()
            raise

        return self.device_client
