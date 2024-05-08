#!/usr/bin/env python3

from forker import Forker

if __name__ == "__main__":
    Forker.run_scripts(
        [
            "angular_srv.py",
            "linear_srv.py",
            "vision_srv.py",
            "speech_srv.py"
        ]
    )
