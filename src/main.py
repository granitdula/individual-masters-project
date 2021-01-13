from src.image_handlers.image_input_handler import ImageInputHandler


class Application:

    def __init__(self):
        self._input_handler = ImageInputHandler()

    def run(self):
        self._input_handler.handle_input()


if __name__ == '__main__':
    application = Application()
    application.run()
