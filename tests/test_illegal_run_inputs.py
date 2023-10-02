#!/usr/bin/env python3

from unittest import main, TestCase
from typing import Iterable, Union, Tuple, List, Dict, Type, Any

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from vacuumworld import VacuumWorld, run
from vacuumworld.vwconfig_manager import VWConfigManager
from vacuumworld.common.vwcolour import VWColour
from vacuumworld.common.vwobservation import VWObservation
from vacuumworld.common.vwexceptions import VWInternalError
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.model.actor.mind.surrogate.vwhysteretic_mind_surrogate import VWHystereticMindSurrogate
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.runner.vwguiless_runner import VWGUIlessRunner
from vacuumworld.common.vwexceptions import VWRunnerException


class EmptySurrogateMind():
    '''
    This class is malformed for surrogate minds, because:
    * It does not inherit from `VWActorMindSurrogate`.
    * It does not implement the `revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None` method.
    * It does not implement the `decide(self) -> Union[VWAction, VWIdleAction]` method.
    '''
    pass


class NoDecideSurrogateMind():
    '''
    This class is malformed for surrogate minds, because:
    * It does not inherit from `VWActorMindSurrogate`.
    * It does not implement the `decide(self) -> Union[VWAction, VWIdleAction]` method.
    '''
    def revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None:
        '''
        This method is well-formed.
        '''
        ignore(observation)

        for m in messages:
            ignore(m)


class NoReviseSurrogateMind():
    '''
    This class is malformed for surrogate minds, because:
    * It does not inherit from `VWActorMindSurrogate`.
    * It does not implement the `revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None` method.
    '''
    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        '''
        This method is well-formed.
        '''
        return VWIdleAction()


class MalformedReviseSurrogateMind():
    '''
    This class is malformed for surrogate minds, because:
    * It does not inherit from `VWActorMindSurrogate`.
    * It implements a malformed `revise(self, observation: VWObservation, messages: Iterable[BccMessage], nonsense: List[str]) -> None` method.
    * It does not implement the `revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None` method.
    '''
    def revise(self, observation: VWObservation, messages: Iterable[BccMessage], nonsense: List[str]) -> None:
        '''
        This method is malformed, because it has an unwarranted `nonsense` argument of type `List[str]`.
        '''
        ignore(observation)

        for m in messages:
            ignore(m)

        for elm in nonsense:
            ignore(elm)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        '''
        This method is well-formed.
        '''
        return VWIdleAction()


class NoMessagesMalformedReviseSurrogateMind():
    '''
    This class is malformed for surrogate minds, because:
    * It does not inherit from `VWActorMindSurrogate`.
    * It implements a malformed `revise(self, observation: VWObservation) -> None` method.
    * It does not implement the `revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None` method.
    '''
    def revise(self, observation: VWObservation) -> None:
        '''
        This method is malformed, because it lacks the `messages` argument of type `Iterable[BccMessage]`.
        '''
        ignore(observation)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        '''
        This method is well-formed.
        '''
        return VWIdleAction()


class NoObservationMalformedReviseSurrogateMind():
    '''
    This class is malformed for surrogate minds, because:
    * It does not inherit from `VWActorMindSurrogate`.
    * It implements a malformed `revise(self, messages: Iterable[BccMessage]) -> None` method.
    * It does not implement the `revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None` method.
    '''
    def revise(self, messages: Iterable[BccMessage]) -> None:
        '''
        This method is malformed, because it lacks the `observation` argument of type `VWObservation`.
        '''
        for m in messages:
            ignore(m)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        return VWIdleAction()


class MalformedDecideSurrogateMind():
    '''
    This class is malformed for surrogate minds, because:
    * It does not inherit from `VWActorMindSurrogate`.
    * It implements a malformed `decide(self, nonsense: List[str]) -> Union[VWAction, VWIdleAction]` method.
    * It does not implement the `decide(self) -> Union[VWAction, VWIdleAction]` method.
    '''
    def revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None:
        '''
        This method is well-formed.
        '''
        ignore(observation)

        for m in messages:
            ignore(m)

    def decide(self, nonsense: List[str]) -> Union[VWAction, Tuple[VWAction]]:
        '''
        This method is malformed, because it has an unwarranted `nonsense` argument of type `List[str]`.
        '''
        for elm in nonsense:
            ignore(elm)

        return VWIdleAction()


class NoInheritanceMalformedSurrogateMind():
    '''
    This class is malformed for surrogate minds, because:
    * It does not inherit from `VWActorMindSurrogate`.
    '''
    def revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None:
        '''
        This method is well-formed.
        '''
        ignore(observation)

        for m in messages:
            ignore(m)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        '''
        This method is well-formed.
        '''
        return VWIdleAction()


class TestIllegalRunInputs(TestCase):
    '''
    Tests the rejection of various illegal/malformed attributes (orcombinations of attributes) of the `run()` method.

    All tests are performed in GUI-less mode.

    All the arguments of `run()` that are not tested are simply ignored if they are not valid.

    All unknown arguments of `run()` are ignored by the system.
    '''
    def __init__(self, args: Any) -> None:
        super(TestIllegalRunInputs, self).__init__(args)

        self.__config: dict[str, Any] = VWConfigManager.load_config_from_file(config_file_path=VacuumWorld.CONFIG_FILE_PATH, load_additional_config=False)
        self.__minds: Dict[VWColour, VWActorMindSurrogate] = {
            VWColour.green: VWHystereticMindSurrogate(),
            VWColour.orange: VWHystereticMindSurrogate(),
            VWColour.white: VWHystereticMindSurrogate()
        }

    def test_illegal_speed_value(self) -> None:
        '''
        Tests various illegal `speed` values.
        '''
        for value in [-1337, -70, -1, 2, 3, 100, 1000]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, speed=value)

        for value in [-1.5, -0.3, 1.1, 2.987, 3.3, 100.0003, 1000.15]:
            self.assertRaises(ValueError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, speed=value)

    def test_illegal_scale_value(self) -> None:
        '''
        Tests various illegal `scale` values.
        '''
        for value in [-100, -1, 2, 3, 100, 1000]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, scale=value)

        for value in [-1.8, -0.3, 2.6, 3.14, 100.001, 1000.1337]:
            self.assertRaises(ValueError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, scale=value)

    def test_play_without_load(self) -> None:
        '''
        Tests the illegal combination of `play=True` and no `load`.
        '''
        self.assertRaises(ValueError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, play=True)

    def test_illegal_total_cycles_value(self) -> None:
        '''
        Tests various illegal `total_cycles` values.
        '''
        for value in [-1.2, -0.3, 0.1, 1.1]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, total_cycles=value)

        for value in [-10, -8, -5, -1]:
            self.assertRaises(ValueError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, total_cycles=value)

    def test_illegal_efforts(self) -> None:
        '''
        Tests various illegal `efforts` values.
        '''
        for value in ["hello", "world", 1, -8.8, ["foo", "bar"]]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, efforts=value)

        for value in [{1: 1}, {2: 2}, {3: 3}, {4: 4}]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, efforts=value)

        for value in [{"donald": "duck"}, {"goofy": "who_knows"}, {"mickey": "mouse"}, {"minnie": "mouse"}]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, efforts=value)

        for value in [{"donald": 1}, {"goofy": 2}, {"mickey": 3}, {"minnie": 4}]:
            self.assertRaises(ValueError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, efforts=value)

    def test_illegal_debug_flag(self) -> None:
        '''
        Tests various illegal `debug_enabled` values.
        '''
        for value in [-1, -8.8, "whatever", ["foo", "bar"], {1: 1}, ("a", "b", "c")]:
            self.assertRaises(TypeError, VWGUIlessRunner, config=self.__config, minds=self.__minds, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS, debug_enabled=value)

    def test_illegal_minds_combination(self) -> None:
        '''
        Tests the `run()` function with various illegal combinations of `default_mind`, `green_mind`, `orange_mind`, and `white_mind`.
        '''
        self.assertRaises(ValueError, run)
        self.assertRaises(ValueError, run, green_mind=VWHystereticMindSurrogate())
        self.assertRaises(ValueError, run, orange_mind=VWHystereticMindSurrogate())
        self.assertRaises(ValueError, run, white_mind=VWHystereticMindSurrogate())
        self.assertRaises(ValueError, run, green_mind=VWHystereticMindSurrogate(), orange_mind=VWHystereticMindSurrogate())
        self.assertRaises(ValueError, run, green_mind=VWHystereticMindSurrogate(), white_mind=VWHystereticMindSurrogate())
        self.assertRaises(ValueError, run, orange_mind=VWHystereticMindSurrogate(), white_mind=VWHystereticMindSurrogate())

    def test_malformed_surrogate_minds(self) -> None:
        '''
        Tests the rejection of various malformed surrogate minds.

        The requirement that surrogate minds must inherit from `VWActorMindSurrogate` is waived in this particular test by means of temporarily overriding `VacuumWorld.ALLOWED_RUN_ARGS`.
        '''
        malformed_minds: list[object] = [
            EmptySurrogateMind(),
            NoReviseSurrogateMind(),
            NoDecideSurrogateMind(),
            MalformedReviseSurrogateMind(),
            NoMessagesMalformedReviseSurrogateMind(),
            NoObservationMalformedReviseSurrogateMind(),
            MalformedDecideSurrogateMind()
        ]

        vw_allowed_run_args_backup: Dict[str, Type[Any]] = {k: v for k, v in VacuumWorld.ALLOWED_RUN_ARGS.items()}

        for mind in malformed_minds:
            for colour in VWColour:
                if colour != VWColour.user:
                    VacuumWorld.ALLOWED_RUN_ARGS["default_mind"] = type(mind)
                    VacuumWorld.ALLOWED_RUN_ARGS[str(colour) + "_mind"] = type(mind)

                self.assertRaises(VWInternalError, VWActorMindSurrogate.validate, mind=mind, colour=colour, surrogate_mind_type=type(mind))

        VacuumWorld.ALLOWED_RUN_ARGS = vw_allowed_run_args_backup

    def test_no_inheritance_malformed_surrogate_mind(self) -> None:
        '''
        Tests the rejection of a surrogate mind that does not inherit from `VWActorMindSurrogate`.
        '''
        for colour in VWColour:
            if colour != VWColour.user:
                self.assertRaises(VWRunnerException, VWGUIlessRunner, config=self.__config, minds={c: NoInheritanceMalformedSurrogateMind() for c in VWColour if c != VWColour.user}, allowed_args=VacuumWorld.ALLOWED_RUN_ARGS)


if __name__ == "__main__":
    main()
