import pigpio
from math import pi

from src.components.Motor import Motor
from src.components.Sonar import Sonar

class Stingray():
    WHEEL_RADIUS = 56.5/2   # Measured in mm

    def __init__(self, raspi):
        self._raspi = raspi
        self.leftMotor = Motor(raspi, 17, 23)
        self.rightMotor = Motor(raspi, 27, 24)
        self.sonar = Sonar(raspi, 4, 18, 25)

    def deinit(self):
        self.leftMotor.deinit()
        self.rightMotor.deinit()
        self.sonar.deinit()
        del self.leftMotor
        del self.rightMotor
        del self.sonar
        self._raspi.stop()

    def moveToPosition(self, position, speed):
        self.leftMotor.setGoal(-position*360/(2*pi*self.WHEEL_RADIUS), speed*360/(2*pi*self.WHEEL_RADIUS))
        self.rightMotor.setGoal(position*360/(2*pi*self.WHEEL_RADIUS), speed*360/(2*pi*self.WHEEL_RADIUS))

    def moveForward(self):
        pass

    def moveRight(self):
        pass

    def stop(self):
        pass

    def getTotalDistance(self):
        return self.rightMotor.getCurrentTheta()*2*pi*self.WHEEL_RADIUS/360

    def getLeftWheelTotalDistance(self):
        return -self.leftMotor.getCurrentTheta()*2*pi*self.WHEEL_RADIUS/360

    def getRightWheelTotalDistance(self):
        return self.rightMotor.getCurrentTheta()*2*pi*self.WHEEL_RADIUS/360

    def getSpeed(self):
        # Maybe a mean of the two values?
        return self.rightMotor.getCurrentOmega()*2*pi*self.WHEEL_RADIUS/360

    def getLeftWheelSpeed(self):
        return -self.leftMotor.getCurrentOmega()*2*pi*self.WHEEL_RADIUS/360

    def getRightWheelSpeed(self):
        return self.rightMotor.getCurrentOmega()*2*pi*self.WHEEL_RADIUS/360

    def triggerSonar(self):
        self.sonar.trigger()

    def getSonarDistance(self):
        return self.sonar.getDistance()

    def setSonarAngle(self, angle):
        self.sonar.setAngle(angle)