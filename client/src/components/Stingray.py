import pigpio
from math import pi

from src.components.Motor import Motor
from src.components.Sonar import Sonar

class Stingray():
    WHEEL_RADIUS = 56.5/2   # Measured in mm

    def __init__(self, raspi):
        self.leftMotor = Motor(raspi, 17, 23)
        self.rightMotor = Motor(raspi, 27, 24)
        self.sonar = Sonar(raspi, 4, 18)

    def moveToPosition(self, position):
        self.rightMotor.setGoalTheta(position)

    def moveForward(self):
        self.leftMotor.setSpeed(100)
        self.rightMotor.setSpeed(-100)

    def moveRight(self):
        self.leftMotor.setSpeed(100)
        self.rightMotor.setSpeed(100)

    def stop(self):
        self.leftMotor.setSpeed(0)
        self.rightMotor.setSpeed(0)

    def getTotalDistance(self):
        return self.rightMotor.getCurrentTheta()*2*pi*self.WHEEL_RADIUS/360

    def getLeftWheelTotalDistance(self):
        return -self.leftMotor.getCurrentTheta()*2*pi*self.WHEEL_RADIUS/360

    def getRightWheelTotalDistance(self):
        return self.rightMotor.getCurrentTheta()*2*pi*self.WHEEL_RADIUS/360

    def getSpeed(self):
        # Maybe a mean of the two values?
        return self.rightMotor.getCurrentSpeed()*2*pi*self.WHEEL_RADIUS/360

    def getLeftWheelSpeed(self):
        return -self.leftMotor.getCurrentSpeed()*2*pi*self.WHEEL_RADIUS/360

    def getRightWheelSpeed(self):
        return self.rightMotor.getCurrentSpeed()*2*pi*self.WHEEL_RADIUS/360

    def triggerSonar(self):
        self.sonar.trigger()

    def getSonarDistance(self):
        return self.sonar.getDistance()