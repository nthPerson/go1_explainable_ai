#!/usr/bin/env python3

from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest
from snap import Snapper

def detect():
    snapper = Snapper()
    snapper.get_frame()
    return call_service(port=ServicePorts[ServiceNames.YOLO], 
                request=GenericRequest(
                    function="detect", 
                    # /home/dicelabs/dog_py/src/go/vision/current_frame.jpg
                    args={"filepath": "/home/dicelabs/dog_py/src/go/videos/person.jpeg"}
    ))

if __name__ == "__main__":
    print(detect())
