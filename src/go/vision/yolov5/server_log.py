#!/usr/bin/env python3

"""
This file was taken from the Linux PC in the lab.  Not sure at this time if this
is the optimal location for this file or what it is used for.  Just collecting all the
dependencies at this time.

"""

class Logging():
    @staticmethod
    def log_server_active_message(name: str, host: str, port: str):
        print(f"{name} Server is Up and Running on {host}:{port}")

    @staticmethod
    def log_connection_message(addr):
        print(f"Connected by {addr}")

    @staticmethod
    def log_data_rcv_message(name):
        print(f"Received Data From {name} Client")