import threading
from queue import Empty
from time import sleep
from time import time

import pigpio
from decouple import config

import settings
from src.components.Stingray import Stingray
from src.helpers.socket_client import SocketClient

DEBUG_PID = bool(config("DEBUG_PID", default=False))
raspi = pigpio.pi()
robot = Stingray(raspi)
sleep(1.5)  # Wait for the wheel to settle
client = SocketClient()
finished = False


def sendTelemetry():
    client.send(
        {
            "dataType": "deviceEvent",
            "deviceName": settings.ROBOT_NAME,
            "body": {
                "eventName": "init",
                "timestamp": time(),
            },
        }
    )
    while not finished:

        client.send(
            {
                "dataType": "telemetry",
                "deviceName": settings.ROBOT_NAME,
                "body": {
                    "instructionID": robot.getInstructionID(),
                    "leftWheelSpeed": robot.getLeftWheelSpeed(),
                    "rightWheelSpeed": robot.getRightWheelSpeed(),
                    "sonarDistance": robot.getSonarDistance(),
                    "detectedObjectList": robot.objectsOnCamera(),
                },
            }
        )
        # PID calibration doesn't need sonar and needs higher sample rate
        if DEBUG_PID:
            sleep(0.01)
        else:
            robot.triggerSonar()
            sleep(1)

    client.send(
        {
            "dataType": "deviceEvent",
            "deviceName": settings.ROBOT_NAME,
            "body": {
                "eventName": "deinit",
                "timestamp": time(),
            },
        }
    )


def main():
    global raspi
    global robot
    global client
    global finished
    robot.triggerSonar()
    sleep(0.1)

    robot.stop()
    robot.setSonarAngle(0)
    sleep(2)

    threadSendTelemetry = threading.Thread(target=sendTelemetry, name="sendTelemetry")
    threadSendTelemetry.start()

    while True:
        try:
            instruction = client.getFromQueue()
        except Empty:
            robot.setInstructionID(0)
            sleep(0.001)
            continue
        methodName = instruction["method_name"]
        payload = instruction["payload"]
        robot.setInstructionID(payload["instructionID"])
        if methodName == "disconnect":
            break
        elif methodName == "setMovement":
            robot.moveDistanceSpeed(
                payload["leftWheelDistance"],
                payload["leftWheelSpeed"],
                payload["rightWheelDistance"],
                payload["rightWheelSpeed"],
            )
            robot.waitUntilGoal()
        elif methodName == "stopForTime":
            sleep(payload["time"])
        elif methodName == "moveUntilObjectFound":
            robot.moveDistanceSpeed(
                payload["leftWheelDistance"],
                payload["leftWheelSpeed"],
                payload["rightWheelDistance"],
                payload["rightWheelSpeed"],
            )
            robot.waitUntilObject(payload["object"])
            robot.stop()

    finished = True
    threadSendTelemetry.join()


if __name__ == "__main__":
    main()
    robot.deinit()
    client.deinit()
    del robot
    del client
    print(
        "---------------------------------------finished---------------------------------------"
    )
