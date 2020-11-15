from enum import Enum
from typing import Type



class Colour(Enum):
    '''
        Representation of colour. Both dirt and agents have a colour (green, orange, white, user).
        
        * A cleaning agent may be green, orange or white;
        * A user agent always has the user colour;
        * A dirt may be green or orange.
        The colour an agent determins its cleaning capability, see ``action.clean``.
        
        Attributes:
            * ``green``
            * ``orange``
            * ``white``
            * ``user``
    '''
    
    green = "green"
    orange = "orange"
    white = "white"
    user = "user"
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)

colour: Type = Colour
