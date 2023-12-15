from __future__ import annotations
from enum import Enum
from random import choice

from .vwdirection import VWDirection
from .vwvalidator import VWValidator


class VWOrientation(Enum):
    '''
    This `Enum` specifies both cardinal points, and absolute orientations related to such points.

    * `north` refers to the North cardinal point, and a northern orientation.

    * `south` refers to the South cardinal point, and a southern orientation.

    * `west` refers to the West cardinal point, and a western orientation.

    * `east` refers to the East cardinal point, and a eastern orientation.
    '''
    north = "north"
    south = "south"
    west = "west"
    east = "east"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)

    def get_left(self) -> VWOrientation:
        '''
        Returns the `VWOrientation` to the `left` of this `VWOrientation`.
        '''
        if self == VWOrientation.north:
            return VWOrientation.west
        elif self == VWOrientation.south:
            return VWOrientation.east
        elif self == VWOrientation.west:
            return VWOrientation.south
        else:
            return VWOrientation.north

    def get_right(self) -> VWOrientation:
        '''
        Returns the `VWOrientation` to the `right` of this `VWOrientation`.
        '''
        if self == VWOrientation.north:
            return VWOrientation.east
        elif self == VWOrientation.south:
            return VWOrientation.west
        elif self == VWOrientation.west:
            return VWOrientation.north
        else:
            return VWOrientation.south

    def get_opposite(self) -> VWOrientation:
        '''
        Returns the `VWOrientation` opposite to this `VWOrientation`.
        '''
        if self == VWOrientation.north:
            return VWOrientation.south
        elif self == VWOrientation.south:
            return VWOrientation.north
        elif self == VWOrientation.west:
            return VWOrientation.east
        else:
            return VWOrientation.west

    def get(self, direction: VWDirection) -> VWOrientation:
        '''
        Returns the `VWOrientation` to the `left` or `right` of this `VWOrientation`, depending on the value of `direction`.
        '''
        VWValidator.validate_not_none(direction)
        VWValidator.validate_type(VWDirection, direction)

        if direction == VWDirection.left:
            return self.get_left()
        else:
            return self.get_right()

    def matches(self, orientation: VWOrientation) -> bool:
        '''
        Returns `True` if this `VWOrientation` matches `orientation`.
        '''
        VWValidator.validate_not_none(orientation)
        VWValidator.validate_type(VWOrientation, orientation)

        return self == orientation

    def distance_from(self, orientation: VWOrientation) -> int:
        '''
        Returns the minimum distance (in 90-degree turns) from this `VWOrientation` to `orientation`.

        * If `self` and `orientation` are the same, the distance is `0`.
        * If `self` and `orientation` are opposite, the distance is `2`.
        * Otherwise, the distance is `1`.
        '''
        VWValidator.validate_not_none(orientation)
        VWValidator.validate_type(VWOrientation, orientation)

        if self == orientation:
            return 0
        elif self.get_left() == orientation or self.get_right() == orientation:
            return 1
        else:
            return 2

    @staticmethod
    def random() -> VWOrientation:
        '''
        Returns a random `VWOrientation`.
        '''
        return choice(list(VWOrientation))

    @classmethod
    def values(cls) -> list[str]:
        '''
        Returns a `list` of all the values of this `Enum`.
        '''
        return [orientation.value for orientation in cls]
