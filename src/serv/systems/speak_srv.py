#!/usr/bin/env python3

from multiprocessing import Process
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest
from server import start_server
from speech_processor import SpeechProcessor

def generic_callback(request: GenericRequest, detector: SpeechProcessor):
    function_call = getattr(detector, request.function)
    return function_call(**request.args)

def start_detector_server(name, port):
    processor = SpeechProcessor()
    try:
        start_server(name=name, port=port, callback=lambda request: generic_callback(request, processor))
    except Exception as e:
        print(e)

def start_detector(service_name, service_port):
    process = Process(target=start_detector_server, args=(service_name, service_port))
    process.start()
    try:
        process.join()
    except KeyboardInterrupt:
        ...

if __name__ == "__main__":
    start_detector(ServiceNames.SPEAK, ServicePorts[ServiceNames.SPEAK])
