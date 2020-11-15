from typing import NamedTuple, Type

from ..common.colour import Colour
from ..common.orientation import Orientation



class Actor(NamedTuple):
    '''
        A datastructure representing an agent in an observation.
        
        Attributes:
            * ``name (str)``: the name of the agent.
            * ``colour (vwc.colour)``:  the colour of the agent.
            * ``orientation (vwc.orientation)``: the orientation of the agent.
    '''
    name : str
    colour : Colour
    orientation : Orientation

actor: Type = Actor
