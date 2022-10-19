import queue
import time

import pigpio


class Encoder:
    """
    More information in Parallax Feedback 360 Servo Datasheet
    PWM_FREQ: Measured in Hertz
    DUTY_CYCLE_MIN: Measured in percent
    DUTY_CYCLE_MAX: Measured in percent
    """

    _PWM_FREQ = 910
    _DUTY_CYCLE_MIN = 2.9
    _DUTY_CYCLE_MAX = 97.1
    _SPEED_PERIOD = 0.1

    def __init__(self, raspi, encoderInputPin) -> None:
        self._raspi = raspi
        self._numTurns = 0
        self._pulseWidth = 0
        self._currentOmega = 0  # Measured in degrees per second
        self._currentTheta = 0  # Measured in degrees
        self._angle = 0
        self._startTime = time.time()
        self._lastTheta = 0
        self._angleFIFO = queue.Queue(maxsize=int(self._PWM_FREQ * self._SPEED_PERIOD))
        for i in range(int(self._PWM_FREQ * self._SPEED_PERIOD)):
            self._angleFIFO.put(0)
        # Setup encoderInputPin and Callback function
        self._raspi.set_mode(encoderInputPin, pigpio.INPUT)
        self._raspi.callback(encoderInputPin, pigpio.EITHER_EDGE, self.__gpio_callback)

    def __gpio_callback(self, GPIO, level, tick):
        if level:
            # Rising edge
            self._startTime = tick
            self._lastTheta = self._angleFIFO.get()
            self._currentTheta = self._numTurns * 360 + self._angle
            self._angleFIFO.put(self._currentTheta)
            self._currentOmega = (
                self._currentTheta - self._lastTheta
            ) / self._SPEED_PERIOD  # Period in seconds
        else:
            # Falling edge
            self.lastPulseWidth = self._pulseWidth
            self._pulseWidth = tick - self._startTime
            self.lastAngle = (
                (
                    100 * (self.lastPulseWidth * self._PWM_FREQ / 1000000)
                    - self._DUTY_CYCLE_MIN
                )
                * 360
                / (self._DUTY_CYCLE_MAX - self._DUTY_CYCLE_MIN)
            )
            self._angle = (
                (
                    100 * (self._pulseWidth * self._PWM_FREQ / 1000000)
                    - self._DUTY_CYCLE_MIN
                )
                * 360
                / (self._DUTY_CYCLE_MAX - self._DUTY_CYCLE_MIN)
            )
            if self._angle - self.lastAngle < -180:
                # One complete turn going forward
                self._numTurns += 1
            elif self._angle - self.lastAngle > 180:
                # One complete turn going backwards
                self._numTurns -= 1

    def getCurrentTheta(self):
        # Theta in degrees
        return self._currentTheta

    def getCurrentOmega(self):
        # Speed in degrees per second
        return self._currentOmega
