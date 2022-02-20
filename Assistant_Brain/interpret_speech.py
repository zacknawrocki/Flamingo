from playsound import playsound
from pathlib import Path
import json


class InterpretSpeech:
    # Default model_path when called from main, optional path called below in main
    def __init__(self):
        self.wakeword = "hey"
        current_path = str(Path.cwd().parent)
        self.activate_file = "activate.m4a"
        self.activate_sound = f"{current_path}/Flamingo/files/audio/assistant_sfx/{self.activate_file}"
        print(self.activate_sound)

    def wait_for_wakeword(self, voice_text):
        voice_text = json.loads(voice_text)
        assistant_called = False
        if self.wakeword in voice_text["text"]:
            print("Voice assistant activated")
            playsound(self.activate_sound, block=False)
            assistant_called = True
        return assistant_called

    def process_command(self, voice_command):
        command = json.loads(voice_command)
        print(command["text"])

