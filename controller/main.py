from src.helpers.controller import Controller
from utils.direct_method_constants import DeviceID, MethodName

# Example
controller = Controller()
controller.iothub_devicemethod(
    device_id=DeviceID.STINGRAY_29,
    method_name=MethodName.SET_MOVEMENT,
    payload={
        "rightWheelSpeed": 10,
        "rightWheelDistance": 20,
        "leftWheelSpeed": 30,
        "rightWheelDistance": 40,
    },
)
