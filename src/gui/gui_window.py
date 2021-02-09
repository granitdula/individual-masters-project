import os

from PySide6 import QtWidgets as qtw

from src.image_handlers.image_input_handler import ImageInputHandler


BASEDIR = os.path.dirname(__file__)  # Relative reference to resources


class GUIWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self._input_handler = ImageInputHandler()

        self._setup_ui()

        self.show()

    def _setup_ui(self):
        # Designs the UI of the window including properties and widget components.

        self.setWindowTitle("Photo2Depth")

        self._setup_background()
        self._setup_gui_widgets()

    def _setup_background(self):
        self.background_widget = qtw.QWidget(self)
        self.background_widget.resize(self.width(), self.height())
        img_path = BASEDIR + "/../../resources/images/gui_images/background_gui.jpeg"
        background_style = f"background-image: url({img_path}) 0 0 0 0 stretch stretch;"
        self.background_widget.setStyleSheet(background_style)

    def _setup_gui_widgets(self):
        self.heading = qtw.QLabel("Photo2Depth")
        self.heading.setStyleSheet("font-size: 64px; font-family: Helvetica; \
                                    text-align: center;")
        self.browse_button = qtw.QPushButton("Browse Button")
        self.browse_button.clicked.connect(self.on_browse)
        font = self.browse_button.font()
        font.setPointSize(16)
        font.setFamily("Helvetica")
        self.browse_button.setFont(font)

        self.layout = qtw.QVBoxLayout(self)
        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.browse_button)

    def resizeEvent(self, event):
        self.background_widget.resize(self.width(), self.height())

    def on_browse(self):
        """
        Callback function that's called after the browse_button is clicked.

        :return: None.
        """
        image_filter = "Images (*.png *.xpm *.jpg)"
        (file_name, extensions) = qtw.QFileDialog.getOpenFileName(self, "Open Image",
                                                                  filter="Images (*.png *.xpm \
                                                                  *.jpg)")

        if not file_name:
            return
        if extensions == image_filter:
            self._input_handler.handle_input(file_name)
