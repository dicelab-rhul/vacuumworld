#!/usr/bin/env python3

from unittest import main, TestCase
from typing import Union, Tuple, Iterable

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from vacuumworld.model.actor.actor_mind_surrogate import ActorMindSurrogate
from vacuumworld.model.actor.hystereticmindsurrogate import VWHystereticMindSurrogate
from vacuumworld.common.colour import Colour
from vacuumworld.common.observation import Observation
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.idle_action import VWIdleAction

import os


class TmpSurrogateMind(ActorMindSurrogate):
    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        ignore(observation)

        for message in messages:
            ignore(message)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        return VWIdleAction()


# The various kinds of malformed surrogates are already tested in `test_illegal_run_inputs.py`.
class TestSurrogate(TestCase):
    def __init__(self, args) -> None:
        super(TestSurrogate, self).__init__(args)

    def test_load_hysteretic_surrogate(self) -> None:
        surrogate_file_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vacuumworld", "model", "actor", "hystereticmindsurrogate.py")

        self.assertTrue(os.path.isfile(surrogate_file_path))

        surrogate_mind: ActorMindSurrogate = ActorMindSurrogate.load_from_file(surrogate_mind_file=surrogate_file_path, surrogate_mind_class_name=VWHystereticMindSurrogate.__name__)

        self.__test_load_surrogate(surrogate_mind=surrogate_mind)

    def test_load_surrogate(self) -> None:
        surrogate_mind: ActorMindSurrogate = ActorMindSurrogate.load_from_file(surrogate_mind_file=os.path.abspath(__file__), surrogate_mind_class_name=TmpSurrogateMind.__name__)

        self.__test_load_surrogate(surrogate_mind=surrogate_mind)

    def __test_load_surrogate(self, surrogate_mind: ActorMindSurrogate) -> None:
        self.assertIsInstance(surrogate_mind, ActorMindSurrogate)

        for colour in [c for c in Colour if c != Colour.user]:
            ActorMindSurrogate.validate(mind=surrogate_mind, colour=colour)


if __name__ == '__main__':
    main()
