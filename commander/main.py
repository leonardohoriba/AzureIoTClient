import threading
from time import sleep

from src.components.intelligence import Intelligence
from src.helpers.graphing import Graphing

robotList = [29]

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
        # All robots move forward until one finds an obstacle
        for robot in robotList:
            intel.device[robot].moveUntilObstacleFound(distance=5000, speed=150, obstacleDistance=300)
        for robot in robotList:
            intel.device[robot].waitUntilExecutingInstruction(5)
        robotThatFoundObstacle = -1
        while robotThatFoundObstacle == -1:
            for robot in robotList:
                if intel.device[robot].getState()["instructionID"] == 0:
                    robotThatFoundObstacle = robot
                    break
        # Stop all other robots
        robotsToStop = robotList.copy()
        robotsToStop.remove(robotThatFoundObstacle)
        for robot in robotsToStop:
            intel.device[robot].flush()
        # All other robots turn to face the obstacle
        robotsToTurn = robotList.copy()
        robotsToTurn.remove(robotThatFoundObstacle)
        for robot in robotsToTurn:
            if robot < robotThatFoundObstacle:
                intel.device[robot].turnUntilObjectFound(angle=3600, angularSpeed=45, radius=0, objectName="bottle")
            else:
                intel.device[robot].turnUntilObjectFound(angle=-3600, angularSpeed=45, radius=0, objectName="bottle")
        for robot in robotList:
            intel.device[robot].waitUntilExecutingInstruction(0)
        sleep(1000)


if __name__ == "__main__":
    threadCommander = threading.Thread(target=commander, name="threadCommander")
    threadCommander.start()
    # graph.plotGraph()
    threadCommander.join()
    intel.deinit()
    del intel
