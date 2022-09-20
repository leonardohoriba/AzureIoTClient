import pigpio
from src.components.Motor import Motor
from math import pi

class Stingray():
    WHEEL_RADIUS = 56.5/2   # Measured in mm

    def __init__(self, raspi):
        self.leftMotor = Motor(raspi, 17, 23)
        self.rightMotor = Motor(raspi, 27, 24)

    def moveForward(self):
        self.leftMotor.setPower(50)
        self.rightMotor.setPower(-50)

    def moveRight(self):
        self.leftMotor.setPower(50)
        self.rightMotor.setPower(50)

    def stop(self):
        self.leftMotor.setPower(0)
        self.rightMotor.setPower(0)

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