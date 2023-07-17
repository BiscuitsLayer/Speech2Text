import os

from qt_modules import *

import whisper

class Recognition():
    def __init__(self, dispatcher):
        super().__init__()
        self.dispatcher = dispatcher
        self.model = whisper.load_model("tiny")

    def run(self):
        try:
            result = self.model.transcribe(
                os.path.join(os.getcwd(), "output.wav"), fp16=False, language="ru"
            )
            self.dispatcher.window.result_text_browser.append(result["text"])
            QApplication.processEvents()
        except FileNotFoundError:
            self.dispatcher.window.result_text_browser.append("File not found exception OR you haven't installed ffmpeg")
            QApplication.processEvents()
        except Exception:
            self.dispatcher.window.result_text_browser.append("Unknown exception caught")
            QApplication.processEvents()