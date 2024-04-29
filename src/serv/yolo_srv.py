#!/usr/bin/env python3

from multiprocessing import Process
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest
from server import start_server
from yolo import PeopleDetector

def generic_callback(request: GenericRequest, detector: PeopleDetector):
    function_call = getattr(detector, request.function)
    return function_call(**request.args)

def start_detector_server(name, port):
    detector = PeopleDetector()
    opt = detector.parse_opt()
    model, names, imgsz, stride, save_dir, pt, vid_stride = detector.init(**vars(opt))
    try:
        start_server(name=name, port=port, callback=lambda request: generic_callback(request, detector))
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
    start_detector(ServiceNames.GO, ServicePorts[ServiceNames.GO])
