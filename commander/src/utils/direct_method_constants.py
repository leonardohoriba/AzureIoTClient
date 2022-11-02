import inspect


class MethodName:
    SET_MOVEMENT = "setMovement"
    DISCONNECT = "disconnect"
    STOP_FOR_TIME = "stopForTime"
    MOVE_UNTIL_OBJECT_FOUND = "moveUntilObjectFound"


class DeviceID:
    STINGRAY_29 = "Stingray29"
    STINGRAY_30 = "Stingray30"

    def getDeviceId(number: int) -> str:
        attributes = inspect.getmembers(DeviceID, lambda a: not (inspect.isroutine(a)))
        for attribute in [
            a for a in attributes if not (a[0].startswith("__") and a[0].endswith("__"))
        ]:
            if str(number) in attribute[0]:
                return attribute[1]
