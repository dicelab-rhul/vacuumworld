from enum import Enum


class VWDirection(Enum):
    '''
    This `Enum` specifies turning directions, and relations between `VWOrientation` objects.

    * `left` refers to a left/counterclockwise turn.
    * `right`refers to a right/clockwise turn.
    '''
    left = "left"
    right = "right"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)