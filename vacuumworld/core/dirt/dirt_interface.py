from typing import NamedTuple

from ..common.colour import Colour



class Dirt(NamedTuple):
    '''
        A datastructure representing a dirt in an observation.
        Attributes:
            * ``name  (str)``: the name of the dirt.
            * ``colour (vwc.colour)``: the colour of the dirt.
    '''
    name : str 
    colour : Colour

dirt = Dirt
