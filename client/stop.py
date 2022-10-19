print("Stopping robot")
import pigpio

raspi = pigpio.pi()
raspi.set_servo_pulsewidth(17, 0)
raspi.set_servo_pulsewidth(27, 0)
raspi.set_servo_pulsewidth(25, 0)
print("Robot stopped")
