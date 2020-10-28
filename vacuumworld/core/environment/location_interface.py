from typing import NamedTuple, Type

from ..common.coordinates import Coord
from ..agent.agent_interface import Agent
from ..dirt.dirt_interface import Dirt



class Location(NamedTuple):
    '''
        A datastructure representing an observed location in the vacuumworld grid. 
        
        Attributes:
            * ``coordinate (vwc.coord)``: The coordinate of the location.
            * ``agent (vwc.agent)``: The agent at this location, ``None`` if there is no agent. 
            * ``dirt (vwc.dirt) ``:The dirt at this location, ``None`` if there is no dirt. 
    '''
    coordinate : Coord
    agent : Agent
    dirt : Dirt

location: Type = Location
