import threading
from queue import Empty
from time import sleep

from src.components.StingrayCommander import StingrayCommander
from src.helpers.commander import Commander


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
            try:
                telemetry = self._commander.getTelemetry()
            except Empty:
                sleep(0.001)
                continue

    def __intelligence(self):
        while not self._finished:
            sleep(10)
            self._robot0.turn(90, 20, 400)
