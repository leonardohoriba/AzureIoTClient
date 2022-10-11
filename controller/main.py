import time

from helpers.commander import Commander
from src.utils.direct_method_constants import DeviceID, MethodName


# Example
controller = Commander()

## Send direct method
controller.iothub_devicemethod(
    device_id=DeviceID.STINGRAY_29,
    method_name=MethodName.SET_MOVEMENT,
    payload={
        "rightWheelSpeed": 10,
        "rightWheelDistance": 20,
        "leftWheelSpeed": 30,
        "rightWheelDistance": 40,
    },
)

## Start listening telemetry from Azure Event Hub
controller.start()

## Get last telemetry from telemetry queue
while(True):
    time.sleep(5)
    telemetry = controller.getTelemetry()

## Stop listening telemetry from Azure Event Hub
controller.stop()