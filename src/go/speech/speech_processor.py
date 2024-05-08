#!/usr/bin/env python3

import pyttsx3
import subprocess

############################################################
"""
    String Literals For Bash Handling
"""
BASH_INTERPRETER    = 'bash'
BASH_SUCCESS        = "Bash script executed successfully"
BASH_ERROR          = "Error running Bash script:"
############################################################

############################################################
""" 
    - Trigger:  Bash Script to send signal to dog to play certain file already on dog (fast)
    - Send:     Bash Script to send custom wav file to dog to speak (slow)
"""
TRIGGER_WAV_SCRIPT = "/home/dicelabs/dog_py/src/go/speech/dog_trigger_speech.sh"
SEND_WAV_SCRIPT = "/home/dicelabs/dog_py/src/go/speech/dog_send_speech.sh"
############################################################

def send_signal_to_dog(filename: str):
    """ 
        Filename is a file already on the dog that you would like to trigger it to play
    """
    try:
        subprocess.run([BASH_INTERPRETER, TRIGGER_WAV_SCRIPT], args=[filename], check=True)
        print(BASH_SUCCESS)
    except subprocess.CalledProcessError as e:
        print(BASH_ERROR, e)

def send_file_to_dog():
    try:
        subprocess.run([BASH_INTERPRETER, SEND_WAV_SCRIPT], check=True)
        print(BASH_SUCCESS)
    except subprocess.CalledProcessError as e:
        print(BASH_ERROR, e)

############################################################
"""     
    This file is used to store a custom message, after language processing creates the wav file it saves it here,
    Then to send to the dog this file is referenced in the bash script to scp over to the dog's computer 
"""
TEMPORARY_WAV_FILE = '/home/dicelabs/dog_py/src/go/speech/waves/temp.wav'
############################################################

class SpeechProcessor():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate',125)

    def speak(self, phrase: str, file: str=TEMPORARY_WAV_FILE, custom_phrase: bool=False):
        self.engine.say(phrase)
        self.engine.save_to_file(phrase, file)
        self.engine.runAndWait()
        if custom_phrase:
            send_file_to_dog()
        else:
            if phrase == "Going To Next Target":
                send_signal_to_dog("target.wav")
            elif phrase == "Entering Search State":
                send_signal_to_dog("search.wav")
            elif phrase == "Human Detected":
                send_signal_to_dog("human.wav")
            elif phrase == "Starting Activity Recognition":
                send_signal_to_dog("activity.wav")

if __name__ == "__main__":
    processor = SpeechProcessor()
    processor.speak("Human Detected")