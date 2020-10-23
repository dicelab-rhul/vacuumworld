# -*- coding: utf-8 -*-
from .gui.vwv import run as run_gui
from .utils.vwutils import process_minds


from vacuumworld.core.common.coordinates import Coord, coord
from vacuumworld.core.common.direction import Direction, direction
from vacuumworld.core.common.orientation import Orientation, orientation
from vacuumworld.core.common.colour import Colour, colour
from vacuumworld.core.common.observation import Observation, observation
from vacuumworld.core.environment.location_interface import Location, location
from vacuumworld.core.agent.agent_interface import Agent, agent
from vacuumworld.core.dirt.dirt_interface import Dirt, dirt
from vacuumworld.core.action import action


import signal

__all__ = ["run", Coord, Direction, Orientation, Colour, Observation, Location, Agent, Dirt, action, coord, direction, orientation, colour, observation, location, agent, dirt]

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


def ignore_ctrl_z(*_):
    print("\nCTRL+Z is ignored by VacuumWorld, use CTRL+C.")
    signal.SIG_IGN


if hasattr(signal, "SIGTSTP") and hasattr(signal, "SIGINT"): # To exclude Windows which does not have SIGTSTP
    signal.signal(signal.SIGTSTP, ignore_ctrl_z)


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

    white_mind, green_mind, orange_mind = process_minds(default_mind, white_mind, green_mind, orange_mind)
    
    try:
        run_gui({Colour.white:white_mind, Colour.green:green_mind, Colour.orange:orange_mind}, **kwargs)
    except KeyboardInterrupt:
        print("\nReceived a keyboard interrupt. Exiting...")
