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
        # Do something with the observation, the messages, and the effort instead of simply storing/printing them.

        self.__observation: Observation = observation
        self.__latest_messages: Iterable[BccMessage] = messages
        self.__my_id: str = self.__observation.get_center().get_actor_appearance().get_id()

        print("Observation:", self.__observation.pretty_format())
        print("Messages: {}".format([str(m) for m in self.__latest_messages]))
        print("Current effort from the beginning of the simulation: {}.".format(self.get_effort()))

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        # VWSpeakAction and VWBroadcastAction will result in a failure if `sender_id` is not the same as the actor ID.
        return VWIdleAction(), VWBroadcastAction(message="Hello!", sender_id=self.__my_id)

        # Replace this trivial decision process with something meaningful.


if __name__ == "__main__":
    run(default_mind=MyMind(), efforts=ActionEffort.REASONABLE_EFFORTS)
