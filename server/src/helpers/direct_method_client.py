import json
import socket
from ast import literal_eval

from azure.iot.device import MethodResponse

import settings


class DirectMethodClient:
    """
    Client to receive Direct Method from cloud and send to the socket client.
    """

    def __init__(self, device_client) -> None:
        self.conn = None
        # Create an IoT Hub client
        self.device_client = device_client
        # Listen direct methods
        self.device_client = self.__start_direct_method()

    def __start_direct_method(self):
        try:
            # Attach the method request handler
            self.device_client.on_method_request_received = (
                self.__method_request_handler
            )
        except:
            # Clean up in the event of failure
            print("[Error] Failed to start the direct method.")

        return self.device_client

    # Define a method request handler
    async def __method_request_handler(self, method_request):
        # Define methods
        if method_request.name == "setMovement":
            try:
                self.payload = method_request.payload
                msg = json.loads(literal_eval(self.payload))
                print(f"Direct Message:\n{msg}")
                # Send payload to socket client (robot)
                if self.conn:
                    self.__socket_send_message(msg)
                else:
                    print("[Error] Set a socket connection in DirectMethodClient.")
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

    def setSocketConnection(self, conn: socket.socket):
        self.conn = conn

    def __socket_send_message(self, msg: dict) -> None:
        """Function to send a json message to Socket"""
        message = json.dumps(msg).encode(settings.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(settings.FORMAT)
        send_length += b" " * (settings.HEADER - len(send_length))
        try:
            self.conn.send(send_length)
            self.conn.send(message)
        except ConnectionResetError:
            # Socket Server (Stingrayd) goes down.
            print("Lost direct method connection to socket.")
            self.conn = None
            print("[CONNECTION CLOSED] Direct method socket.")
        except Exception as ex:
            print(ex)
