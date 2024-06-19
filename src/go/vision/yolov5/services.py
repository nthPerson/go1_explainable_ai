#!/usr/bin/env python3

"""
This file was taken from the Linux PC in the lab.  Not sure at this time if this
is the optimal location for this file or what it is used for.  Just collecting all the
dependencies at this time.

"""

class ServiceNames():
    GO = "GO"
    YOLO = "YOLO"
    SPEAK = "SPEAK"

ServicePorts = {
    ServiceNames.GO:   6001,
    ServiceNames.YOLO: 6002,
    ServiceNames.SPEAK: 6003
}