import cv2 as cv
import sys

from src.image_handlers.image_processor import ImageProcessor
from src.three_d.view_3d import View3D


class ImageInputHandler:

    def __init__(self):
        self._image_processor = ImageProcessor()
        self._view_3d = None  # Initialised as None before any input handling.

    def handle_input(self, file_path):
        """
        Gets the image from the specified file_path and runs the processor to analyse the image
        and start the 3D application.

        :param file_path: The file path of the desired image.
        :return: None.
        """
        image = self._input_image(file_path)

        instance_data = self._image_processor.process_image(image)
        print(instance_data)

        self._view_3d = View3D(instance_data)
        self._view_3d.run()

    @staticmethod
    def _input_image(file_path):
        # Reads the image safely with OpenCV and returns it.
        image = cv.imread(file_path)

        if image is None:
            sys.exit("Could not read the image.")

        return image
