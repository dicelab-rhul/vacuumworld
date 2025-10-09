#!/usr/bin/env python3

from typing import Iterable, override

from vacuumworld import run
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vwmove_action import VWMoveAction
from vacuumworld.model.actions.vwturn_action import VWTurnAction
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.common.vwdirection import VWDirection


class MyMind(VWActorMindSurrogate):
    '''
    The goal of this surrogate mind is to make the actor directly face the western wall.

    This is just for demonstration purposes. Ordinarily, you would want to avoid bumping into walls thanks to the `VWObservation` size and content.
    '''

    def __init__(self) -> None:
        super(MyMind, self).__init__()

        self.__facing_left_wall: bool = False

    @override
    def revise(self) -> None:
        # We are done.
        if not self.__facing_left_wall and self.get_own_appearance().is_facing_west() and self.get_latest_observation().is_wall_immediately_ahead():
            print("I am at the western wall - success!")

            self.__facing_left_wall = True
        # One more step.
        elif not self.__facing_left_wall and self.get_own_appearance().is_facing_west() and self.get_latest_observation().is_wall_one_step_ahead():
            print("Almost there! One more step and I'll be at the western wall.")

    @override
    def decide(self) -> Iterable[VWAction]:
        # Once we have found the western wall, we remain idle.
        if self.__facing_left_wall:
            return [VWIdleAction()]
        # If we are heading the right way, move forward (in search of a wall).
        elif self.get_own_appearance().is_facing_west():
            return [VWMoveAction()]
        # If we are facing north, turn left.
        elif self.get_own_appearance().is_facing_north():
            return [VWTurnAction(VWDirection.left)]
        # Otherwise (i.e., facing east or south), turn right.
        else:
            return [VWTurnAction(VWDirection.right)]


if __name__ == "__main__":
    run(default_mind=MyMind(), skip=True)
