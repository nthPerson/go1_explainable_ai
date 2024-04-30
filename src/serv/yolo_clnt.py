#!/usr/bin/env python3

from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest
from time import sleep

def detect(filepath: str):
    return call_service(port=ServicePorts[ServiceNames.YOLO], 
                request=GenericRequest(
                    function="detect", 
                    args={"filepath": filepath}
    ))

if __name__ == "__main__":
    while True:
        print("person detected") if detect("/home/dicelabs/dog_py/src/go/vision/current_frame.jpg") else ...
        sleep(.1)