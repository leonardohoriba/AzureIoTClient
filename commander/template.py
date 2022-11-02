import time

from src.helpers.commander import Commander
from src.utils.direct_method_constants import DeviceID, MethodName

# Example
commander = Commander()

## Send direct method
# commander.iothub_devicemethod(
#     device_id=DeviceID.STINGRAY_29,
#     method_name=MethodName.SET_MOVEMENT,
#     payload={
#         "rightWheelSpeed": 10,
#         "rightWheelDistance": 20,
#         "leftWheelSpeed": 30,
#         "rightWheelDistance": 40,
#     },
# )

## Start listening telemetry from Azure Event Hub
commander.start()

## Get last telemetry from telemetry queue
while True:
    time.sleep(5)
    telemetry = commander.getTelemetry()

## Stop listening telemetry from Azure Event Hub
commander.stop()
