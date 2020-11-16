from .vwactions import VWPhysicalAction
from ...common.direction import Direction
from ...utils.exceptions import VWMalformedActionException



class VWTurnAction(VWPhysicalAction):
    def __init__(self, direction: Direction) -> None:
        super(VWTurnAction, self).__init__()

        if not direction:
            raise VWMalformedActionException("No turning direction was specified")
        elif not direction in [Direction.left, Direction.right]:
            raise VWMalformedActionException("Invalid turning direction: {}.".format(direction))
        else:
            self.__direction: Direction = direction

    def get_turning_direction(self) -> Direction:
        return self.__direction
