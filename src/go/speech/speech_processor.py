#!/usr/bin/env python3

import pyttsx3
import subprocess

CUSTOM_PHRASE = 0

class SpeechProcessor():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate',125)

    def speak(self, phrase: str, file: str='/home/dicelabs/dog_py/src/go/speech/temp.wav'):
        self.engine.say(phrase)
        self.engine.save_to_file(phrase, file)
        self.engine.runAndWait()
        if CUSTOM_PHRASE:
            self.send_file_to_dog()
        else:
            if phrase == "Going To Next Target":
                self.send_signal_to_dog("target.wav")
            elif phrase == "Entering Search State":
                self.send_signal_to_dog("search.wav")
            elif phrase == "Human Detected":
                self.send_signal_to_dog("human.wav")
            elif phrase == "Starting Activity Recognition":
                self.send_signal_to_dog("activity.wav")

    def send_signal_to_dog(filename):
        bash_script_path = "/home/dicelabs/dog_py/src/go/speech/dog_say.sh"
        try:
            subprocess.run(['bash', bash_script_path], args=[filename], check=True)
            print("Bash script executed successfully")
        except subprocess.CalledProcessError as e:
            print("Error running Bash script:", e)

    def send_file_to_dog(self):
        bash_script_path = "/home/dicelabs/dog_py/src/go/speech/dog_speak.sh"
        try:
            subprocess.run(['bash', bash_script_path], check=True)
            print("Bash script executed successfully")
        except subprocess.CalledProcessError as e:
            print("Error running Bash script:", e)

if __name__ == "__main__":
    processor = SpeechProcessor()
    processor.speak("Human Detected")