#!/usr/bin/env python3

"""
This file was taken from the Linux PC in the lab.  Not sure at this time if this
is the optimal location for this file or what it is used for.  Just collecting all the
dependencies at this time.

"""

from dataclasses import dataclass
from typing import Callable

@dataclass
class GenericRequest():
    function: Callable
    args    : dict

@dataclass
class Object():
    x : int
    y : int
    z : int

