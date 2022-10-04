import threading
from time import sleep

from src.components.Encoder import Encoder


class Motor:

    _NUM_INTEGRAL_TERMS = 20
    _error = [0] * _NUM_INTEGRAL_TERMS
    _goalTheta = 0
    _goalOmega = 0
    _currentGoalTheta = 0
    _finished = False
    _moving = True

    def __init__(self, raspi, encoderInputPin, motorOutputPin):
        self.raspi = raspi
        self.encoder = Encoder(raspi, encoderInputPin)
        self.motorOutputPin = motorOutputPin
        self.threadControl = threading.Thread(
            target=self.__control, name="control " + str(motorOutputPin)
        )
        self.threadSpeed = threading.Thread(
            target=self.__speed, name="speed " + str(motorOutputPin)
        )
        self.threadControl.start()
        self.threadSpeed.start()

    def deinit(self):
        self._finished = True
        self.threadControl.join()
        self.__setPower(0)
        del self.encoder

    def setGoal(self, theta, omega):
        # Omega in absolute value
        self._goalTheta = theta
        self._goalOmega = omega
        # Must set _moving to True here, because otherwise it would be set only in the next iteration of __speed
        self._moving = True

    def stop(self):
        self._goalTheta = self._currentGoalTheta

    def getCurrentTheta(self):
        return self.encoder.getCurrentTheta()

    def getCurrentOmega(self):
        return self.encoder.getCurrentOmega()

    def getMoving(self):
        return self._moving

    def __setPower(self, power):
        # power ranging from -100 to 100
        if power == 0:
            self.raspi.set_servo_pulsewidth(self.motorOutputPin, 1500)
        elif power > 0 and power <= 100:
            self.raspi.set_servo_pulsewidth(
                self.motorOutputPin, 1520 + power * 200 / 100
            )
        elif power > 100:
            self.raspi.set_servo_pulsewidth(self.motorOutputPin, 1720)
        elif power < 0 and power >= -100:
            self.raspi.set_servo_pulsewidth(
                self.motorOutputPin, 1480 + power * 200 / 100
            )
        elif power < -100:
            self.raspi.set_servo_pulsewidth(self.motorOutputPin, 1280)

    def __speed(self):
        while not self._finished:
            if self._goalTheta - self._currentGoalTheta > 1:
                # Moving forward
                self._moving = True
                self._currentGoalTheta += 1
            elif self._goalTheta - self._currentGoalTheta < -1:
                # Moving backwards
                self._moving = True
                self._currentGoalTheta -= 1
            else:
                # Between -1 and 1, we can consider the motor reached its goal
                self._moving = False
            # Bad implementation, imposees a minimum speed of 10
            if self._goalOmega > 10:
                sleep(1 / self._goalOmega)
            else:
                sleep(0.1)

    def __control(self):
        while not self._finished:
            kp = -1
            ki = 0
            kd = 0
            for i in range(self._NUM_INTEGRAL_TERMS - 1):
                self._error[i] = self._error[i + 1]
            self._error[self._NUM_INTEGRAL_TERMS - 1] = (
                self._currentGoalTheta - self.getCurrentTheta()
            )
            derror = (
                self._error[self._NUM_INTEGRAL_TERMS - 1]
                - self._error[self._NUM_INTEGRAL_TERMS - 2]
            )
            # Integrate the last _NUM_INTEGRAL_TERMS, decaying the weight linearly
            ierror = 0
            for i in range(self._NUM_INTEGRAL_TERMS):
                ierror += self._error[self._NUM_INTEGRAL_TERMS - (i + 1)] * (
                    1 - (i / self._NUM_INTEGRAL_TERMS)
                )
            power = (
                kp * self._error[self._NUM_INTEGRAL_TERMS - 1]
                + ki * ierror
                + kd * derror
            )
            self.__setPower(power)
            sleep(0.025)
