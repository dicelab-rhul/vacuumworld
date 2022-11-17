from __future__ import annotations
from typing import Any, Iterable, Tuple, Union
from inspect import signature
from importlib import import_module

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from ..actions.vwactions import VWAction
from ...common.observation import Observation
from ...common.colour import Colour
from ...common.exceptions import VWInternalError, VWLoadException

import os
import sys


class ActorMindSurrogate():
    '''
    This class specifies the surrogate for the `VWMind` of a `VWActor`. It is an abstract class.
    '''
    MUST_BE_DEFINED: dict = {
        "revise": 2,  # Not including `self`.
        "decide": 0   # Not including `self`.
    }

    def __init__(self) -> None:
        self.__effort: int = 0

    def get_effort(self) -> int:
        '''
        Returns the cumulative effort of the `VWActor` up until now.
        '''
        return self.__effort

    def update_effort(self, increment: int) -> None:
        '''
        WARNING: This method must be public, but it is not part of the public `ActorMindSurrogate` API.

        Updates the cumulative effort of the `VWActor` by `increment`.
        '''
        assert type(increment) == int

        self.__effort += increment

    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        '''
        This is an abstract method. It is called by the `VWActor` to update the `ActorMindSurrogate` with the latest `Observation` and `Iterable[BccMessage]`.
        '''
        ignore(observation)

        for message in messages:
            ignore(message)

        raise NotImplementedError()

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        '''
        This is an abstract method. It is called by the `VWActor` to decide the next `VWAction` or `Tuple[VWAction]` to be executed.

        This method MUST NOT loop, as it is called by the `VWActor` every cycle after `revise()`.
        '''
        raise NotImplementedError()

    @staticmethod
    def validate(mind: ActorMindSurrogate, colour: Colour) -> None:
        '''
        Validates the `ActorMindSurrogate` `mind` by checking that all the methods specified in `ActorMindSurrogate.MUST_BE_DEFINED` are defined, together with the correct arguments.
        '''
        assert mind

        for fun_name, number_of_parameters in ActorMindSurrogate.MUST_BE_DEFINED.items():
            if fun_name not in set(dir(mind)):
                raise VWInternalError("The {} mind surrogate must define the following method: `{}`".format(colour, fun_name))

            fun: Any = getattr(mind, fun_name)

            if not callable(fun):
                raise VWInternalError("{} agent: {} must be callable".format(colour, fun_name))
            elif len(signature(fun).parameters) != number_of_parameters:
                raise VWInternalError("{} agent: `{}` must be defined with {} arguments, excluding `self`.".format(colour, fun_name, number_of_parameters))

    @staticmethod
    def load_from_file(surrogate_mind_file: str, surrogate_mind_class_name: str) -> ActorMindSurrogate:
        '''
        Loads the `ActorMindSurrogate` class from the Python file whose path is specified by `surrogate_mind_file` and returns an instance of it.
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
            raise VWLoadException("Could not load {} from {}.".format(surrogate_mind_file, surrogate_mind_class_name))
