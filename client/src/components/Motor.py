from src.components.Encoder import Encoder

class Motor():
    def __init__(self, raspi, encoderInputPin, motorOutputPin):
        self.raspi = raspi
        self.encoder = Encoder(raspi, encoderInputPin)
        self.motorOutputPin = motorOutputPin
    
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