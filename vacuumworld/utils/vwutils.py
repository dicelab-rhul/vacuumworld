from inspect import signature, getsourcefile
from sys import gettrace, settrace
from typing import Any, List, Optional, Callable, Tuple, Dict, Set
from importlib import import_module

from .exceptions import VWLoadException, VWInternalError
from ..model.actor.actor_mind_surrogate import ActorMindSurrogate
from ..common.colour import Colour

import sys
import os



def load_surrogate_mind_from_file(surrogate_mind_file: str, surrogate_mind_class_name: str) -> ActorMindSurrogate:
    try:
        assert surrogate_mind_file.endswith(".py")

        parent_dir: str = os.path.dirname(surrogate_mind_file)
        module_name: str = os.path.basename(surrogate_mind_file)[:-3]

        if parent_dir not in sys.path:
            sys.path.append(parent_dir)

        return getattr(import_module(name=module_name), surrogate_mind_class_name)()
    except Exception:
        raise VWLoadException("Could not load {} from {}.".format(surrogate_mind_file, surrogate_mind_class_name))


def get_location_img_files(path: str) -> List[str]:
    return [file for file in os.listdir(path) if file.endswith(".png")]


def process_minds(default_mind: ActorMindSurrogate=None, white_mind: ActorMindSurrogate=None, green_mind: ActorMindSurrogate=None, orange_mind: ActorMindSurrogate=None) -> Tuple[ActorMindSurrogate, ActorMindSurrogate, ActorMindSurrogate]:
    assert default_mind is not None or white_mind is not None and green_mind is not None and orange_mind is not None
    
    if white_mind is None:
        white_mind = default_mind

    if green_mind is None:
        green_mind = default_mind

    if orange_mind is None:
        orange_mind = default_mind

    validate_mind(white_mind, Colour.white)
    validate_mind(green_mind, Colour.green)
    validate_mind(orange_mind, Colour.orange)
    
    return white_mind, green_mind, orange_mind


def raise_static_modification_error(agent: str, name: str, _) -> None:
    raise VWInternalError("Agent: {0} tried to modify the static field: {1} this is cheating!".format(agent, name))


def print_observer(agent: str, name: str, value: str) -> None:
    print("Agent {0} updated {1}: {2}".format(agent, name, value))


def validate_mind(mind: ActorMindSurrogate, colour: Colour) -> None:
    def decide_def(fun: Any) -> None:
        if not callable(fun):
            raise VWInternalError("{0} agent: decide must be callable".format(colour))            
        if len(signature(fun).parameters) != 0:
            raise VWInternalError("{0} agent: decide must be defined with no arguments, decide(self)".format(colour))
    
    def revise_def(fun: Any) -> None:
        if not callable(fun):
            raise VWInternalError("{0} agent: revise must be callable".format(colour))            
        if len(signature(fun).parameters) != 2:
            raise VWInternalError("{0} agent: revise must be defined with two arguments, revise(self, observation, messages)".format(colour))
             
    MUST_BE_DEFINED: Dict[str, Callable] = {"decide": decide_def, "revise": revise_def}
    
    mind_dir: Set[str] = set(dir(mind))

    for fun, validate in MUST_BE_DEFINED.items():
        if fun in mind_dir:
            validate(getattr(mind, fun))
        else:
            raise VWInternalError("The {} mind surrogate must define the following method: {}".format(colour, fun))


def print_simulation_speed_message(time_step: float) -> None:
    print("INFO: simulation speed set to {:1.4f} s/cycle".format(time_step))


# For debug.
class ReturnFrame():
    def __init__(self) -> None:
        self.frame = None
        self._old_trace: Any = None

    def start(self) -> None:
        self._old_trace: Any = gettrace()
        settrace(self.trace)

    def stop(self) -> None:
        settrace(self._old_trace)

    def __enter__(self) -> "ReturnFrame":
        self.start()

        return self

    def __exit__(self, *_) -> None:
        self.stop()


    def trace(self, frame, event: str, _) -> Optional[Callable]:
        filename: str = None
        if frame is not None:
            filename = getsourcefile(frame)
        if event == "call":
            if filename == __file__:
                return # skip ourselves     
            return self.trace
        elif event == "return":
            self.frame: Any = frame

        return None
