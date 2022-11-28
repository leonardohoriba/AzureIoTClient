import inspect


class MethodName:
    FLUSH = "flush"
    SET_MOVEMENT = "setMovement"
    DISCONNECT = "disconnect"
    STOP_FOR_TIME = "stopForTime"
    MOVE_UNTIL_OBJECT_FOUND = "moveUntilObjectFound"


class DeviceID:
    STINGRAY_1 = "Stingray01"
    STINGRAY_2 = "Stingray02"
    STINGRAY_29 = "Stingray29"
    STINGRAY_30 = "Stingray30"

    def getDeviceIdFromNumber(number: int) -> str:
        attributes = inspect.getmembers(DeviceID, lambda a: not (inspect.isroutine(a)))
        for attribute in [
            a for a in attributes if not (a[0].startswith("__") and a[0].endswith("__"))
        ]:
            if str(number) == attribute[0].split("_")[-1]:
                return attribute[1]

    def getNumberFromDeviceId(deviceID: str) -> int:
        attributes = inspect.getmembers(DeviceID, lambda a: not (inspect.isroutine(a)))
        for attribute in [
            a for a in attributes if not (a[0].startswith("__") and a[0].endswith("__"))
        ]:
            if attribute[1] == deviceID:
                return int(attribute[0].split("_")[-1])

    def getDevices() -> list:
        attributes = inspect.getmembers(DeviceID, lambda a: not (inspect.isroutine(a)))
        return [
            a[-1] for a in attributes if not (a[0].startswith("__") and a[0].endswith("__"))
        ]
