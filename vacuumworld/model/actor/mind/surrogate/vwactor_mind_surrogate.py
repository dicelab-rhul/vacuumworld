from __future__ import annotations
from typing import Any, Iterable, Type
from abc import ABC, abstractmethod
from inspect import signature
from importlib import import_module

from pystarworldsturbo.common.message import BccMessage

from ....actions.vwactions import VWAction
from ....actions.vwactions import VWPhysicalAction
from ....actions.vwactions import VWCommunicativeAction
from .....model.actor.appearance.vwactor_appearance import VWActorAppearance
from .....common.vwobservation import VWObservation
from .....common.vwcolour import VWColour
from .....common.vworientation import VWOrientation
from .....common.vwcoordinates import VWCoord
from .....common.vwexceptions import VWLoadException, VWSurrogateMindException

import os
import sys


class VWActorMindSurrogate(ABC):
    '''
    This class specifies the surrogate for the `VWMind` of a `VWActor`. It is an abstract class.
    '''
    MUST_BE_DEFINED: dict[str, Any] = {
        "revise": {"number_of_params_excluding_self": 0, "return_type": [None, "None", "NoneType"]},
        "decide": {"number_of_params_excluding_self": 0, "return_type": [Iterable[VWAction], Iterable[VWPhysicalAction], Iterable[VWCommunicativeAction]]},
    }

    def __init__(self) -> None:
        self.__effort: int = 0

    def get_effort(self) -> int:
        '''
        Returns the cumulative effort of the `VWActor` up until now.
        '''
        return self.__effort

    def get_latest_observation(self) -> VWObservation:
        '''
        Returns the last `VWObservation` perceived by the `VWActor`.
        '''
        return self.__latest_observation

    def get_latest_received_messages(self) -> Iterable[BccMessage]:
        '''
        Returns the last `Iterable[BccMessage]` received by the `VWActor`.
        '''
        return self.__latest_received_messages

    def get_own_appearance(self) -> VWActorAppearance:
        '''
        Returns the `VWActorAppearance` of the `VWActor` this `VWActorMindSurrogate` is part of.
        '''
        return self.__latest_observation.get_center().or_else_raise().get_actor_appearance().or_else_raise()

    def get_own_id(self) -> str:
        '''
        Returns the `str` ID of the `VWActor` this `VWActorMindSurrogate` is part of.
        '''
        return self.__latest_observation.get_observer_id().or_else_raise()

    def get_own_colour(self) -> VWColour:
        '''
        Returns the `VWColour` of the `VWActor` this `VWActorMindSurrogate` is part of.
        '''
        return self.get_own_appearance().get_colour()

    def get_own_orientation(self) -> VWOrientation:
        '''
        Returns the `VWOrientation` of the `VWActor` this `VWActorMindSurrogate` is part of.
        '''
        return self.get_own_appearance().get_orientation()

    def get_own_position(self) -> VWCoord:
        '''
        Returns the position (as a `VWCoord` object) of the `VWActor` this `VWActorMindSurrogate` is part of.
        '''
        return self.__latest_observation.get_center().or_else_raise().get_coord()

    def update_effort(self, increment: int) -> None:
        '''
        WARNING: This method must be public, but it is not part of the public `VWActorMindSurrogate` API.

        Updates the cumulative effort of the `VWActor` by `increment`.
        '''
        assert int is not None and isinstance(increment, int)

        self.__effort += increment

    def perceive(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None:
        '''
        WARNING: This method must be public, but it is not part of the public `VWActorMindSurrogate` API.

        This method is automatically called by a `VWActor` to store the received `VWObservation` and `Iterable[BccMessage]`.
        '''
        assert observation is not None and isinstance(observation, VWObservation)
        assert messages is not None and isinstance(messages, Iterable) and all(isinstance(message, BccMessage) for message in messages)

        self.__latest_observation: VWObservation = observation
        self.__latest_received_messages: Iterable[BccMessage] = messages if messages else []

    @abstractmethod
    def revise(self) -> None:
        '''
        This method must be overridden by a subclass.

        Revises the internal state of this `VWActorMindSurrogate` based on the latest received `VWObservation` and `Iterable[BccMessage]`.
        '''
        ...

    @abstractmethod
    def decide(self) -> Iterable[VWAction]:
        '''
        This method must be overridden by a subclass.

        Decides the next `Iterable[VWAction]` to be performed by the `VWActor` based on the internal state of this `VWActorMindSurrogate`.
        '''
        ...

    @staticmethod
    def validate(mind: VWActorMindSurrogate, colour: VWColour, surrogate_mind_type: Type[Any]) -> None:
        '''
        WARNING: This method must be public, but it is not part of the public `VWActorMindSurrogate` API.

        Validates the `VWActorMindSurrogate` `mind` by checking that all the methods specified in `VWActorMindSurrogate.MUST_BE_DEFINED` are defined, together with the correct arguments.

        The type check on `mind` is replaced with an assertion, as the actual check is performed by the `VWRunner` constructor.
        '''
        assert mind
        assert isinstance(mind, surrogate_mind_type)
        assert isinstance(colour, VWColour)

        for fun_name, fun_info in VWActorMindSurrogate.MUST_BE_DEFINED.items():
            if fun_name not in set(dir(mind)):
                raise VWSurrogateMindException(f"The {colour} mind surrogate must define the following method: `{fun_name}`")

            fun: Any = getattr(mind, fun_name)

            if not callable(fun):
                raise VWSurrogateMindException(f"{colour} agent: {fun_name} must be callable")

            number_of_parameters: int = fun_info["number_of_params_excluding_self"]

            if len(signature(fun).parameters) != number_of_parameters:
                raise VWSurrogateMindException(f"{colour} agent: `{fun_name}` must be defined with exactly {number_of_parameters} parameters.")

            return_type: list[Type[Any]] = fun_info["return_type"]

            if signature(fun).return_annotation not in return_type:
                raise VWSurrogateMindException(f"{colour} agent: `{fun_name}` must be defined with a return type that is compatible with `{return_type}`.")

    @staticmethod
    def load_from_file(surrogate_mind_file: str, surrogate_mind_class_name: str) -> VWActorMindSurrogate:
        '''
        WARNING: This method must be public, but it is not part of the public `VWActorMindSurrogate` API.

        Loads the `VWActorMindSurrogate` class from the Python file whose path is specified by `surrogate_mind_file` and returns an instance of it.
        '''
        try:
            python_file_extension: str = ".py"

            assert surrogate_mind_file.endswith(python_file_extension)

            parent_dir: str = os.path.dirname(surrogate_mind_file)
            module_name: str = os.path.basename(surrogate_mind_file)[:-len(python_file_extension)]

            if parent_dir not in sys.path:
                sys.path.append(parent_dir)

            return getattr(import_module(name=module_name), surrogate_mind_class_name)()
        except Exception:
            raise VWLoadException(f"Could not load {surrogate_mind_class_name} from {surrogate_mind_file}.")
