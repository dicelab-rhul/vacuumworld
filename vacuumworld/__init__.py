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

__author__ = "Benedict Wilkins"
__license__ = "GPL"
__version__ = "4.1.7"
__maintainer__ = "Benedict Wilkins"
__email__ = "zavc926@live.rhul.ac.uk"

from . import vw
from . import vwv
from . import vwc
from . import vwutils

__all__ = ('vw', 'vwv', 'vwc')

def run(white_mind, green_mind=None, orange_mind=None, **kwargs):
    '''
        This function is used to run a vacuumworld simulation. 
        
        Arguments:
            * white_mind: the mind of the white agent
            * green_mind: the mind of the green agent
            * orange_mind: the mind of the orange agent
        
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
    white_mind, green_mind, orange_mind = vwutils.process_minds(white_mind, green_mind, orange_mind, default_observe)
    
    vwv.run({vwc.colour.white:white_mind, 
             vwc.colour.green:green_mind, 
             vwc.colour.orange:orange_mind}, **kwargs)




