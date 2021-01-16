import cv2 as cv
import sys

from src.image_handlers.rcnn_segmenter import RCNNSegmenter


class ImageInputHandler:

    SEGMENT_ACC_THRESHOLD = 0.5

    def __init__(self):
        self._rcnn = RCNNSegmenter(self.SEGMENT_ACC_THRESHOLD)

    # TODO: Change this to be UI where user can browse for an image.
    def handle_input(self):
        image = self._input_image()

        # cv.imshow("Display window", image)
        self._rcnn.visualise_segmentation(image)
        _ = cv.waitKey(0)

    def _input_image(self):
        image_path = "./../resources/images/living_room_1_small.jpg"

        # TODO: Change image read, to be one that's input by user by browsing files.
        image = cv.imread(image_path)

        if image is None:
            sys.exit("Could not read the image.")

        return image
