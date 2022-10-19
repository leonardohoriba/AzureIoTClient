import pigpio

import settings


class Sonar:
    """
    Class for the HC-SR04 ultrassonic sensor (sonar)
    _TRIG_PULSE_LEN: Measured in microseconds
    _SOUND_SPEED: Measured in meters per second
    _MAX_ECHO_PULSE_WIDTH: Measure in microseconds
    echo pulse width with no obstacle is 38ms by datasheet, 134.2ms measured on stingray 29
    """

    _TRIG_PULSE_LEN = 20
    _SOUND_SPEED = 340.0
    _MAX_ECHO_PULSE_WIDTH = settings.SONAR_MAX_ECHO_PULSE_WIDTH

    def __init__(self, raspi, trigPin, echoPin, motorPin):
        self._raspi = raspi
        self._trigPin = trigPin
        self._echoPin = echoPin
        self._motorPin = motorPin
        self._startTime = 0
        self._deltaTime = 0
        self._raspi.set_mode(trigPin, pigpio.OUTPUT)
        self._raspi.set_mode(echoPin, pigpio.INPUT)
        self._raspi.set_mode(motorPin, pigpio.OUTPUT)
        self._raspi.callback(echoPin, pigpio.EITHER_EDGE, self.__gpio_callback)

    def deinit(self):
        # Stop the servo
        self._raspi.set_servo_pulsewidth(self._motorPin, 0)

    def __gpio_callback(self, GPIO, level, tick):
        if level:
            # Rising edge
            self._startTime = tick
        else:
            # Falling edge
            self._deltaTime = tick - self._startTime

    def trigger(self):
        self._raspi.gpio_trigger(self._trigPin, self._TRIG_PULSE_LEN, pigpio.ON)

    def getDistance(self):
        # Distance in millimeters
        if self._deltaTime > self._MAX_ECHO_PULSE_WIDTH:
            return -1
        else:
            return self._deltaTime * self._SOUND_SPEED / (1000 * 2)

    def setAngle(self, angle):
        if angle >= -100 and angle <= 100:
            self._raspi.set_servo_pulsewidth(self._motorPin, 1520 + angle * 900 / 90)
