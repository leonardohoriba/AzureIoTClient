import pigpio


print("Stopping robot")
raspi = pigpio.pi()
raspi.set_servo_pulsewidth(23, 0)
raspi.set_servo_pulsewidth(24, 0)
raspi.set_servo_pulsewidth(25, 0)
print("Robot stopped")
