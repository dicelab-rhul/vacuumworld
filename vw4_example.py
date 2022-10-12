#!/usr/bin/env python3

from typing import Iterable, Tuple, Union

from pystarworldsturbo.common.message import BccMessage

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.idle_action import VWIdleAction
from vacuumworld.model.actor.actor_mind_surrogate import ActorMindSurrogate
from vacuumworld.common.observation import Observation



class MyMind(ActorMindSurrogate):
    def __init__(self) -> None:
        super(MyMind, self).__init__()

        # Add here all the attributes you need/want.

    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        # Do something with the observation and the messages, instead of printing them.

        print("Observation:", observation)
        print("Messages: {}".format([str(m) for m in messages]))

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        return VWIdleAction()
    
        # Replace this trivial decision process with something meaningful.
        
        
        
if __name__ == "__main__":
    run(default_mind=MyMind())
