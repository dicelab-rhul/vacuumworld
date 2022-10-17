#!/usr/bin/env python3

from typing import Iterable, Tuple, Union

from pystarworldsturbo.common.message import BccMessage

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.idle_action import VWIdleAction
from vacuumworld.model.actions.broadcast_action import VWBroadcastAction
from vacuumworld.model.actions.effort import ActionEffort
from vacuumworld.model.actor.actor_mind_surrogate import ActorMindSurrogate
from vacuumworld.common.observation import Observation


class MyMind(ActorMindSurrogate):
    def __init__(self) -> None:
        super(MyMind, self).__init__()

        # Add here all the attributes you need/want.

    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        # Do something with the observation, the messages, and the effort instead of simply printing them.

        print("Observation:", observation.pretty_format())
        print("Messages: {}".format([str(m) for m in messages]))
        print("Current effort from the beginning of the simulation: {}.".format(self.get_effort()))

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        return VWIdleAction(), VWBroadcastAction(message="Hello!", sender_id="HIDDEN")

        # Replace this trivial decision process with something meaningful.


if __name__ == "__main__":
    run(default_mind=MyMind(), efforts=ActionEffort.REASONABLE_EFFORTS)
