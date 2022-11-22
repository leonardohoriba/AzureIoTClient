import threading
from time import sleep

from src.components.intelligence import Intelligence
from src.helpers.graphing import Graphing

graph = Graphing(numPlots=2, numPoints=20)
intel = Intelligence(deviceNumberList=[2, 1], graph=graph)

finished = False


def commander() -> None:
    while not intel.device[2].telemetryStarted:
        sleep(0.001)
        continue
    while not intel.device[1].telemetryStarted:
        sleep(0.001)
        continue
    # Here goes the intelligence logic
    while not finished:
        intel.moveSync([1, 2], distance=2000, speed=200)
        intel.device[2].turn(angle=180, angularSpeed=45, radius=0)
        intel.device[1].turn(angle=-180, angularSpeed=45, radius=0)
        intel.moveSync([1, 2], distance=2000, speed=200)
        intel.device[2].turn(angle=-180, angularSpeed=45, radius=0)
        intel.device[1].turn(angle=180, angularSpeed=45, radius=0)
        intel.device[2].waitUntilExecutingInstruction(0)
        intel.device[1].waitUntilExecutingInstruction(0)
        sleep(10)


if __name__ == "__main__":
    threadCommander = threading.Thread(target=commander, name="threadCommander")
    threadCommander.start()
    graph.plotGraph()
    finished = True
    threadCommander.join()
    intel.deinit()
    del intel
