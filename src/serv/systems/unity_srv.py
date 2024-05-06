#!/usr/bin/env python3

import subprocess
import signal
import os

INVOKE_PY_INTERPRETER = "python3"
angular_srv =   ["angular_srv.py"]
linear_srv =    ["linear_srv.py"]
vision_srv =    ["vision_srv.py"]
speech_srv =    ["speech_srv.py"]

def fork_processes(scripts):
    processes = []
    for script in scripts:
        process = subprocess.Popen(script)
        processes.append(process)
    return processes

def terminate_processes(processes):
    for process in processes:
        if process.poll() is None:  
            process.kill()  
    print("All child processes terminated.")

if __name__ == "__main__":
    scripts = [angular_srv, linear_srv, vision_srv, speech_srv]
    processes = fork_processes(scripts)

    def signal_handler(signum, frame):
        print("Received signal to terminate. Cleaning up...")
        terminate_processes(processes)
        os._exit(0)  

    signal.signal(signal.SIGINT, signal_handler)

    for process in processes:
        process.wait()
