#!/usr/bin/env python3

from typing import Iterable, Tuple, Union

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from vacuumworld import run
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwmove_action import VWMoveAction
from vacuumworld.model.actions.vwturn_action import VWTurnAction
from vacuumworld.common.vwobservation import VWObservation
from vacuumworld.common.vwdirection import VWDirection


class MyMind(VWActorMindSurrogate):
    '''
    The goal of this surrogate mind is to find any corner of the grid.
    '''

    def __init__(self) -> None:
        super(MyMind, self).__init__()

        self.__corner_found: bool = False

    def revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None:
        # We store our observation.
        self.__observation: VWObservation = observation

        for message in messages:
            ignore(message)

        if not self.__corner_found and self.__observation.get_center().is_corner():
            print(f"I found a corner at {self.__observation.get_center().get_coord()}. I'm staying idle from now on.")

            self.__corner_found = True

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        # If we've found a corner, don't do anything else.
        if self.__corner_found:
            return VWIdleAction()
        # If we can see a wall one step ahead, but no wall to the left, turn right.
        elif self.__observation.is_wall_one_step_ahead() and not self.__observation.is_wall_immediately_to_the_left():
            return VWTurnAction(VWDirection.right)
        # If we can see a wall one step ahead, but no wall to the right, turn left.
        elif self.__observation.is_wall_one_step_ahead() and not self.__observation.is_wall_immediately_to_the_right():
            return VWTurnAction(VWDirection.left)
        # If we can see a wall directly ahead, but no wall to the left, turn right.
        elif self.__observation.is_wall_immediately_ahead() and not self.__observation.is_wall_immediately_to_the_left():
            return VWTurnAction(VWDirection.right)
        # If we can see a wall directly ahead, but no wall to the right, turn left.
        elif self.__observation.is_wall_immediately_ahead() and not self.__observation.is_wall_immediately_to_the_right():
            return VWTurnAction(VWDirection.left)
        # Otherwise move forward.
        else:
            return VWMoveAction()


if __name__ == "__main__":
    run(default_mind=MyMind(), skip=True)
