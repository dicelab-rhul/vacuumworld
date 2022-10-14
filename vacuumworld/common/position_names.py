from enum import Enum


class PositionNames(Enum):
    center = "center"
    forward = "forward"
    left = "left"
    right = "right"
    forwardleft = "forwardleft"
    forwardright = "forwardright"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)
