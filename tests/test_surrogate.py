#!/usr/bin/env python3

from unittest import main, TestCase
from typing import Union, Tuple, Iterable
from inspect import getsourcefile

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.model.actor.mind.surrogate.vwhysteretic_mind_surrogate import VWHystereticMindSurrogate
from vacuumworld.common.vwcolour import VWColour
from vacuumworld.common.vwobservation import VWObservation
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction

import os


class TmpSurrogateMind(VWActorMindSurrogate):
    def revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None:
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
        surrogate_file_path: str = getsourcefile(VWHystereticMindSurrogate)

        self.assertTrue(os.path.isfile(surrogate_file_path))

        surrogate_mind: VWActorMindSurrogate = VWActorMindSurrogate.load_from_file(surrogate_mind_file=surrogate_file_path, surrogate_mind_class_name=VWHystereticMindSurrogate.__name__)

        self.__test_load_surrogate(surrogate_mind=surrogate_mind)

    def test_load_surrogate(self) -> None:
        surrogate_mind: VWActorMindSurrogate = VWActorMindSurrogate.load_from_file(surrogate_mind_file=os.path.abspath(__file__), surrogate_mind_class_name=TmpSurrogateMind.__name__)

        self.__test_load_surrogate(surrogate_mind=surrogate_mind)

    def __test_load_surrogate(self, surrogate_mind: VWActorMindSurrogate) -> None:
        self.assertIsInstance(surrogate_mind, VWActorMindSurrogate)

        for colour in [c for c in VWColour if c != VWColour.user]:
            VWActorMindSurrogate.validate(mind=surrogate_mind, colour=colour)


if __name__ == '__main__':
    main()
