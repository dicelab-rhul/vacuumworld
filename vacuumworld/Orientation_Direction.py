
from enum import Enum, unique

@unique
class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
   
    
class Orientation(Enum):
    NORTH = "north"
    EAST="east"
    WEST = "west"
    SOUTH = "south"
    ALL="all"# -*- coding: utf-8 -*-

