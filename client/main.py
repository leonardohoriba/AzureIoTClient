import pigpio
from src.components.Stingray import Stingray
from time import sleep
import threading

from src.helpers.socket_client import SocketClient

raspi = pigpio.pi()
robot = Stingray(raspi)
client = SocketClient()
finished = False

def printSpeed():
    global finished
    while not finished:
        print(f"Distance: {robot.getTotalDistance()} LeftSpeed: {robot.getLeftWheelSpeed()}  RightSpeed: {robot.getRightWheelSpeed()}")
        client.send({
            "LeftWheelSpeed": robot.getLeftWheelSpeed(),
            "RightWheelSpeed": robot.getRightWheelSpeed()
        })
        sleep(0.25)

threadPrintSpeed = threading.Thread(target=printSpeed)
threadPrintSpeed.start()

sleep(5)
robot.moveForward()
sleep(5)
robot.moveRight()
sleep(5)
robot.moveForward()
sleep(5)
robot.stop()
sleep(5)
finished = True
threadPrintSpeed.join()