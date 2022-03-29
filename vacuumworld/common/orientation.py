from __future__ import annotations
from enum import Enum

from .direction import Direction



class Orientation(Enum):
    north = "north"
    east = "east"
    south = "south"
    west = "west"

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)

    def get_left(self) -> Orientation:
        if self == Orientation.north:
            return Orientation.west
        elif self == Orientation.south:
            return Orientation.east
        elif self == Orientation.west:
            return Orientation.south
        else:
            return Orientation.north

    def get_right(self) -> Orientation:
        if self == Orientation.north:
            return Orientation.east
        elif self == Orientation.south:
            return Orientation.west
        elif self == Orientation.west:
            return Orientation.north
        else:
            return Orientation.south
        
    def get_opposite(self) -> Orientation:
        if self == Orientation.north:
            return Orientation.south
        elif self == Orientation.south:
            return Orientation.north
        elif self == Orientation.west:
            return Orientation.east
        else:
            return Orientation.west

    def get(self, direction: Direction) -> Orientation:
        if direction == Direction.left:
            return self.get_left()
        else:
            return self.get_right()

    left: Orientation = get_left
    right: Orientation = get_right
