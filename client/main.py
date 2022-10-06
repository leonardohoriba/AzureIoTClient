import threading
from queue import Empty
from time import sleep

import pigpio
from decouple import config

from src.components.Stingray import Stingray
from src.helpers.socket_client import SocketClient
from src.components.Camera import Camera

DEBUG_PID = bool(config("DEBUG_PID", default=False))
raspi = pigpio.pi()
robot = Stingray(raspi)
camera = Camera()
sleep(0.1)  # Must wait for the first frame to be captured before starting stream
camera.startStreaming()
client = SocketClient()
finished = False


def printSpeed():
    global finished
    global DEBUG_PID
    while not finished:
        # PID calibration doesn't need sonar and needs higher sample rate
        if not DEBUG_PID:
            # print(f"Distance: {robot.getSonarDistance()}")
            robot.triggerSonar()
        # client.send(
        #     {
        #         "leftWheelSpeed": robot.getLeftWheelSpeed(),
        #         "rightWheelSpeed": robot.getRightWheelSpeed(),
        #         "sonarDistance": robot.getSonarDistance(),
        #     }
        # )
        if DEBUG_PID:
            sleep(0.01)
        else:
            sleep(0.25)


robot.triggerSonar()
sleep(0.1)

robot.stop()
robot.setSonarAngle(0)
sleep(2)

threadSendTelemetry = threading.Thread(target=printSpeed, name="sendTelemetry")
threadSendTelemetry.start()

while True:
    try:
        instruction = client.getFromQueue()
    except Empty:
        sleep(0.01)
        continue
    if instruction["method_name"] == "setMovement":
        payload = instruction["payload"]
        robot.moveDistanceSpeed(
            payload["leftWheelDistance"],
            payload["leftWheelSpeed"],
            payload["rightWheelDistance"],
            payload["rightWheelSpeed"],
        )
        robot.waitUntilGoal()
    elif instruction["method_name"] == "disconnect":
        break

finished = True
threadSendTelemetry.join()
camera.deinit()
robot.deinit()
client.deinit()
del camera
del robot
del client
