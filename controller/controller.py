# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific HTTP endpoint on your IoT Hub.
import sys
# pylint: disable=E0611

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult
from decouple import config
from builtins import input
import json

# The service connection string to authenticate with your IoT hub.
# Using the Azure CLI:
# az iot hub show-connection-string --hub-name {your iot hub name} --policy-name service
AZURE_IOT_HUB_CONNECTION_STRING = config("AZURE_IOT_HUB_CONNECTION_STRING")
DEVICE_ID = "Stingray29"

# Details of the direct method to call.
METHOD_NAME = "setMovement"

def iothub_devicemethod_sample_run():
    try:
        # Create IoTHubRegistryManager
        registry_manager = IoTHubRegistryManager(AZURE_IOT_HUB_CONNECTION_STRING)

        # Call the direct method.
        payload = {
        "leftSpeed": 10, 
        "leftDistance": 20, 
        "rightSpeed": 30, 
        "rightDistance": 40
}

        encodedPayload = json.dumps(payload).encode("utf-8")
        deviceMethod = CloudToDeviceMethod(method_name=METHOD_NAME, payload=encodedPayload)
        response = registry_manager.invoke_device_method(DEVICE_ID, deviceMethod)

        print ( "" )
        print ( "Device Method called" )
        print ( "Device Method name       : {0}".format(METHOD_NAME) )
        print ( "Device Method payload    : {0}".format(deviceMethod) )
        print ( "" )
        print ( "Response status          : {0}".format(response.status) )
        print ( "Response payload         : {0}".format(response.payload) )

        input("Press Enter to continue...\n")

    except Exception as ex:
        print ( "" )
        print ( "Unexpected error {0}".format(ex) )
        return
    except KeyboardInterrupt:
        print ( "" )
        print ( "IoTHubDeviceMethod sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Python quickstart #2..." )

    iothub_devicemethod_sample_run()