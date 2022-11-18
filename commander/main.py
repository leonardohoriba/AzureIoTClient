from time import sleep

from src.components.intelligence import Intelligence

intel = Intelligence(deviceNumberList=[29, 30])


def main() -> None:
    while not intel.device[29].telemetryStarted:
        sleep(0.001)
        continue
    while not intel.device[30].telemetryStarted:
        sleep(0.001)
        continue
    # Here goes the intelligence logic
    while True:
        intel.device[29].move(distance=1000, speed=200)
        intel.device[30].move(distance=1000, speed=200)
        intel.device[29].stopForTime(time=2)
        intel.device[30].stopForTime(time=2)
        intel.device[29].turn(angle=180, angularSpeed=45, radius=0)
        intel.device[30].turn(angle=-180, angularSpeed=45, radius=0)
        intel.device[29].stopForTime(time=2)
        intel.device[30].stopForTime(time=2)
        intel.device[29].move(distance=1000, speed=200)
        intel.device[30].move(distance=1000, speed=200)
        intel.device[29].stopForTime(time=2)
        intel.device[30].stopForTime(time=2)
        intel.device[29].turn(angle=-180, angularSpeed=45, radius=0)
        intel.device[30].turn(angle=180, angularSpeed=45, radius=0)
        intel.device[29].waitUntilExecutingInstruction(0)
        intel.device[30].waitUntilExecutingInstruction(0)         
        sleep(10)

if __name__ == "__main__":
    main()
    intel.deinit()
    del intel
