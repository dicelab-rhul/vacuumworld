#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 10:29:55 2019

@author: ben
"""
from pystarworlds.Agent import Mind
from . import vwc

import inspect

from inspect import signature
from os import devnull

class VacuumWorldInternalError(Exception):
    pass

class VacuumWorldActionError(VacuumWorldInternalError):
    
    def __init__(self, message):
        super(VacuumWorldActionError, self).__init__("for agent: " + caller_id() + "\n      " + message)

def caller_id():
    caller = inspect.currentframe().f_back
    while not isinstance(caller.f_locals.get('self', None), Mind):
        caller = caller.f_back
    return caller.f_locals['self'].body.ID

def warn_agent(message, *args):
    print("WARNING: " + message.format(caller_id(), *args))

def process_minds(white_mind, green_mind=None, orange_mind=None, observers={}):
    assert white_mind is not None
    
    if green_mind is not None:
        validate_mind(green_mind, vwc.Colour.green)
        observe(green_mind, observers)
    else:
        green_mind = white_mind
        
    if orange_mind is not None:
        validate_mind(orange_mind, vwc.Colour.orange)
        observe(orange_mind, observers)
    else:
        orange_mind = white_mind
    
    validate_mind(white_mind, vwc.Colour.white)
    #observe(white_mind, observers) # I think this should be removed, it is quite fragile.
    
    return white_mind, green_mind, orange_mind

def raise_static_modification_error(agent, name, _):
    raise VacuumWorldInternalError("Agent: {0} tried to modify the static field: {1} this is cheating!".format(agent, name))

def observe(mind, observers):
    for obs in observers:
        if not obs in set(dir(mind)):
            print("WARNING: agent attribute: {0} not defined.".format(obs))
            #raise vw.VacuumWorldInternalError("WARNING: {0} agent: must define 
            # \ the attribute: {1}, (see coursework question 1)".format(colour, obs)) 
    def sneaky_setattr(self, name, value):
        if name in observers:
            observers[name](caller_id(), name, value)
        super(type(mind), self).__setattr__(name, value)
    type(mind).__setattr__ = sneaky_setattr
    return mind

def print_observer(agent, name, value):
    print("Agent {0} updated {1}: {2}".format(agent, name, value))

def validate_mind(mind, colour):
    
    def decide_def(fun):
        if not callable(fun):
            raise VacuumWorldInternalError("{0} agent: decide must be callable".format(colour))            
        if len(signature(fun).parameters) != 0:
            raise VacuumWorldInternalError("{0} agent: decide must be defined with no arguments, decide(self)".format(colour))
    
    def revise_def(fun):
        if not callable(fun):
            raise VacuumWorldInternalError("{0} agent: revise must be callable".format(colour))            
        if len(signature(fun).parameters) != 2:
            raise VacuumWorldInternalError("{0} agent: revise must be defined with two arguments, revise(self, observation, messages)".format(colour))
             
    MUST_BE_DEFINED = {'decide':decide_def, 
                       'revise':revise_def}
    
    mind_dir = set(dir(mind))

    for fun, validate in MUST_BE_DEFINED.items():
        if fun in mind_dir:
            validate(getattr(mind, fun))
        else:
            raise VacuumWorldInternalError("{0} agent: must define method: {1}".format(colour, fun))

def print_simulation_speed_message(time_step):
    print("INFO: simulation speed set to {:1.4f} s/cycle".format(time_step))

def ignore(obj):
    if not obj:
        return

    with open(devnull, "w") as f:
        f.write(str(obj))
        f.flush()


# SOME MEGA HACKY STUFF... not sure if we want to use it 

import inspect
import sys

class ReturnLine:

    def __init__(self):
        self.return_line = None
        self._old_trace = None

    def start(self):
        self._old_trace = sys.gettrace()
        sys.settrace(self.trace)

    def stop(self):
        sys.settrace(self._old_trace)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc):
        self.stop()

    def trace(self, frame, event, arg):
        filename = None
        if frame is not None:
            filename = inspect.getsourcefile(frame)
        if event == 'call':
            if filename == __file__:
                # skip ourselves 
                return       
            return self.trace
        elif event == 'return':
            self.return_line = (filename, frame.f_lineno)
        
    def line(self, agent):
        source, start = inspect.getsourcelines(agent)
        return source[self.return_line[1] - start]