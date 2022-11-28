import threading
from time import sleep

from src.components.intelligence import Intelligence
from src.helpers.graphing import Graphing

robotList = [1, 2, 29, 30]

graph = Graphing(numPlots=2, numPoints=20)
intel = Intelligence(deviceNumberList=robotList, graph=graph)

def commander() -> None:
    for robot in robotList:
        while not intel.device[robot].telemetryStarted:
            sleep(0.001)
            continue
    intel.waitForStartButton()
    # Here goes the intelligence logic
    while True:
        intel.moveSync(robotList, distance=2000, speed=150)
        intel.device[1].turn(angle=180, angularSpeed=45, radius=0)
        intel.device[2].turn(angle=-180, angularSpeed=45, radius=0)
        intel.device[29].turn(angle=180, angularSpeed=45, radius=0)
        intel.device[30].turn(angle=-180, angularSpeed=45, radius=0)
        intel.moveSync(robotList, distance=2000, speed=150)
        intel.device[1].turn(angle=-180, angularSpeed=45, radius=0)
        intel.device[2].turn(angle=180, angularSpeed=45, radius=0)
        intel.device[29].turn(angle=-180, angularSpeed=45, radius=0)
        intel.device[30].turn(angle=180, angularSpeed=45, radius=0)
        for robot in robotList:
            intel.device[robot].waitUntilExecutingInstruction(0)
        sleep(10)


if __name__ == "__main__":
    threadCommander = threading.Thread(target=commander, name="threadCommander")
    threadCommander.start()
    # graph.plotGraph()
    threadCommander.join()
    intel.deinit()
    del intel
