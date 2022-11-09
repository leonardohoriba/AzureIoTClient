import threading
from time import sleep
from time import time
from decouple import config

from src.components.Encoder import Encoder

DEBUG_PID = bool(config("DEBUG_PID", default=False))


class Motor:
    def __init__(self, raspi, encoderInputPin, motorOutputPin):
        self._error = [0] * self._NUM_INTEGRAL_TERMS
        self._goalTheta = 0
        self._goalOmega = 0
        self._currentGoalTheta = 0
        self._finished = False
        self._moving = True
        self._raspi = raspi
        self._encoder = Encoder(raspi, encoderInputPin)
        self._motorOutputPin = motorOutputPin
        self._threadControl = threading.Thread(
            target=self.__control, name="control " + str(motorOutputPin)
        )
        self._threadSpeed = threading.Thread(
            target=self.__speed, name="speed " + str(motorOutputPin)
        )
        self._threadControl.start()
        self._threadSpeed.start()

    def deinit(self):
        self._finished = True
        self._threadControl.join()
        self._threadSpeed.join()
        self.__setPower(0)
        del self._encoder

    def __setPower(self, power):
        # power ranging from -100 to 100
        if power == 0:
            self._raspi.set_servo_pulsewidth(self._motorOutputPin, 1500)
        elif power > 0 and power <= 100:
            self._raspi.set_servo_pulsewidth(
                self._motorOutputPin, 1520 + power * 200 / 100
            )
        elif power > 100:
            self._raspi.set_servo_pulsewidth(self._motorOutputPin, 1720)
        elif power < 0 and power >= -100:
            self._raspi.set_servo_pulsewidth(
                self._motorOutputPin, 1480 + power * 200 / 100
            )
        elif power < -100:
            self._raspi.set_servo_pulsewidth(self._motorOutputPin, 1280)

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
        ierror = 0
        currentError = 0
        while not self._finished:
            freq = 100
            kp = 1.326 * -1
            ki = 1.2546 / -freq
            kd = 0.019635 * -freq

            lastTime = time()
            while time() - lastTime < 1 / freq:
                sleep(0.0001)

            lastError = currentError
            currentError = self._currentGoalTheta - self.getCurrentTheta()
            derror = currentError - lastError
            ierror += currentError
            if ierror < -100:
                ierror = -100
            elif ierror > 100:
                ierror = 100

            power = kp * currentError + ki * ierror + kd * derror
            # if self._motorOutputPin == 23:
            # print(f"error: {currentError}, ierror: {ierror}, derror:{derror}, power: {power}")
            if DEBUG_PID:
                # self.__setPower(self._goalOmega)
                self.__setPower(power)
            else:
                self.__setPower(power)

    def setGoal(self, theta, omega):
        # Omega in absolute value
        self._goalTheta = theta
        self._goalOmega = omega
        # Must set _moving to True here, because otherwise it would be set only in the next iteration of __speed
        self._moving = True

    def stop(self):
        self._goalTheta = self._currentGoalTheta
        return self._goalTheta

    def getCurrentTheta(self):
        return self._encoder.getCurrentTheta()

    def getCurrentOmega(self):
        return self._encoder.getCurrentOmega()

    def getMoving(self):
        return self._moving
