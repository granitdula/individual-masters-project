import sys

from PySide6.QtWidgets import QApplication

from src.gui.gui_window import GUIWindow


class Application:

    def __init__(self):
        self._app = QApplication(sys.argv)
        self._gui_window = GUIWindow()
        self._gui_window.resize(800, 600)

    def run(self):
        """
        Runs the main application

        :return: None
        """
        sys.exit(self._app.exec_())


if __name__ == '__main__':
    application = Application()
    application.run()
