import threading
from queue import Empty
from time import sleep

from src.components.StingrayCommander import StingrayCommander
from src.helpers.commander import Commander
from src.helpers.graphing import Graphing
from src.utils.direct_method_constants import DeviceID


class Intelligence:
    _MAX_NUMBER_OF_ROBOTS = 64

    def __init__(self, deviceNumberList: list[int], graph: Graphing):
        self._graph = graph
        self._finished = False
        self._commander = Commander()
        self.device = [StingrayCommander] * self._MAX_NUMBER_OF_ROBOTS
        self._deviceNumberList = deviceNumberList
        for deviceNumber in deviceNumberList:
            self.device[deviceNumber] = StingrayCommander(self._commander, deviceNumber)
        self._commander.start()

        self._threadGetTelemetry = threading.Thread(
            target=self.__getTelemetry, name="getTelemetry"
        )
        self._threadGetInterface = threading.Thread(
            target=self.__getInterface, name="getInterface"
        )
        self._threadGetTelemetry.start()
        self._threadGetInterface.start()
        self._startButtonClicked = False

    def deinit(self):
        self._commander.stop()
        self._finished = True
        self._threadGetTelemetry.join()

    def __getTelemetry(self):
        while not self._finished:
            telemetry = self._commander.getTelemetry()
            if telemetry is None:
                sleep(0.001)
                continue
            deviceNumber = DeviceID().getNumberFromDeviceId(telemetry["deviceID"])
            if deviceNumber in self._deviceNumberList:
                self.device[deviceNumber].telemetryStarted = True
                self.device[deviceNumber].telemetryCallback(telemetry["body"])
            if deviceNumber == 2:
                self._graph.plotValue(
                    value=[
                        self.device[2].getState()["leftWheelSpeed"],
                        self.device[1].getState()["leftWheelSpeed"],
                    ]
                )

    def __getInterface(self):
        while not self._finished:
            interfaceButtons = self._commander.socket.receive_all()
            if(interfaceButtons["start_button"]):
                print("start_button")
                self._startButtonClicked = True
                continue
            if(interfaceButtons["stop_button"]):
                print("stop_button")
                for deviceNumber in self._deviceNumberList:
                    self.device[deviceNumber].flush()
                raise Exception("Emergency stop")
            else:
                sleep(1)
                continue
            
    def waitForStartButton(self):
        while not self._startButtonClicked:
            sleep(0.001)

    def moveSync(self, robots: list[int], distance: float, speed: float):
        for robotNumber in robots:
            self.device[robotNumber].waitUntilExecutingInstruction(0)
        # Get start position and command a movement for half the distance required
        startPosition = self._MAX_NUMBER_OF_ROBOTS * [float(0)]
        lessThanOneQuarter = True
        for robotNumber in robots:
            startPosition[robotNumber] = self.device[robotNumber].getState()[
                "leftWheelPosition"
            ]
            self.device[robotNumber].move(distance=distance / 2, speed=speed)
        # Calculate delta speed for each robot
        deltaSpeed = self._MAX_NUMBER_OF_ROBOTS * [float(0)]
        robotThatReachedOneQuarter = 0
        while lessThanOneQuarter:
            for robotNumber in robots:
                if (
                    self.device[robotNumber].getState()["leftWheelPosition"]
                    - startPosition[robotNumber]
                    > distance / 4
                ):
                    lessThanOneQuarter = False
                    robotThatReachedOneQuarter = robotNumber
                    print(f"Robot {robotNumber} reached one quarter")
        for robotNumber in robots:
            if robotNumber != robotThatReachedOneQuarter:
                deltaDistance = (
                    self.device[robotThatReachedOneQuarter].getState()[
                        "leftWheelPosition"
                    ]
                    - startPosition[robotThatReachedOneQuarter]
                ) - (
                    self.device[robotNumber].getState()["leftWheelPosition"]
                    - startPosition[robotNumber]
                )
                print(f"Delta distance {robotNumber} = {deltaDistance}")
                deltaSpeed[robotNumber] = deltaDistance * 2 * speed / distance
        # Command the rest of the movement with the delta speed added
        for robotNumber in robots:
            self.device[robotNumber].move(
                distance=distance / 2, speed=(speed + deltaSpeed[robotNumber])
            )
