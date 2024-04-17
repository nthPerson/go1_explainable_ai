#!/usr/bin/env python3

from tcp_srv import TCPServer
from dataclasses import dataclass
from struct import unpack, calcsize
from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest

DOG_IP = '192.168.12.1'

if __name__ == "__main__":
    call_service(host=DOG_IP, port=ServicePorts[ServiceNames.GO], request=GenericRequest(function="stop", args={}))