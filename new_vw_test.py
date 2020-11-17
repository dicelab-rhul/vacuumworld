#!/usr/bin/env python3

from typing import Iterable, Tuple, Union
from time import time_ns

from pystarworldsturbo.common.message import BccMessage

from vacuumworld import run
from vacuumworld.common.direction import Direction
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.idle_action import VWIdleAction
from vacuumworld.model.actions.turn_action import VWTurnAction
from vacuumworld.model.actions.move_action import VWMoveAction
from vacuumworld.model.actions.clean_action import VWCleanAction
from vacuumworld.model.actions.drop_action import VWDropAction
from vacuumworld.model.actions.speak_action import VWSpeakAction
from vacuumworld.model.actions.broadcast_action import VWBroadcastAction
from vacuumworld.model.actor.actor_mind_surrogate import ActorMindSurrogate
from vacuumworld.common.observation import Observation




class MyMind(ActorMindSurrogate):
    def __init__(self) -> None:
        super(MyMind, self).__init__()

        # Add here all the class attributes you may need.

    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        # Do something with the observation and the messages.
        print("Observation:", observation)
        print("Messages: {}".format([str(m) for m in messages]))

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        return VWIdleAction()


run(default_mind=MyMind(), skip=True)
