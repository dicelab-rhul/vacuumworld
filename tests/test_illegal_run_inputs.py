#!/usr/bin/env python3

from unittest import main, TestCase
from typing import Iterable, Union, Tuple, List, Dict, Type

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from vacuumworld import VacuumWorld, run
from vacuumworld.common.colour import Colour
from vacuumworld.common.observation import Observation
from vacuumworld.gui.gui import VWGUI
from vacuumworld.model.actor.hystereticmindsurrogate import VWHystereticMindSurrogate
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.idle_action import VWIdleAction


class EmptySurrogateMind():
    pass


class NoDecideSurrogateMind():
    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        ignore(self)
        ignore(observation)

        for m in messages:
            ignore(m)


class NoReviseSurrogateMind():
    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        return VWIdleAction()


class MalformedReviseSurrogateMind():
    def revise(self, observation: Observation, messages: Iterable[BccMessage], nonsense: List[str]) -> None:
        ignore(self)
        ignore(observation)

        for m in messages:
            ignore(m)

        for elm in nonsense:
            ignore(elm)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        return VWIdleAction()


class NoMessagesMalformedReviseSurrogateMind():
    def revise(self, observation: Observation) -> None:
        ignore(self)
        ignore(observation)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        return VWIdleAction()


class NoObservationMalformedReviseSurrogateMind():
    def revise(self, messages: Iterable[BccMessage]) -> None:
        ignore(self)

        for m in messages:
            ignore(m)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        return VWIdleAction()


class MalformedDecideSurrogateMind():
    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        ignore(self)
        ignore(observation)

        for m in messages:
            ignore(m)

    def decide(self, nonsense: List[str]) -> Union[VWAction, Tuple[VWAction]]:
        for elm in nonsense:
            ignore(elm)

        return VWIdleAction()


# TODO: this class needs to be rewritten, because of the new `VWGUIRunner` and `VWGUIlessRunner` classes.
class TestIllegalRunInputs(TestCase):
    '''
    All the arguments of `run()` that are not tested are simply ignored if they are not valid.

    All unknown arguments of `run()` are ignored by the system.
    '''

    def test_illegal_speed_value(self) -> None:
        for value in [-1, -0.3, 1.1, 2, 3, 100, 1000]:
            self.assertRaises(ValueError, VWGUI._VWGUI__validate_arguments, play=False, file_to_load="", scale=1, speed=value, total_cycles=0)

    def test_illegal_scale_value(self) -> None:
        for value in [-1, -0.3, 2.6, 3, 100, 1000]:
            self.assertRaises(ValueError, VWGUI._VWGUI__validate_arguments, play=False, file_to_load="", scale=value, speed=0, total_cycles=0)

    def test_play_without_load(self) -> None:
        self.assertRaises(ValueError, VWGUI._VWGUI__validate_arguments, play=True, file_to_load="", scale=1, speed=0, total_cycles=0)

    def test_illegal_total_cycles_value(self) -> None:
        for value in [-1, -0.3, 0.1, 1.1]:
            self.assertRaises(ValueError, VWGUI._VWGUI__validate_arguments, play=False, file_to_load="", scale=1, speed=0, total_cycles=value)

    def test_illegal_minds_combination(self) -> None:
        self.assertRaises(AssertionError, run)
        self.assertRaises(AssertionError, run, green_mind=VWHystereticMindSurrogate())
        self.assertRaises(AssertionError, run, orange_mind=VWHystereticMindSurrogate())
        self.assertRaises(AssertionError, run, white_mind=VWHystereticMindSurrogate())
        self.assertRaises(AssertionError, run, green_mind=VWHystereticMindSurrogate(), orange_mind=VWHystereticMindSurrogate())
        self.assertRaises(AssertionError, run, green_mind=VWHystereticMindSurrogate(), white_mind=VWHystereticMindSurrogate())
        self.assertRaises(AssertionError, run, orange_mind=VWHystereticMindSurrogate(), white_mind=VWHystereticMindSurrogate())

    def test_malformed_surrogate_minds(self) -> None:
        malformed_minds: list = [
            EmptySurrogateMind(),
            NoReviseSurrogateMind(),
            NoDecideSurrogateMind(),
            MalformedReviseSurrogateMind(),
            NoMessagesMalformedReviseSurrogateMind(),
            NoObservationMalformedReviseSurrogateMind(),
            MalformedDecideSurrogateMind()
        ]

        vw_allowed_run_args_backup: Dict[str, Type] = VacuumWorld.ALLOWED_RUN_ARGS

        for mind in malformed_minds:
            for colour in Colour:
                if colour != Colour.user:
                    VacuumWorld.ALLOWED_RUN_ARGS["default_mind"] = type(mind)
                    VacuumWorld.ALLOWED_RUN_ARGS[str(colour) + "_mind"] = type(mind)

            # self.assertRaises(VWInternalError, run, default_mind=mind)
            # self.assertRaises(VWInternalError, run, green_mind=mind, orange_mind=mind, white_mind=mind)

        VacuumWorld.ALLOWED_RUN_ARGS = vw_allowed_run_args_backup


if __name__ == "__main__":
    main()
