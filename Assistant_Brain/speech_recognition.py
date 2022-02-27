from Assistant_Brain.interpret_speech import InterpretSpeech
from playsound import playsound
from pathlib import Path
import sounddevice as sd
import queue
import vosk
import time
import json
import sys


class SpeechRecognition:
    # Default model_path when called from main, optional path called below in main
    def __init__(self, flamingo_tools, model_path=f"Assistant_Brain/models/sr_model"):
        self.flamingo_tools = flamingo_tools
        self.q = queue.Queue()
        self.model_path = model_path
        self.interpreter = InterpretSpeech()
        self.device = None
        self.rec = None
        self.device_info = sd.query_devices(self.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        self.sample_rate = int(self.device_info['default_samplerate'])
        # Deactivate sound
        current_path = str(Path.cwd().parent)
        self.deactivate_file = "deactivate.m4a"
        self.deactivate_sound = f"{current_path}/Flamingo/files/audio/assistant_sfx/{self.deactivate_file}"
        # Location of downloaded model from setup_speech_recognition
        self.model = vosk.Model(self.model_path)
        # Time to listen for command (seconds)
        self.listen_time = 10

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def start_listening(self):
        with sd.RawInputStream(samplerate=self.sample_rate, blocksize=8000, device=self.device, dtype='int16',
                               channels=1, callback=self.callback):
            self.rec = vosk.KaldiRecognizer(self.model, self.sample_rate)
            while True:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    speech_result = self.rec.Result()
                    print(speech_result)
                    assistant_called = self.interpreter.wait_for_wakeword(speech_result)
                    if assistant_called:
                        self.listen_for_command()
                else:
                    print(self.rec.PartialResult())

    def listen_for_command(self):
        end_listening_tm = time.time() + self.listen_time
        while time.time() < end_listening_tm:
            data = self.q.get()
            if self.rec.AcceptWaveform(data):
                speech_result = self.rec.Result()
                if json.loads(speech_result)["text"] != "":
                    print(speech_result)
                    command_followed = self.interpreter.process_command(speech_result, self.flamingo_tools)
                    if command_followed:
                        return True

            else:
                print(self.rec.PartialResult())

        print("No full command given in time")
        playsound(self.deactivate_sound, block=False)

