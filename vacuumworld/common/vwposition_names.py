from __future__ import annotations
from enum import Enum


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

    @classmethod
    def elements(cls) -> list[VWPositionNames]:
        '''
        Returns a `list` of all the elements of this `Enum`.
        '''
        return list(cls)

    @classmethod
    def values(cls) -> list[str]:
        '''
        Returns a `list` of all the values of this `Enum`.
        '''
        return [position_name.value for position_name in cls]

    @staticmethod
    def elements_in_order() -> list[VWPositionNames]:
        '''
        Returns an ordered `list` of all the elements of this `Enum`.

        The order is as follows:
        * `VWPositionNames.center`
        * `VWPositionNames.forward`
        * `VWPositionNames.left`
        * `VWPositionNames.right`
        * `VWPositionNames.forwardleft`
        * `VWPositionNames.forwardright`
        '''
        return [VWPositionNames.center, VWPositionNames.forward, VWPositionNames.left, VWPositionNames.right, VWPositionNames.forwardleft, VWPositionNames.forwardright]
