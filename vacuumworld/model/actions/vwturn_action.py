from .vwactions import VWPhysicalAction
from ...common.vwdirection import VWDirection
from ...common.vwexceptions import VWMalformedActionException


class VWTurnAction(VWPhysicalAction):
    '''
    This class is a `VWPhysicalAction` that turns the `VWActor` in the specified direction.
    '''
    def __init__(self, direction: VWDirection) -> None:
        super(VWTurnAction, self).__init__()

        if not direction:
            raise VWMalformedActionException("No turning direction was specified")
        elif direction not in [VWDirection.left, VWDirection.right]:
            raise VWMalformedActionException(f"Invalid turning direction: {direction}.")
        else:
            self.__direction: VWDirection = direction

    def get_turning_direction(self) -> VWDirection:
        '''
        Returns the turning direction of this `VWTurnAction` as a `VWDirection`.
        '''
        return self.__direction
