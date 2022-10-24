from enum import Enum
from typing import List


class PositionNames(Enum):
    center = "center"
    left = "left"
    right = "right"
    forward = "forward"
    forwardleft = "forwardleft"
    forwardright = "forwardright"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def values() -> List["PositionNames"]:
        return [pn for pn in PositionNames]
