from typing import NamedTuple, Type

from ..common.colour import Colour



class DirtInterface(NamedTuple):
    '''
        A datastructure representing a dirt in an observation.
        Attributes:
            * ``name  (str)``: the name of the dirt.
            * ``colour (vwc.colour)``: the colour of the dirt.
    '''
    name : str 
    colour : Colour

dirt: Type = DirtInterface
