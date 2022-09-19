import pigpio
from src.components.Stingray import Stingray
from time import sleep
import threading

raspi = pigpio.pi()
robot = Stingray(raspi)
finished = False

def printSpeed():
    global finished
    while not finished:
        print(f"Distance: {robot.getTotalDistance()} Speed: {robot.getSpeed()}")
        sleep(0.1)

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