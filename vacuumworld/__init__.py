#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Welcome to Vacuum World! Before you start, we suggest reading the Vacuum World 
Guide available on the course moodle page. It will give you all the information you need 
to get started.

To start a VacuumWorld simulation you should start by creating a new .py file `test.py` with the following template:

test.py
------------
::
    
    import vacuumworld
    from vwc import action, orientation, direction, colour
    
    class Mind:
        
        def __init__(self):
            pass
            
        def decide(self):
            pass
            
        def revise(self, observation, messages):
            pass
            
This is the template of an agents mind, in this course we are using a simple architecture for agent decision making,
the `decide` and `revise` methods are key in this. For more information and examples check the Guide!
"""

import signal

def ignore_ctrl_z(*_):
    print("\nCTRL+Z is ignored by VacuumWorld, use CTRL+C.")
    signal.SIG_IGN

signal.signal(signal.SIGTSTP, ignore_ctrl_z)



from . import vwv
from . import vwc
from . import vwutils

__all__ = ('vw', 'vwv', 'vwc')

def run(default_mind=None, white_mind=None, green_mind=None, orange_mind=None, **kwargs):
    '''
        This function is used to run a vacuumworld simulation. 
        
        Arguments:
            * default_mind: the default mind for all agents. Can be overridden for specific agents by white_mind, green_mind, and orange_mind.
            * white_mind: the mind for white agents.
            * green_mind: the mind for green agents.
            * orange_mind: the mind for orange agents.
        
        If `green_mind` or `orange_mind` are not specified, `white_mind` will be
        used for these agents.
        
        Optional Arguments:
            * `skip (bool)`: `True` skips the welcome screen, default `False`. 
            * `play (bool)`: `True` automatically plays the simulation (requires `load=True`), default `False`.
            * `load (str)`: File name of a simulation to load (e.g. `test.vw`), default `None`.
            * `speed (float [0-1])`: simulation speed from 0-1, 0 = slow, 1 = fast, default 0.
            * `scale (float)`: scales the graphics (e.g. 2 will scale 2x), default 1.
            
        Example
        -------
        ::
            
            import vacuumworld
            
            class Mind:
                ...
                
            vacuumworld.run(Mind(), skip=True, play=True, load='test.vw')
    '''
    
    default_observe = {'grid_size':vwutils.print_observer}
    white_mind, green_mind, orange_mind = vwutils.process_minds(default_mind, white_mind, green_mind, orange_mind, default_observe)
    
    try:
        vwv.run({vwc.Colour.white:white_mind, vwc.Colour.green:green_mind, vwc.Colour.orange:orange_mind}, **kwargs)
    except KeyboardInterrupt:
        print("\nReceived a keyboard interrupt. Exiting...")
