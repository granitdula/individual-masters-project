import cv2 as cv
import sys

from src.image_handlers.image_processor import ImageProcessor
from src.three_d.view_3d import View3D


class ImageInputHandler:

    def __init__(self):
        self._image_processor = ImageProcessor()
        self._view_3d = View3D()

    # TODO: Change this to be UI where user can browse for an image.
    def handle_input(self):
        image = self._input_image()

        instance_data = self._image_processor.process_image(image)
        print(instance_data)

        self._view_3d.run()

    def _input_image(self):
        image_path = "./../resources/images/living_room_1_small.jpg"

        # TODO: Change image read, to be one that's input by user by browsing files.
        image = cv.imread(image_path)

        if image is None:
            sys.exit("Could not read the image.")

        return image
