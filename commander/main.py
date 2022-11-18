from time import sleep

from src.components.intelligence import Intelligence

intel = Intelligence(deviceNumberList=[29])


def main() -> None:
    while not intel.device[29].telemetryStarted:
        sleep(0.001)
        continue
    # Here goes the intelligence logic
    while True:
        intel.device[29].turn(90, 20, 400)
        intel.device[29].stopForTime(10)
        intel.device[29].waitUntilExecutingInstruction(3)
        sleep(3)
        # intel.device[29].waitUntilExecutingInstruction(1)
        intel.device[29].flush()
        intel.device[29].waitUntilExecutingInstruction(0)


if __name__ == "__main__":
    main()
    intel.deinit()
    del intel
