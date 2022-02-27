from playsound import playsound
from pathlib import Path
from gtts import gTTS
import json
import os


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

    def process_command(self, voice_command, flamingo_tools):
        command = json.loads(voice_command)
        command_followed = False
        print(f"Flamingo received this command: {command['text']}")

        # For now, just test out some light commands
        lights = flamingo_tools["lights"]
        weather = flamingo_tools["weather"]

        if "on" in voice_command:
            lights.lights_on()
            command_followed = True
        if "off" in voice_command:
            lights.lights_off()
            command_followed = True
        if "weather" in voice_command:
            self.respond(weather.get_current_weather_response())
            command_followed = True

        return command_followed

    def respond(self, response_text):
        response = gTTS(response_text)
        response.save(".response.mp3")
        playsound(".response.mp3", block=False)
        os.remove(".response.mp3")



