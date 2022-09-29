from src.components.Encoder import Encoder
import threading
from time import sleep

class Motor():

    NUM_INTEGRAL_TERMS = 20
    error = [0]*NUM_INTEGRAL_TERMS
    goalTheta = 0
    finished = False

    def __init__(self, raspi, encoderInputPin, motorOutputPin):
        self.raspi = raspi
        self.encoder = Encoder(raspi, encoderInputPin)
        self.motorOutputPin = motorOutputPin
        self.threadControl = threading.Thread(target=self.__control)
        self.threadControl.start()
    
    def deinit(self):
        self.finished = True
        self.threadControl.join()
        self.setPower(0)
        del self.encoder 
    
    def setSpeed(self, speed):
        self.setPower(speed)

    def setGoalTheta(self, goalTheta):
        self.goalTheta = goalTheta

    def setPower(self, power):
        # power ranging from -100 to 100
        if power == 0:
            self.raspi.set_servo_pulsewidth(self.motorOutputPin, 1500)
        elif power > 0 and power <= 100:
            self.raspi.set_servo_pulsewidth(self.motorOutputPin, 1520+power*200/100)
        elif power > 100:
            self.raspi.set_servo_pulsewidth(self.motorOutputPin, 1720)
        elif power < 0 and power >= -100:
            self.raspi.set_servo_pulsewidth(self.motorOutputPin, 1480+power*200/100)
        elif power < -100:
            self.raspi.set_servo_pulsewidth(self.motorOutputPin, 1280)

    def getCurrentTheta(self):
        return self.encoder.getCurrentTheta()

    def getCurrentSpeed(self):
        return self.encoder.getCurrentSpeed()

    def __control(self):
        while not self.finished:
            kp = -1
            ki = 0
            kd = 0
            for i in range(self.NUM_INTEGRAL_TERMS - 1):
                self.error[i] = self.error[i+1]
            self.error[self.NUM_INTEGRAL_TERMS - 1] = self.goalTheta - self.getCurrentTheta()
            derror = self.error[self.NUM_INTEGRAL_TERMS - 1] - self.error[self.NUM_INTEGRAL_TERMS - 2]
            ierror = 0
            for i in range(self.NUM_INTEGRAL_TERMS):
                ierror += self.error[self.NUM_INTEGRAL_TERMS - (i+1)] * (1-(i/self.NUM_INTEGRAL_TERMS))
            power = kp*self.error[self.NUM_INTEGRAL_TERMS - 1] + ki*ierror + kd*derror
            self.setPower(power)
            sleep(0.025)