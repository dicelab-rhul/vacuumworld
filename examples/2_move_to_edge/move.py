#!/usr/bin/env python3

from typing import Iterable

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwmove_action import VWMoveAction
from vacuumworld.model.actions.vwturn_action import VWTurnAction
from vacuumworld.common.vwdirection import VWDirection
from vacuumworld.model.actions.vweffort import VWActionEffort
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.common.vworientation import VWOrientation


class MyMind(VWActorMindSurrogate):
    def __init__(self) -> None:
        super(MyMind, self).__init__()

        # Add here all the attributes you need/want.

    def revise(self) -> None:
        # Do something with the observation, the messages, and the effort instead of simply storing/printing them.

        pass

    def __go_towards_east(self) -> Iterable[VWAction]:
        if self.get_own_orientation() == VWOrientation.east:
            return [VWMoveAction()]
        elif self.get_own_orientation() == VWOrientation.north:
            return [VWTurnAction(VWDirection.right)]
        else:
            return [VWTurnAction(VWDirection.left)]

    def __go_towards_south(self) -> Iterable[VWAction]:
        if self.get_own_orientation() == VWOrientation.south:
            return [VWMoveAction()]
        elif self.get_own_orientation() == VWOrientation.east:
            return [VWTurnAction(VWDirection.right)]
        else:
            return [VWTurnAction(VWDirection.left)]

    def decide(self) -> Iterable[VWAction]:
        if self.get_own_position().get_x() > self.get_own_position().get_y():
            return self.__go_towards_east()
        else:
            return self.__go_towards_south()


if __name__ == "__main__":
    run(default_mind=MyMind(), efforts=VWActionEffort.REASONABLE_EFFORTS)
