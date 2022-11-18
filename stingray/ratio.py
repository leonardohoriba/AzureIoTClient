import threading
from queue import Empty
from time import sleep
from time import time

import pigpio
from decouple import config

import settings
from src.components.Stingray import Stingray
from src.helpers.socket_client import SocketClient
from src.helpers.direct_method_constants import MethodName

DEBUG_PID = bool(config("DEBUG_PID", default=False))
raspi = pigpio.pi()
robot = Stingray(raspi)
sleep(1.5)  # Wait for the wheel to settle
client = SocketClient(MethodName.FLUSH, robot.flushCallback)
finished = False

def main():
    while True:
        sleep(1)

if __name__ == "__main__":
    main()
    robot.deinit()
    client.deinit()
    del robot
    del client
    print(
        "---------------------------------------finished---------------------------------------"
    )
