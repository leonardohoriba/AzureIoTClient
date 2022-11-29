from math import pi
from time import sleep, time

from src.helpers.commander import Commander
from src.utils.direct_method_constants import DeviceID, MethodName


class StingrayCommander:
    ROBOT_RADIUS = 205  # millimeters

    def __init__(self, commander: Commander, robotNumber: int):
        self._commander = commander
        self._deviceID = DeviceID.getDeviceIdFromNumber(robotNumber)
        self.telemetryStarted = False
        self._state = {
            "instructionID": -1,
            "leftWheelSpeed": 0,
            "rightWheelSpeed": 0,
        }
        self._lastTime = time()

    def telemetryCallback(self, telemetryBody):
        if telemetryBody["dataType"] == "telemetry":
            currentTime = time()
            self._state = {"timeDelta": currentTime - self._lastTime} | telemetryBody[
                "body"
            ]
            self._lastTime = currentTime
            print(self._state)

    def getState(self):
        return self._state

    def turn(self, angle: float, angularSpeed: float, radius: float):
        self._commander.iothub_devicemethod(
            device_id=self._deviceID,
            method_name=MethodName.SET_MOVEMENT,
            payload={
                "instructionID": 2,
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

    def turnUntilObjectFound(self, angle: float, angularSpeed: float, radius: float, objectName: str):
        self._commander.iothub_devicemethod(
            device_id=self._deviceID,
            method_name=MethodName.MOVE_UNTIL_OBJECT_FOUND,
            payload={
                "instructionID": 2,
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
                "object": objectName
            },
        )

    def move(self, distance: float, speed: float):
        self._commander.iothub_devicemethod(
            device_id=self._deviceID,
            method_name=MethodName.SET_MOVEMENT,
            payload={
                "instructionID": 4,
                "rightWheelSpeed": abs(speed),
                "rightWheelDistance": distance,
                "leftWheelSpeed": abs(speed),
                "leftWheelDistance": distance,
            },
        )

    def moveUntilObjectFound(self, distance: float, speed: float, objectName: str):
        self._commander.iothub_devicemethod(
            device_id=self._deviceID,
            method_name=MethodName.MOVE_UNTIL_OBJECT_FOUND,
            payload={
                "instructionID": 5,
                "rightWheelSpeed": abs(speed),
                "rightWheelDistance": distance,
                "leftWheelSpeed": abs(speed),
                "leftWheelDistance": distance,
                "object:": objectName,
            },
        )

    def moveUntilObstacleFound(self, distance: float, speed: float, obstacleDistance: float):
        self._commander.iothub_devicemethod(
            device_id=self._deviceID,
            method_name=MethodName.MOVE_UNTIL_OBSTACLE_FOUND,
            payload={
                "instructionID": 5,
                "rightWheelSpeed": abs(speed),
                "rightWheelDistance": distance,
                "leftWheelSpeed": abs(speed),
                "leftWheelDistance": distance,
                "obstacle_distance": obstacleDistance,
            },
        )

    def flush(self):
        self._commander.iothub_devicemethod(
            device_id=self._deviceID,
            method_name=MethodName.FLUSH,
            payload={
                "instructionID": 1,
            },
        )

    def stopForTime(self, time: float):
        self._commander.iothub_devicemethod(
            device_id=self._deviceID,
            method_name=MethodName.STOP_FOR_TIME,
            payload={
                "instructionID": 3,
                "time": time,
            },
        )

    def waitUntilExecutingInstruction(self, instructionID: int):
        while self._state["instructionID"] != instructionID:
            sleep(0.001)
            continue
