from qt_modules import *

import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"

RECORD_TIME_IN_SECONDS = 5
EXTRA_RECORD_TIME_IN_SECONDS = RECORD_TIME_IN_SECONDS / 10

class Recorder():
    def __init__(self, dispatcher):
        super().__init__()
        self.dispatcher = dispatcher
        
        self.is_recording = False
        self.frames = []
        
        self.iters_count = int(RATE / CHUNK * RECORD_TIME_IN_SECONDS)
        self.counter = 0

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def start_recording(self):
        self.frames = []

        self.is_recording = True
        self.counter = 0
        self.dispatcher.window.timer.start(RECORD_TIME_IN_SECONDS + EXTRA_RECORD_TIME_IN_SECONDS)

    def stop_recording(self):
        self.dispatcher.window.log_text_browser.setText("Recording done!")
        self.is_recording = False
        self.dispatcher.window.timer.stop()
        QApplication.processEvents()
        self.save()
        QApplication.processEvents()
        self.dispatcher.recognition.run()
        QApplication.processEvents()
        
    def tick(self):
        if self.counter == 0 and self.is_recording:
            self.dispatcher.window.log_text_browser.setText("Recording in progress...")

        if self.counter < self.iters_count and self.is_recording:
            data = self.stream.read(CHUNK)
            self.frames.append(data)
            self.counter += 1

            if self.counter % 10 == 0:
                self.dispatcher.window.log_text_browser.setText("Recording in progress...")
                self.dispatcher.window.log_text_browser.append(f"{RECORD_TIME_IN_SECONDS - self.counter * CHUNK / RATE :.2f} seconds left")
                QApplication.processEvents()
        
        if self.counter >= self.iters_count and self.is_recording:
            self.stop_recording()

    def save(self):
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        self.dispatcher.window.log_text_browser.append("Saved successfully!")
