#!/usr/bin/env python3

from multiprocessing import Process
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest
from server import start_server
from go import Go1

def generic_callback(request: GenericRequest, go: Go1):
    function_call = getattr(go, request.function)
    function_call(**request.args)

def start_go_server(name, port):
    go = Go1()
    start_server(name=name, port=port, callback=lambda request: generic_callback(request, go))
    go.shutdown()

def start_go(service_name, service_port):
    process = Process(target=start_go_server, args=(service_name, service_port))
    process.start()
    try:
        process.join()
    except KeyboardInterrupt:
        ...

if __name__ == "__main__":
    start_go(ServiceNames.GO, ServicePorts[ServiceNames.GO])
