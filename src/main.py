import pyaudio
import wave

import sys
from PySide2.QtWidgets import QApplication, QPushButton, QWidget, QTextBrowser
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QGridLayout

import whisper
import sys, os

BIG_BUTTON_HSIZE = 200
BIG_BUTTON_VSIZE = 60

EXIT_BUTTON_HSIZE = 150
EXIT_BUTTON_VSIZE = 60

class Recognition():
    def __init__(self):
        self.model = whisper.load_model("tiny")

    def set_result_text_browser(self, result_text_browser):
        self.result_text_browser = result_text_browser

    def run(self):
        try:
            result = self.model.transcribe(
                os.path.join(os.getcwd(), "output.wav"),
                decode_options={"fp16": False, "language": "ru"}
            )
            self.result_text_browser.append(result["text"])
            QApplication.processEvents()
        except FileNotFoundError:
            self.result_text_browser.append("File not found exception OR you haven't installed ffmpeg")
            QApplication.processEvents()
        except Exception as e:
            self.result_text_browser.append("Unknown exception caught")
            QApplication.processEvents()
            self.result_text_browser.append(e.with_traceback)
            QApplication.processEvents()
            exit()

class Recorder():
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.WAVE_OUTPUT_FILENAME = "output.wav"
        self.RECORD_SECONDS = 5
        
        self.is_recording = False
        self.frames = []
        
        self.iters_count = int(self.RATE / self.CHUNK * self.RECORD_SECONDS)
        self.counter = 0

        self.recognition = Recognition()

    def set_log_text_browser(self, log_text_browser):
        self.log_text_browser = log_text_browser

    def set_result_text_browser(self, result_text_browser):
        self.recognition.set_result_text_browser(result_text_browser)

    def prepare(self):
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK)
        
    def tear_down(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def start_recording(self):
        self.prepare()
        self.is_recording = True
        self.counter = 0

    def stop_recording(self):
        self.log_text_browser.setText("Recording done!")
        self.is_recording = False
        
    def tick(self):
        if self.counter == 0 and self.is_recording:
            self.log_text_browser.setText("Recording in progress...")

        if self.counter < self.iters_count and self.is_recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            self.counter += 1

            if self.counter % 30 == 0:
                self.log_text_browser.setText("Recording in progress...")
                self.log_text_browser.append(f"{self.RECORD_SECONDS - self.counter * self.CHUNK / self.RATE :.2f} seconds left")
                QApplication.processEvents()
        
        if self.counter >= self.iters_count and self.is_recording:
            self.stop_recording()
            QApplication.processEvents()
            self.save()
            QApplication.processEvents()
            self.recognition.run()
            QApplication.processEvents()
            self.tear_down()

    def save(self):
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        self.log_text_browser.append("Saved successfully!")


class Window(QWidget):
    def __init__(self, app, recorder, parent=None):
        super().__init__(parent)

        start_recording_button = QPushButton(
            text='Start recording',
            parent=self
        )
        start_recording_button.clicked.connect(recorder.start_recording)
        start_recording_button.setFixedSize(BIG_BUTTON_HSIZE, BIG_BUTTON_VSIZE)

        stop_recording_button = QPushButton(
            text='Stop recording', 
            parent=self
        )
        stop_recording_button.clicked.connect(recorder.stop_recording)
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
        recorder.set_log_text_browser(self.log_text_browser)
        log_text_layout.addWidget(self.log_text_browser)
        log_text_gbox.setLayout(log_text_layout)
        grid.addWidget(log_text_gbox, 0, 1)

        result_text_gbox = QGroupBox()
        result_text_layout = QVBoxLayout()
        self.result_text_browser = QTextBrowser()
        recorder.set_result_text_browser(self.result_text_browser)
        result_text_layout.addWidget(self.result_text_browser)
        result_text_gbox.setLayout(result_text_layout)
        grid.addWidget(result_text_gbox, 1, 0, 1, 2)

        self.setLayout(grid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    recorder = Recorder()

    window = Window(app, recorder)
    window.show()

    sys.path.append(os.getcwd())

    QApplication.processEvents()
    frame_counter = 0
    while True:
        recorder.tick()
        if frame_counter % 3 == 0:
            QApplication.processEvents()

        frame_counter += 1
        # sys.exit(app.exec_())
