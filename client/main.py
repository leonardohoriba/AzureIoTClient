import threading
from time import sleep

import pigpio
from decouple import config

from src.components.Stingray import Stingray
from src.helpers.socket_client import SocketClient

DEBUG_PID = config("DEBUG_PID", default=False)
raspi = pigpio.pi()
robot = Stingray(raspi)
client = SocketClient()
finished = False


def printSpeed():
    global finished
    while not finished:
        # PID calibration doesn't need sonar and needs higher sample rate
        if not DEBUG_PID:
            print(f"Distance: {robot.getSonarDistance()}")
            robot.triggerSonar()
        client.send(
            {
                "leftWheelSpeed": robot.getLeftWheelSpeed(),
                "rightWheelSpeed": robot.getRightWheelSpeed(),
                "sonarDistance": robot.getSonarDistance(),
            }
        )
        if DEBUG_PID:
            sleep(0.01)
        else:
            sleep(0.25)


robot.triggerSonar()
sleep(0.1)

threadPrintSpeed = threading.Thread(target=printSpeed)
threadPrintSpeed.start()
robot.stop()
robot.setSonarAngle(0)
sleep(2)
robot.movePositionSpeed(300, 200, 300, 200)
sleep(5)
robot.movePositionSpeed(0, 100, 0, 100)
sleep(5)
finished = True
threadPrintSpeed.join()
robot.deinit()
del robot
