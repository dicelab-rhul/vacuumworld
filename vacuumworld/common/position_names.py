from __future__ import annotations
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
    def values() -> List[PositionNames]:
        '''
        Returns an ordered `List` of all the values of the enum.
        '''
        return [pn for pn in PositionNames]
