#!/usr/bin/env python3

from typing import Iterable, Tuple, Union, Optional

from pystarworldsturbo.common.message import BccMessage

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vwbroadcast_action import VWBroadcastAction
from vacuumworld.model.actions.vweffort import VWActionEffort
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.common.vwobservation import VWObservation


class MyMind(VWActorMindSurrogate):
    def __init__(self) -> None:
        super(MyMind, self).__init__()

        # Add here all the attributes you need/want.

    def revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None:
        # Do something with the observation, the messages, and the effort instead of simply storing/printing them.

        self.__observation: VWObservation = observation
        self.__latest_messages: Iterable[BccMessage] = messages
        self.__my_id: Optional[str] = self.__observation.get_observer_id()

        print("Observation:", self.__observation.pretty_format())
        print("Messages: {}".format([str(m) for m in self.__latest_messages]))
        print("Current effort since the beginning of the simulation: {}.".format(self.get_effort()))

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        # Replace this trivial decision process with something meaningful.
        if self.__my_id is not None:
            return VWIdleAction(), VWBroadcastAction(message="Hello!", sender_id=self.__my_id)
        else:
            return VWIdleAction()


if __name__ == "__main__":
    run(default_mind=MyMind(), efforts=VWActionEffort.REASONABLE_EFFORTS)
