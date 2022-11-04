from math import pi
from time import sleep
from time import time

import pigpio

from src.components.Motor import Motor
from src.components.NeuralNetwork.NeuralNetwork import NeuralNetwork
from src.components.Sonar import Sonar


class Stingray:
    WHEEL_RADIUS = 56.5 / 2  # Measured in mm

    def __init__(self, raspi: pigpio.pi):
        self._raspi = raspi
        self._flushed = False
        self.leftMotor = Motor(raspi, 17, 23)
        self.rightMotor = Motor(raspi, 27, 24)
        self.sonar = Sonar(raspi, 4, 18, 25)
        self.neuralnetwork = NeuralNetwork()
        self.neuralnetwork.startStreaming()
        self.leftPosition = 0
        self.rightPosition = 0
        self._instructionID = 0

    def deinit(self):
        self.leftMotor.deinit()
        self.rightMotor.deinit()
        self.sonar.deinit()
        self.neuralnetwork.deinit()
        del self.leftMotor
        del self.rightMotor
        del self.sonar
        del self.neuralnetwork
        self._raspi.stop()

    def flushCallback(self):
        self._flushed = True
        self.stop()

    def stopForTime(self, stopTime):
        startTime = int(time())
        while (time() - startTime < stopTime) and not self._flushed:
            sleep(0.001)
        self._flushed = False

    def moveDistanceSpeed(self, leftDistance, leftSpeed, rightDistance, rightSpeed):
        self.movePositionSpeed(
            self.leftPosition + leftDistance,
            leftSpeed,
            self.rightPosition + rightDistance,
            rightSpeed,
        )

    def movePositionSpeed(self, leftPosition, leftSpeed, rightPosition, rightSpeed):
        # Non-blocking function
        # Motors mirrored, so one of them must go backwards
        self.leftPosition = leftPosition
        self.leftMotor.setGoal(
            -leftPosition * 360 / (2 * pi * self.WHEEL_RADIUS),
            leftSpeed * 360 / (2 * pi * self.WHEEL_RADIUS),
        )
        self.rightPosition = rightPosition
        self.rightMotor.setGoal(
            rightPosition * 360 / (2 * pi * self.WHEEL_RADIUS),
            rightSpeed * 360 / (2 * pi * self.WHEEL_RADIUS),
        )

    def objectsOnCamera(self):
        return self.neuralnetwork.getObjectList()

    def waitUntilObject(self, object: str):
        while (object not in [obj["name"] for obj in self.objectsOnCamera()]) and (
            self.leftMotor.getMoving() or self.rightMotor.getMoving()
        ):
            sleep(0.01)

    def stop(self):
        # One of the motors must have a negative angle, because they are mirrored
        self.leftPosition = -self.leftMotor.stop() * 2 * pi * self.WHEEL_RADIUS / 360
        self.rightPosition = self.rightMotor.stop() * 2 * pi * self.WHEEL_RADIUS / 360

    def waitUntilGoal(self):
        while self.leftMotor.getMoving() or self.rightMotor.getMoving():
            sleep(0.01)

    def getTotalDistance(self):
        return self.rightMotor.getCurrentTheta() * 2 * pi * self.WHEEL_RADIUS / 360

    def getLeftWheelTotalDistance(self):
        return -self.leftMotor.getCurrentTheta() * 2 * pi * self.WHEEL_RADIUS / 360

    def getRightWheelTotalDistance(self):
        return self.rightMotor.getCurrentTheta() * 2 * pi * self.WHEEL_RADIUS / 360

    def getSpeed(self):
        # Maybe a mean of the two values?
        return self.rightMotor.getCurrentOmega() * 2 * pi * self.WHEEL_RADIUS / 360

    def getLeftWheelSpeed(self):
        return -self.leftMotor.getCurrentOmega() * 2 * pi * self.WHEEL_RADIUS / 360

    def getRightWheelSpeed(self):
        return self.rightMotor.getCurrentOmega() * 2 * pi * self.WHEEL_RADIUS / 360

    def setInstructionID(self, id: int):
        self._instructionID = id

    def getInstructionID(self) -> int:
        return self._instructionID

    def triggerSonar(self):
        self.sonar.trigger()

    def getSonarDistance(self):
        return self.sonar.getDistance()

    def setSonarAngle(self, angle):
        self.sonar.setAngle(angle)
