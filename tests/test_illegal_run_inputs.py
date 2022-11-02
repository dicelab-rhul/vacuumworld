#!/usr/bin/env python3

from unittest import main, TestCase
from typing import Iterable, Union, Tuple, List, Dict, Type

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from vacuumworld import VacuumWorld, run
from vacuumworld.config_manager import ConfigManager
from vacuumworld.common.colour import Colour
from vacuumworld.common.observation import Observation
from vacuumworld.common.exceptions import VWInternalError
from vacuumworld.model.actor.actor_mind_surrogate import ActorMindSurrogate
from vacuumworld.model.actor.hystereticmindsurrogate import VWHystereticMindSurrogate
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.idle_action import VWIdleAction
from vacuumworld.runner.guiless_runner import VWGUIlessRunner


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


class TestIllegalRunInputs(TestCase):
    '''
    All the arguments of `run()` that are not tested are simply ignored if they are not valid.

    All unknown arguments of `run()` are ignored by the system.
    '''

    def __init__(self, args) -> None:
        super(TestIllegalRunInputs, self).__init__(args)

        self.__config: dict = ConfigManager.load_config_from_file(config_file_path=VacuumWorld.CONFIG_FILE_PATH)
        self.__minds: Dict[Colour, ActorMindSurrogate()] = {
            Colour.green: VWHystereticMindSurrogate(),
            Colour.orange: VWHystereticMindSurrogate(),
            Colour.white: VWHystereticMindSurrogate()
        }

    def test_illegal_speed_value(self) -> None:
        for value in [-1337, -70, -1, 2, 3, 100, 1000]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, speed=value)

        for value in [-1.5, -0.3, 1.1, 2.987, 3.3, 100.0003, 1000.15]:
            self.assertRaises(ValueError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, speed=value)

    def test_illegal_scale_value(self) -> None:
        for value in [-100, -1, 2, 3, 100, 1000]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, scale=value)

        for value in [-1.8, -0.3, 2.6, 3.14, 100.001, 1000.1337]:
            self.assertRaises(ValueError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, scale=value)

    def test_play_without_load(self) -> None:
        self.assertRaises(ValueError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, play=True)

    def test_illegal_total_cycles_value(self) -> None:
        for value in [-1.2, -0.3, 0.1, 1.1]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, total_cycles=value)

        for value in [-10, -8, -5, -1]:
            self.assertRaises(ValueError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, total_cycles=value)

    def test_illegal_efforts(self) -> None:
        for value in ["hello", "world", 1, -8.8, ["foo", "bar"]]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, efforts=value)

        for value in [{1: 1}, {2: 2}, {3: 3}, {4: 4}]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, efforts=value)

        for value in [{"donald": "duck"}, {"goofy": "who_knows"}, {"mickey": "mouse"}, {"minnie": "mouse"}]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, efforts=value)

        for value in [{"donald": 1}, {"goofy": 2}, {"mickey": 3}, {"minnie": 4}]:
            self.assertRaises(ValueError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, efforts=value)

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

            self.assertRaises(VWInternalError, ActorMindSurrogate.validate, mind=mind, colour=colour)

        VacuumWorld.ALLOWED_RUN_ARGS = vw_allowed_run_args_backup


if __name__ == "__main__":
    main()
