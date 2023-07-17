import sys

from qt_modules import *

from window import *
from recorder import *
from recognition import *

class Dispatcher():
    def __init__(self):
        sys.path.append(os.getcwd())

        self.recognition = Recognition(self)
        self.recorder = Recorder(self)

        app = QApplication(sys.argv)
        self.window = Window(app, self)

        self.window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    Dispatcher()