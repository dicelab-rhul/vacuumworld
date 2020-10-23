# -*- coding: utf-8 -*-
from vacuumworld.gui.vwv import run as run_gui
from vacuumworld.utils.vwutils import process_minds

from vacuumworld.core.common.coordinates import Coord, coord
from vacuumworld.core.common.direction import Direction, direction
from vacuumworld.core.common.orientation import Orientation, orientation
from vacuumworld.core.common.colour import Colour, colour
from vacuumworld.core.common.observation import Observation, observation
from vacuumworld.core.environment.location_interface import Location, location
from vacuumworld.core.agent.agent_interface import Agent, agent
from vacuumworld.core.dirt.dirt_interface import Dirt, dirt
from vacuumworld.core.action import action

from signal import signal, SIGTSTP, SIG_IGN
from sys import exit



__all__ = ["run", Coord, Direction, Orientation, Colour, Observation, Location, Agent, Dirt, action, coord, direction, orientation, colour, observation, location, agent, dirt]


def run(default_mind=None, white_mind=None, green_mind=None, orange_mind=None, **kwargs):
    if hasattr(signal, "SIGTSTP"): # To exclude Windows and every OS without SIGTSTP.
        signal(SIGTSTP, SIG_IGN)

    white_mind, green_mind, orange_mind = process_minds(default_mind, white_mind, green_mind, orange_mind)

    try:
        run_gui({Colour.white:white_mind, Colour.green:green_mind, Colour.orange:orange_mind}, **kwargs)
    except KeyboardInterrupt:
        print("\nReceived a keyboard interrupt. Exiting...")
        exit(-1)
