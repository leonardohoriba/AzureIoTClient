import cv2 as cv
import numpy as np
from tflite_runtime.interpreter import Interpreter

import settings
from src.components.NeuralNetwork.Camera import Camera


class NeuralNetwork(Camera):
    __INPUT_MEAN = 127.5
    __INPUT_STD = 127.5
    __MINIMUM_CONFIDENCE = settings.NEURAL_NETWORK_MINIMUM_CONFIDENCE

    def __init__(self):
        with open("./src/components/NeuralNetwork/labelmap.txt", "r") as f:
            self.__labels = [line.strip() for line in f.readlines()]
            if self.__labels[0] == "???":
                del self.__labels[0]
        self.__model_interpreter = Interpreter(
            model_path="./src/components/NeuralNetwork/detect.tflite"
        )
        self.__model_interpreter.allocate_tensors()
        self.__input = self.__model_interpreter.get_input_details()
        self.__output = self.__model_interpreter.get_output_details()
        self.__height = self.__input[0]["shape"][1]
        self.__width = self.__input[0]["shape"][2]
        self.__floating_model = self.__input[0]["dtype"] == np.float32

        # Must call parent constructor after everything is initialized to avoid a race condition between child constructor and camera thread
        super().__init__()

    def processFrame(self, frame):
        # Duplicating the frame and adjusting the size of it
        frame_copy = frame.copy()
        frame_rgb = cv.cvtColor(frame_copy, cv.COLOR_BGR2RGB)
        frame_resized = cv.resize(frame_rgb, (self.__width, self.__height))
        input_data = np.expand_dims(frame_resized, axis=0)
        # For a non quantized model we should normalize the pixels
        if self.__floating_model:
            input_data = (np.float32(input_data) - self.__INPUT_MEAN) / self.__INPUT_STD
        self.__model_interpreter.set_tensor(self.__input[0]["index"], input_data)
        self.__model_interpreter.invoke()
        # Bounding box coordinates
        box = self.__model_interpreter.get_tensor(self.__output[0]["index"])[0]
        # Class index of the objects
        classes = self.__model_interpreter.get_tensor(self.__output[1]["index"])[0]
        # Confidence of detected objects
        conf_value = self.__model_interpreter.get_tensor(self.__output[2]["index"])[0]
        self.__object_list = []
        for i in range(len(conf_value)):  # Comparing with the minimum threshold
            if (conf_value[i] > self.__MINIMUM_CONFIDENCE) and (conf_value[i] <= 1.0):
                # Get bounding box coordinates and draw box
                # To force the interpretor to return coordinates within the image using predefined max and min functions
                ymin = int(max(1, (box[i][0] * self._RESOLUTION_HEIGHT)))
                xmin = int(max(1, (box[i][1] * self._RESOLUTION_WIDTH)))
                ymax = int(
                    min(self._RESOLUTION_HEIGHT, (box[i][2] * self._RESOLUTION_HEIGHT))
                )
                xmax = int(
                    min(self._RESOLUTION_WIDTH, (box[i][3] * self._RESOLUTION_WIDTH))
                )
                cv.rectangle(frame_copy, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)
                # Draw label around the box
                object_name = self.__labels[int(classes[i])]
                label = "%s: %d%%" % (object_name, int(conf_value[i] * 100))
                self.__object_list.append({
                    "name": object_name,
                    "confidence": conf_value[i]
                })
                # Get font size
                labelSize, baseLine = cv.getTextSize(
                    label, cv.FONT_HERSHEY_SIMPLEX, 0.7, 2
                )
                label_ymin = max(ymin, labelSize[1] + 10)
                cv.rectangle(
                    frame_copy,
                    (xmin, label_ymin - labelSize[1] - 10),
                    (xmin + labelSize[0], label_ymin + baseLine - 10),
                    (255, 255, 255),
                    cv.FILLED,
                )
                cv.putText(
                    frame_copy,
                    label,
                    (xmin, label_ymin - 7),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 0),
                    2,
                )
        return frame_copy

    def getObjectList(self):
        return self.__object_list