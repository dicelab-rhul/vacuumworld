#!/usr/bin/env python3

from typing import Iterable, override

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwmove_action import VWMoveAction
from vacuumworld.model.actions.vwturn_action import VWTurnAction
from vacuumworld.model.actions.vwbroadcast_action import VWBroadcastAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.common.vwdirection import VWDirection
from vacuumworld.model.actions.vweffort import VWActionEffort
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate


class MyMind(VWActorMindSurrogate):
    '''
    A mind that bumps into walls.

    This is just for demonstration purposes. Ordinarily, you would want to avoid bumping into walls thanks to the `VWObservation` size and content.
    '''
    def __init__(self) -> None:
        super(MyMind, self).__init__()

        # Add here all the attributes you need/want.

    @override
    def revise(self) -> None:
        # Do something with the observation, the messages, and the effort instead of simply storing/printing them.

        print(f"Observation:\n{self.get_latest_observation().pretty_format()}")
        print(f"Messages: {[str(m) for m in self.get_latest_received_messages()]}")
        print(f"Current effort since the beginning of the simulation: {self.get_effort()}.")

    def __go_towards_east(self) -> Iterable[VWAction]:
        if self.get_own_appearance().is_facing_east():
            return [VWMoveAction()]
        elif self.get_own_appearance().is_facing_north():
            return [VWTurnAction(VWDirection.right)]
        else:
            return [VWTurnAction(VWDirection.left)]

    def __go_towards_south(self) -> Iterable[VWAction]:
        if self.get_own_appearance().is_facing_south():
            return [VWMoveAction()]
        elif self.get_own_appearance().is_facing_east():
            return [VWTurnAction(VWDirection.right)]
        else:
            return [VWTurnAction(VWDirection.left)]

    @override
    def decide(self) -> Iterable[VWAction]:
        if self.get_latest_observation().is_wall_immediately_ahead():
            return [VWIdleAction(), VWBroadcastAction(message="I am at the edge!", sender_id=self.get_own_id())]
        # The following is potentially unoptimal, because it does not take into account the orientation.
        elif self.get_own_position().get_x() > self.get_own_position().get_y():
            return self.__go_towards_east()
        else:
            return self.__go_towards_south()


if __name__ == "__main__":
    run(default_mind=MyMind(), efforts=VWActionEffort.REASONABLE_EFFORTS)
