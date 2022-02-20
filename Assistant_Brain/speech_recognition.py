from Assistant_Brain.interpret_speech import InterpretSpeech
import sounddevice as sd
import queue
import vosk
import sys


class SpeechRecognition:
    # Default model_path when called from main, optional path called below in main
    def __init__(self, model_path=f"Assistant_Brain/models/sr_model"):
        self.q = queue.Queue()
        self.model_path = model_path
        self.interpreter = InterpretSpeech()

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def start_listening(self):
        device = None
        device_info = sd.query_devices(device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        sample_rate = int(device_info['default_samplerate'])
        # Location of downloaded model from setup_speech_recognition
        model = vosk.Model(self.model_path)

        with sd.RawInputStream(samplerate=sample_rate, blocksize = 8000, device=device, dtype='int16',
                               channels=1, callback=self.callback):
            rec = vosk.KaldiRecognizer(model, sample_rate)
            while True:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    speech_result = rec.Result()
                    print(speech_result)
                    assistant_called = self.interpreter.wait_for_wakeword(speech_result)
                    if assistant_called:
                        self.interpreter.process_command(speech_result)
                else:
                    print(rec.PartialResult())
