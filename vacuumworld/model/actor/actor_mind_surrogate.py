from __future__ import annotations
from typing import Any, Iterable, Tuple, Union
from inspect import signature
from importlib import import_module

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from ..actions.vwactions import VWAction
from ..actions.idle_action import VWIdleAction
from ...common.observation import Observation
from ...common.colour import Colour
from ...common.exceptions import VWInternalError, VWLoadException

import os
import sys



class ActorMindSurrogate():
    MUST_BE_DEFINED: dict = {
        "revise": 2, # Not including 'self'.
        "decide": 0  # Not including 'self'.
    }
    
    def __init__(self) -> None:        
        self.__effort: int = 0
        
    def get_effort(self) -> int:
        return self.__effort
    
    def update_effort(self, increment: int) -> None:
        assert type(increment) == int
        
        self.__effort += increment

    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        # Abstract.
        ignore(self)
        ignore(observation)
        ignore(messages)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        # Abstract.
        ignore(self)

        return VWIdleAction()

    @staticmethod
    def validate(mind: ActorMindSurrogate, colour: Colour) -> None:
        assert mind

        for fun_name, number_of_parameters in ActorMindSurrogate.MUST_BE_DEFINED.items():
            if fun_name not in set(dir(mind)):
                raise VWInternalError("The {} mind surrogate must define the following method: {}".format(colour, fun_name))
            
            fun: Any = getattr(mind, fun_name)
            
            if not callable(fun):
                raise VWInternalError("{} agent: {} must be callable".format(colour, fun_name))
            elif len(signature(fun).parameters) != number_of_parameters:
                raise VWInternalError("{} agent: {} must be defined with no arguments, decide(self)".format(colour, fun_name))

    @staticmethod
    def load_from_file(surrogate_mind_file: str, surrogate_mind_class_name: str) -> ActorMindSurrogate:
        try:
            assert surrogate_mind_file.endswith(".py")

            parent_dir: str = os.path.dirname(surrogate_mind_file)
            module_name: str = os.path.basename(surrogate_mind_file)[:-3]

            if parent_dir not in sys.path:
                sys.path.append(parent_dir)

            return getattr(import_module(name=module_name), surrogate_mind_class_name)()
        except Exception:
            raise VWLoadException("Could not load {} from {}.".format(surrogate_mind_file, surrogate_mind_class_name))
