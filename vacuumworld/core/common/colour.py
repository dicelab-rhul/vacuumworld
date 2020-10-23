from enum import Enum



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
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return str(self)

colour = Colour
