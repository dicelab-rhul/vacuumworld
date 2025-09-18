#!/usr/bin/env python3

from typing import Iterable

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vweffort import VWActionEffort
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.common.vworientation import VWOrientation
from vacuumworld.model.actions.vwturn_action import VWTurnAction
from vacuumworld.common.vwdirection import VWDirection


class MyMind(VWActorMindSurrogate):
    def __init__(self) -> None:
        super(MyMind, self).__init__()

        # Add here all the attributes you need/want.

        # Example of a target orientation set in advance
        self.__target_orientation: VWOrientation = VWOrientation.east

    def __turn_to_target(self) -> VWAction:
        if self.get_own_orientation() == self.__target_orientation:
            return VWIdleAction()
        elif self.get_own_orientation().get_left() == self.__target_orientation:
            return VWTurnAction(VWDirection.left)
        else:
            return VWTurnAction(VWDirection.right)

    def revise(self) -> None:
        # Do something with the observation, the messages, and the effort instead of simply storing/printing them.

        print(f"Observation:\n{self.get_latest_observation().pretty_format()}")
        print(f"Messages: {[str(m) for m in self.get_latest_received_messages()]}")
        print(f"Current effort since the beginning of the simulation: {self.get_effort()}.")

    def decide(self) -> Iterable[VWAction]:
        # Example of a sub-behaviour (you could simply
        # list here the behaviour of the function, but
        # you will not be able to reuse it).

        return [self.__turn_to_target()]


if __name__ == "__main__":
    run(default_mind=MyMind(), efforts=VWActionEffort.REASONABLE_EFFORTS)
