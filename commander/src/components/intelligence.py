import threading
from time import sleep

from src.helpers.commander import Commander
from src.components.StingrayCommander import StingrayCommander


class Intelligence:
    def __init__(self):
        self._finished = False
        self._commander = Commander()
        self._robot0 = StingrayCommander(self._commander, 29)
        self._commander.start()

        self._threadGetTelemetry = threading.Thread(
            target=self.__getTelemetry, name="getTelemetry"
        )
        self._threadGetTelemetry.start()
        self._threadIntelligence = threading.Thread(
            target=self.__intelligence, name="intelligence"
        )
        self._threadIntelligence.start()

    def deinit(self):
        self._commander.stop()
        self._finished = True
        self._threadGetTelemetry.join()
        self._threadIntelligence.join()

    def __getTelemetry(self):
        while not self._finished:
            telemetry = self._commander.getTelemetry()
            sleep(5)

    def __intelligence(self):
        while not self._finished:
            sleep(10)
            self._robot0.turn(90, 20, 400)
