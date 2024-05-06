#!/usr/bin/env python3

import pyttsx3
import subprocess

class SpeechProcessor():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate',125)

    def speak(self, string: str):
        self.engine.say(string)
        self.engine.save_to_file(string, '/home/dicelabs/dog_py/src/go/speech/temp.wav')
        self.engine.runAndWait()
        # self.send_to_dog()
    def send_to_dog(self):
        bash_script_path = "/home/dicelabs/dog_py/src/go/speech/dog_speak.sh"
        try:
            subprocess.run(['bash', bash_script_path], check=True)
            print("Bash script executed successfully")
        except subprocess.CalledProcessError as e:
            print("Error running Bash script:", e)

if __name__ == "__main__":
    processor = SpeechProcessor()
    processor.speak("I'm a robot talking dog, what else do you want bitch")