from .vwactions import VWPhysicalAction
from ..actor.vwactor_appearance import VWActorAppearance
from ...common.direction import Direction
from ...utils.exceptions import VWMalformedActionException



class VWTurnAction(VWPhysicalAction):
    def __init__(self, direction: Direction, actor_appearance: VWActorAppearance) -> None:
        super(VWTurnAction, self).__init__(actor_appearance=actor_appearance)

        if not direction:
            raise VWMalformedActionException("No direction was specified")
        elif not direction in [Direction.left, Direction.right]:
            raise VWMalformedActionException("Invalid turning direction: {}.".format(direction))
        else:
            self.__direction: Direction = direction

    def get_turning_direction(self) -> Direction:
        return self.__direction
