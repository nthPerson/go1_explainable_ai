#!/usr/bin/env python3

from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest

def speak(string: str):
    call_service(port=ServicePorts[ServiceNames.SPEAK], 
                request=GenericRequest(
                    function="speak", 
                    args={"string": string}
    ))

if __name__ == "__main__":
    speak("Hey")