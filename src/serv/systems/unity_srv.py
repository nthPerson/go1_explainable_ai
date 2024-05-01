#!/usr/bin/env python3

import subprocess
from pynput import keyboard

INVOKE_PY_INTERPRETER = "python3"
angular_srv =   ["angular_srv.py"]
linear_srv =    ["linear_srv.py"]
vision_srv =    ["vision_srv.py"]
EXIT_KEY = 'c'

def key_valid(key):
     return hasattr(key, 'char') and key.char is not None

def on_key_press(key, processes):
    if key_valid(key):
        if key.char == EXIT_KEY:
            for pid in processes:
                pid.kill()
            return False # Exit

def fork_processes(scripts):
    processes=[]
    for script in scripts:
        process = subprocess.Popen(script)
        processes.append(process)
    return processes

if __name__ == "__main__":
    scripts = [angular_srv, linear_srv, vision_srv]
    processes = fork_processes(scripts)
    with keyboard.Listener(
        on_press=lambda key: on_key_press(key, processes)
    ) as listener:
        listener.join()