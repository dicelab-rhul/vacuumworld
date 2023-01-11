from __future__ import annotations
from enum import Enum
from typing import List


class VWPositionNames(Enum):
    '''
    This `Enum` specifies names for different positions in the context of a `VWObservation` received by by a `VWActor`.
    * `center` refers to the `VWActor` positon.
    * `forward` refers to the position in front of the `VWActor` positon.
    * `left` refers to the position to the left of the `VWActor` positon.
    * `right` refers to the position to the right of the `VWActor` positon.
    * `forwardleft` refers to the position to the forward-left of the `VWActor` positon.
    * `forwardright` refers to the position to the forward-right of the `VWActor` positon.
    '''
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

    @staticmethod
    def values() -> List[VWPositionNames]:
        '''
        Returns an ordered `List` of all the values of the `Enum`.
        '''
        return [pn for pn in VWPositionNames]

    @staticmethod
    def values_in_order() -> List[VWPositionNames]:
        '''
        Returns an ordered `List` of all the values of this `Enum`.

        The order is as follows:
        * `VWPositionNames.center`
        * `VWPositionNames.forward`
        * `VWPositionNames.left`
        * `VWPositionNames.right`
        * `VWPositionNames.forwardleft`
        * `VWPositionNames.forwardright`
        '''
        return [VWPositionNames.center, VWPositionNames.forward, VWPositionNames.left, VWPositionNames.right, VWPositionNames.forwardleft, VWPositionNames.forwardright]
