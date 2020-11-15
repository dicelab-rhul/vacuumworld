# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 10:29:55 2019

@author: ben
"""

from inspect import signature, currentframe, getsourcefile
from os import devnull
from sys import gettrace, settrace
from types import FrameType
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from pystarworlds.Agent import Mind

from ..core.common.colour import Colour

import os



class VacuumWorldInternalError(Exception):
    pass

class VacuumWorldActionError(VacuumWorldInternalError):
    
    def __init__(self, message: str) -> None:
        c_id: str = caller_id()

        if c_id is None:
            c_id = ""

        super(VacuumWorldActionError, self).__init__("for agent: " + c_id + "\n      " + message)


def get_location_img_files(path: str) -> List[str]:
    return [file for file in os.listdir(path) if file.endswith(".png")]


def caller_id() -> Optional[str]:
    caller: FrameType = currentframe().f_back

    if caller is None:
        return None

    while not isinstance(caller.f_locals.get('self', None), Mind):
        if caller.f_back is not None:
            caller = caller.f_back
        else:
            return None
    return caller.f_locals['self'].body.ID


def warn_agent(message: str, *args) -> None:
    c_id: str = caller_id()

    if c_id is None:
        c_id = ""

    print("WARNING: " + message.format(c_id, *args))


def process_minds(default_mind: Any=None, white_mind: Any=None, green_mind: Any=None, orange_mind: Any=None, observers: dict={}) -> Tuple[Any, Any, Any]:
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

    for mind in (white_mind, green_mind, orange_mind):
        observe(mind, observers)
    
    return white_mind, green_mind, orange_mind


def raise_static_modification_error(agent: str, name: str, _) -> None:
    raise VacuumWorldInternalError("Agent: {0} tried to modify the static field: {1} this is cheating!".format(agent, name))


def observe(mind: Any, observers: dict) -> None:
    for obs in observers:
        if not obs in set(dir(mind)):
            print("WARNING: agent attribute: {0} not defined.".format(obs))
    def sneaky_setattr(self, name, value) -> None:
        if name in observers:
            c_id: str = caller_id()

            if c_id is not  None:
                observers[name](c_id, name, value)
        super(type(mind), self).__setattr__(name, value)
    type(mind).__setattr__ = sneaky_setattr


def print_observer(agent: str, name: str, value: str) -> None:
    print("Agent {0} updated {1}: {2}".format(agent, name, value))


def validate_mind(mind, colour: Colour) -> None:
    def decide_def(fun: Any) -> None:
        if not callable(fun):
            raise VacuumWorldInternalError("{0} agent: decide must be callable".format(colour))            
        if len(signature(fun).parameters) != 0:
            raise VacuumWorldInternalError("{0} agent: decide must be defined with no arguments, decide(self)".format(colour))
    
    def revise_def(fun: Any) -> None:
        if not callable(fun):
            raise VacuumWorldInternalError("{0} agent: revise must be callable".format(colour))            
        if len(signature(fun).parameters) != 2:
            raise VacuumWorldInternalError("{0} agent: revise must be defined with two arguments, revise(self, observation, messages)".format(colour))
             
    MUST_BE_DEFINED: Dict[str, Callable] = {"decide": decide_def, "revise": revise_def}
    
    mind_dir: Set[str] = set(dir(mind))

    for fun, validate in MUST_BE_DEFINED.items():
        if fun in mind_dir:
            validate(getattr(mind, fun))
        else:
            raise VacuumWorldInternalError("{0} agent: must define method: {1}".format(colour, fun))


def print_simulation_speed_message(time_step: float) -> None:
    print("INFO: simulation speed set to {:1.4f} s/cycle".format(time_step))


def ignore(obj: Any) -> None:
    if not obj:
        return

    with open(devnull, "w") as f:
        f.write(str(obj))
        f.flush()


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
