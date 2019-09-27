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

class VacuumWorldInternalError(Exception):
    pass

def callerID():
    caller = inspect.currentframe().f_back
    while not isinstance(caller.f_locals.get('self', None), Mind):
        caller = caller.f_back
    return caller.f_locals['self'].body.ID

def warn_agent(message, *args):
    print("WARNING: " + message.format(callerID(), *args))

def process_minds(white_mind, green_mind=None, orange_mind=None, observers={}):
    assert white_mind is not None
    
    if green_mind is not None:
        validate_mind(green_mind, vwc.colour.green)
        observe(green_mind, observers)
    else:
        green_mind = white_mind
        
    if orange_mind is not None:
        validate_mind(orange_mind, vwc.colour.orange)
        observe(orange_mind, observers)
    else:
        orange_mind = white_mind
    
    validate_mind(white_mind, vwc.colour.white)
    observe(white_mind, observers)
    
    return white_mind, green_mind, orange_mind

def raise_static_modification_error(agent, name, _):
    raise VacuumWorldInternalError("Agent: {0} tried to modify the static field: {1} this is cheating!")

def observe(mind, observers):
    for obs in observers:
        if not obs in set(dir(mind)):
            print("WARNING: agent attribute: {0} not defined.".format(obs))
            #raise vw.VacuumWorldInternalError("WARNING: {0} agent: must define 
            # \ the attribute: {1}, (see coursework question 1)".format(colour, obs)) 
    def sneaky_setattr(self, name, value):
        if name in observers:
            observers[name](callerID(), name, value)
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
            raise VacuumWorldInternalError("{0} agent: decide must be defined with no arguments, do(self)".format(colour))
    
    def revise_def(fun):
        if not callable(fun):
            raise VacuumWorldInternalError("{0} agent: revise must be callable".format(colour, fun.__name__))            
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
            
            
            
            
            
            
            
            