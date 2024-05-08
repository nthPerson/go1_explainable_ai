#!/usr/bin/env python3

from forker import Forker

if __name__ == "__main__":
    Forker.run_scripts(
        [
            "unity_srv.py",
            "speak_srv.py",
            "ar_srv.py"
        ]
    )