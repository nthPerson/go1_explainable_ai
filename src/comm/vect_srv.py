#!/usr/bin/env python3

from tcp_srv import TCPServer
from dataclasses import dataclass
from struct import unpack, calcsize
from client import call_service
from services import ServiceNames, ServicePorts
from req_resp import GenericRequest

DATA_REPRESENTATION = '3f' # Two Floats
PACKET_SIZE = calcsize(DATA_REPRESENTATION)
DOG_IP = '192.168.12.1'

@dataclass
class VectorStream():
    x : float
    z : float
    yaw: float

def print_data(msg: VectorStream):
    print(f"Received Message with x: {msg.x}, z: {msg.z} yaw: {-msg.yaw}")

def callback(data):
    x, z, yaw = unpack(DATA_REPRESENTATION, data)
    msg = VectorStream(x, z, yaw)
    print_data(msg)
    call_service(host=DOG_IP, port=ServicePorts[ServiceNames.GO], request=GenericRequest(function="vector", args={"x": .97*msg.z, "y": .97*msg.x, "yaw": -yaw}))

if __name__ == "__main__":
    tcp_server = TCPServer(port=7000, callback=lambda data: callback(data), payload_size=PACKET_SIZE)
    tcp_server.run()
