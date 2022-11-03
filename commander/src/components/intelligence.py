import threading
from queue import Empty
from time import sleep

from src.components.StingrayCommander import StingrayCommander
from src.helpers.commander import Commander
from src.utils.direct_method_constants import DeviceID


class Intelligence:
    def __init__(self, deviceNumberList: list[int]):
        self._finished = False
        self._commander = Commander()
        self.device = [StingrayCommander] * 64
        self._deviceNumberList = deviceNumberList
        for deviceNumber in deviceNumberList:
            self.device[deviceNumber] = StingrayCommander(self._commander, deviceNumber)
        self._commander.start()

        self._threadGetTelemetry = threading.Thread(
            target=self.__getTelemetry, name="getTelemetry"
        )
        self._threadGetTelemetry.start()

    def deinit(self):
        self._commander.stop()
        self._finished = True
        self._threadGetTelemetry.join()

    def __getTelemetry(self):
        while not self._finished:
            telemetry = self._commander.getTelemetry()
            if telemetry is not None:
                deviceNumber = DeviceID.getNumberFromDeviceId(telemetry["deviceID"])
                if deviceNumber in self._deviceNumberList:
                    self.device[deviceNumber].telemetryStarted = True
                    self.device[deviceNumber].telemetryCallback(telemetry["body"])
            else:
                sleep(0.001)


