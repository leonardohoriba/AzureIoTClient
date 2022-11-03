from math import pi
from time import sleep

from src.helpers.commander import Commander
from src.utils.direct_method_constants import DeviceID, MethodName


class StingrayCommander:
    ROBOT_RADIUS = 204  # millimeters

    def __init__(self, commander: Commander, robotNumber: int):
        self._commander = commander
        self._deviceID = DeviceID.getDeviceIdFromNumber(robotNumber)
        self.telemetryStarted = False
        self._state = {
            "instructionID": -1,
        }

    def telemetryCallback(self, telemetryBody):
        if telemetryBody["dataType"] == "telemetry":
            self._state = telemetryBody["body"]

    def turn(self, angle: float, angularSpeed: float, radius: float):
        self._commander.iothub_devicemethod(
            device_id=self._deviceID,
            method_name=MethodName.SET_MOVEMENT,
            payload={
                "instructionID": 1,
                "rightWheelSpeed": abs(
                    angularSpeed * (2 * pi / 360) * (radius - self.ROBOT_RADIUS / 2)
                ),
                "rightWheelDistance": angle
                * (2 * pi / 360)
                * (radius - self.ROBOT_RADIUS / 2),
                "leftWheelSpeed": abs(
                    angularSpeed * (2 * pi / 360) * (radius + self.ROBOT_RADIUS / 2)
                ),
                "leftWheelDistance": angle
                * (2 * pi / 360)
                * (radius + self.ROBOT_RADIUS / 2),
            },
        )

    def waitUntilExecutingInstruction(self, instructionID: int):
        while self._state["instructionID"] != instructionID:
            sleep(0.001)
            continue
