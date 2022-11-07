from .vwactions import VWPhysicalAction
from ...common.direction import Direction
from ...common.exceptions import VWMalformedActionException


class VWTurnAction(VWPhysicalAction):
    '''
    This class is a `VWPhysicalAction` that turns the `VWActor` in the specified direction.
    '''
    def __init__(self, direction: Direction) -> None:
        super(VWTurnAction, self).__init__()

        if not direction:
            raise VWMalformedActionException("No turning direction was specified")
        elif direction not in [Direction.left, Direction.right]:
            raise VWMalformedActionException("Invalid turning direction: {}.".format(direction))
        else:
            self.__direction: Direction = direction

    def get_turning_direction(self) -> Direction:
        '''
        Returns the turning direction of this `VWTurnAction` as a `Direction`.
        '''
        return self.__direction
