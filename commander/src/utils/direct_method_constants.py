import re
from azure.iot.hub import IoTHubRegistryManager
from decouple import config


class MethodName:
    FLUSH = "flush"
    SET_MOVEMENT = "setMovement"
    DISCONNECT = "disconnect"
    STOP_FOR_TIME = "stopForTime"
    MOVE_UNTIL_OBJECT_FOUND = "moveUntilObjectFound"
    MOVE_UNTIL_OBSTACLE_FOUND = "moveUntilObstacleFound"


class DeviceID:
    device_list = IoTHubRegistryManager(
        config("AZURE_IOT_HUB_CONNECTION_STRING")
    ).get_devices()

    def getDeviceIdFromNumber(self, number: int) -> str:
        for device in self.device_list:
            if str(number) in device.device_id:
                return device.device_id
        return None

    def getNumberFromDeviceId(self, deviceID: str) -> int:
        numbers_list = re.findall(r"\d+", deviceID)
        return int(numbers_list[-1])

    def getDevices(self) -> list:
        return [device.device_id for device in self.device_list]
