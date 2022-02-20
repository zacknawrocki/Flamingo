from Assistant_Brain.speech_recognition import SpeechRecognition
from Assistant_Modules.lights import Lights
import urllib.request
import zipfile
import shutil
import os


def initialize_home():
    init_objs = dict()
    init_lights = Lights()
    init_objs["lights"] = init_lights
    # download default speech_recognition model, if not already downloaded, or
    # set model to user's preference
    setup_speech_recognition()
    return init_objs


def setup_speech_recognition():
    # Give default model, if no model downloaded
    if not os.path.isdir("Assistant_Brain/models/sr_model/"):
        sr_model_path = "Assistant_Brain/models/"
        sr_zip_path = f"{sr_model_path}sr_model.zip"
        model_url = "https://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.15.zip"
        urllib.request.urlretrieve(model_url, filename=sr_zip_path)
        with zipfile.ZipFile(sr_zip_path, 'r') as zip_ref:
            zip_ref.extractall(sr_model_path)
            # rename unzipped folder
            orig_sr_folder = f"{sr_model_path}vosk-model-small-en-us-0.15"
            new_sr_folder = f"{sr_model_path}sr_model"
            for file in os.listdir(orig_sr_folder):
                print(os.path.join(orig_sr_folder, file))
                print(new_sr_folder)
                shutil.move(os.path.join(orig_sr_folder, file), os.path.join(new_sr_folder, file))
            os.remove(sr_zip_path)
            os.rmdir(orig_sr_folder)


def main():
    init_objects = initialize_home()
    lights = init_objects["lights"]
    lights.lights_on()
    sr = SpeechRecognition()
    sr.start_listening()


if __name__ == '__main__':
    main()
