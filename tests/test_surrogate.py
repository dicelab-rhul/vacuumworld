#!/usr/bin/env python3

from unittest import main, TestCase
from typing import Iterable, Any
from inspect import getsourcefile
from pyoptional.pyoptional import PyOptional

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from vacuumworld import VacuumWorld
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.model.actor.mind.surrogate.vwhysteretic_mind_surrogate import VWHystereticMindSurrogate
from vacuumworld.common.vwcolour import VWColour
from vacuumworld.common.vwobservation import VWObservation
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction

import os


class TmpSurrogateMind(VWActorMindSurrogate):
    '''
    This class inherits from VWActorMindSurrogate and overrides the `revise()` and `decide()` methods.

    No malformed surrogate minds are tested here, as those are tested in the `test_illegal_run_inputs.py` file.
    '''
    def perceive(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None:
        '''
        This method ignores both `observation`, and each item of `messages`, and does nothing.
        '''
        ignore(observation)

        for message in messages:
            ignore(message)

    def decide(self) -> Iterable[VWAction]:
        '''
        This method always returns a `VWIdleAction`.
        '''
        return [VWIdleAction()]


# The various kinds of malformed surrogates are already tested in `test_illegal_run_inputs.py`.
class TestSurrogate(TestCase):
    '''
    This class tests:
    * The loading and validity of `VwHystereticMindSurrogate` objects.
    * The loading and validity of objects whose class is a custom subclass (in this case `TmpSurrogateMind`) of `VWActorSurrogateMind`.
    '''
    def __init__(self, args: Any) -> None:
        super(TestSurrogate, self).__init__(args)

    def test_load_hysteretic_surrogate(self) -> None:
        '''
        Tests the loading and validity of `VWHystereticMindSurrogate` objects.
        '''
        surrogate_file_path: PyOptional[str] = PyOptional.of_nullable(getsourcefile(VWHystereticMindSurrogate))

        self.assertTrue(surrogate_file_path.is_present())
        self.assertTrue(os.path.isfile(surrogate_file_path.or_else_raise()))

        surrogate_mind: VWActorMindSurrogate = VWActorMindSurrogate.load_from_file(surrogate_mind_file=surrogate_file_path.or_else_raise(), surrogate_mind_class_name=VWHystereticMindSurrogate.__name__)

        self.__test_load_surrogate(surrogate_mind=surrogate_mind)

    def test_load_surrogate(self) -> None:
        '''
        Tests the loading and validity of objects whose class is a custom subclass (in this case `TmpSurrogateMind`) of `VWActorSurrogateMind`.
        '''
        surrogate_mind: VWActorMindSurrogate = VWActorMindSurrogate.load_from_file(surrogate_mind_file=os.path.abspath(__file__), surrogate_mind_class_name=TmpSurrogateMind.__name__)

        self.__test_load_surrogate(surrogate_mind=surrogate_mind)

    def __test_load_surrogate(self, surrogate_mind: VWActorMindSurrogate) -> None:
        self.assertIsInstance(surrogate_mind, VWActorMindSurrogate)

        for colour in [c for c in VWColour if c != VWColour.user]:
            VWActorMindSurrogate.validate(mind=surrogate_mind, colour=colour, surrogate_mind_type=VacuumWorld.ALLOWED_RUN_ARGS["{}_mind".format(str(colour))])


if __name__ == '__main__':
    main()
