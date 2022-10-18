import threading
from queue import Empty
from time import sleep

import pigpio
from decouple import config

from src.components.NeuralNetwork.NeuralNetwork import NeuralNetwork
from src.components.Stingray import Stingray
from src.helpers.socket_client import SocketClient

DEBUG_PID = bool(config("DEBUG_PID", default=False))
raspi = pigpio.pi()
robot = Stingray(raspi)
sleep(1.5)  # Wait for the wheel to settle
neuralnetwork = NeuralNetwork()
sleep(0.5)  # Must wait for the first frame to be captured before starting stream
neuralnetwork.startStreaming()
client = SocketClient()
finished = False


def sendTelemetry():
    while not finished:
        # PID calibration doesn't need sonar and needs higher sample rate
        if not DEBUG_PID:
            # print(f"Distance: {robot.getSonarDistance()}")
            robot.triggerSonar()
        # client.send(
        #     {
        #         "leftWheelSpeed": robot.getLeftWheelSpeed(),
        #         "rightWheelSpeed": robot.getRightWheelSpeed(),
        #         "sonarDistance": robot.getSonarDistance(),
        #     }
        # )
        if DEBUG_PID:
            sleep(0.01)
        else:
            sleep(0.25)


def main():
    global raspi
    global robot
    global neuralnetwork
    global client
    global finished
    robot.triggerSonar()
    sleep(0.1)

    robot.stop()
    robot.setSonarAngle(0)
    sleep(2)

    threadSendTelemetry = threading.Thread(target=sendTelemetry, name="sendTelemetry")
    threadSendTelemetry.start()

    while True:
        try:
            instruction = client.getFromQueue()
        except Empty:
            sleep(0.001)
            continue
        if instruction["method_name"] == "disconnect":
            break
        elif instruction["method_name"] == "setMovement":
            payload = instruction["payload"]
            robot.moveDistanceSpeed(
                payload["leftWheelDistance"],
                payload["leftWheelSpeed"],
                payload["rightWheelDistance"],
                payload["rightWheelSpeed"],
            )
            robot.waitUntilGoal()
        elif instruction["method_name"] == "stopForTime":
            payload = instruction["payload"]
            sleep(payload["time"])
        elif instruction["methodName"] == "moveUntilObjectFound":
            payload = instruction["payload"]
            robot.moveDistanceSpeed(
                payload["leftWheelDistance"],
                payload["leftWheelSpeed"],
                payload["rightWheelDistance"],
                payload["rightWheelSpeed"],
            )
            # TODO Wait until object found goes here

    finished = True
    threadSendTelemetry.join()
    neuralnetwork.deinit()
    robot.deinit()
    client.deinit()
    del neuralnetwork
    del robot
    del client


if __name__ == "__main__":
    main()
