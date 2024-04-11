#!/usr/bin/env python3

from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest

def turn(vel):
    call_service(port=ServicePorts[ServiceNames.STATEMACHINE], request=GenericRequest(function="turn", args={"vel": vel}))

def walk(vel):
    call_service(port=ServicePorts[ServiceNames.STATEMACHINE], request=GenericRequest(function="walk", args={"vel": vel}))

def vect(x, y):
    call_service(port=ServicePorts[ServiceNames.STATEMACHINE], request=GenericRequest(function="vect", args={"x": x, "y": y}))

def stop():
    call_service(port=ServicePorts[ServiceNames.STATEMACHINE], request=GenericRequest(function="stop", args={}))

