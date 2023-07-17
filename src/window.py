from qt_modules import *

from PySide2.QtWidgets import QPushButton, QWidget, QTextBrowser
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QGridLayout
from PySide2.QtCore import QTimer, SIGNAL

BIG_BUTTON_HSIZE = 200
BIG_BUTTON_VSIZE = 60

EXIT_BUTTON_HSIZE = 150
EXIT_BUTTON_VSIZE = 60

class Window(QWidget):
    def __init__(self, app, dispatcher, parent=None):
        super().__init__(parent)
        self.dispatcher = dispatcher

        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.dispatcher.recorder.tick)

        start_recording_button = QPushButton(
            text='Start recording',
            parent=self
        )
        start_recording_button.clicked.connect(self.dispatcher.recorder.start_recording)
        start_recording_button.setFixedSize(BIG_BUTTON_HSIZE, BIG_BUTTON_VSIZE)

        stop_recording_button = QPushButton(
            text='Stop recording', 
            parent=self
        )
        stop_recording_button.clicked.connect(self.dispatcher.recorder.stop_recording)
        stop_recording_button.setFixedSize(BIG_BUTTON_HSIZE, BIG_BUTTON_VSIZE)

        exit_button = QPushButton(
            text="Exit",
            parent=self
        )
        exit_button.clicked.connect(app.exit)
        exit_button.setFixedSize(EXIT_BUTTON_HSIZE, EXIT_BUTTON_VSIZE)
        
        grid = QGridLayout()

        buttons_gbox = QGroupBox()
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(start_recording_button)
        buttons_layout.addWidget(stop_recording_button)
        buttons_layout.addWidget(exit_button)
        buttons_gbox.setLayout(buttons_layout)
        grid.addWidget(buttons_gbox, 0, 0)

        log_text_gbox = QGroupBox()
        log_text_layout = QVBoxLayout()
        self.log_text_browser = QTextBrowser()
        log_text_layout.addWidget(self.log_text_browser)
        log_text_gbox.setLayout(log_text_layout)
        grid.addWidget(log_text_gbox, 0, 1)

        result_text_gbox = QGroupBox()
        result_text_layout = QVBoxLayout()
        self.result_text_browser = QTextBrowser()
        result_text_layout.addWidget(self.result_text_browser)
        result_text_gbox.setLayout(result_text_layout)
        grid.addWidget(result_text_gbox, 1, 0, 1, 2)

        self.setLayout(grid)