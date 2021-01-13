import cv2 as cv
import sys


class ImageInputHandler:

    def __init__(self):
        pass

    # TODO: Change this to be UI where user can browse for an image.
    def handle_input(self):
        image = self.__input_image()

        cv.imshow("Display window", image)
        _ = cv.waitKey(0)

    def __input_image(self):
        image_path = sys.path[0] + "/../resources/images/living_room_1.jpg"

        # TODO: Change image read, to be one that's input by user by browsing files.
        image = cv.imread(cv.samples.findFile(image_path))

        if image is None:
            sys.exit("Could not read the image.")

        return image
