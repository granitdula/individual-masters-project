import sys

from PySide6.QtWidgets import QApplication

from src.gui.gui_window import GUIWindow
# from src.image_handlers.image_input_handler import ImageInputHandler


class Application:

    def __init__(self):
        self._app = QApplication(sys.argv)
        self._gui_window = GUIWindow()
        self._gui_window.resize(800, 600)

        # self._input_handler = ImageInputHandler()

    def run(self):
        # self._input_handler.handle_input()
        sys.exit(self._app.exec_())


if __name__ == '__main__':
    application = Application()
    application.run()
