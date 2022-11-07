from pystarworldsturbo.elements.body import Body

from ...common.colour import Colour


class Dirt(Body):
    '''
    This class represents a piece of dirt.

    A `Dirt` object is a `Body` object with a `Colour` attribute.
    '''
    def __init__(self, colour: Colour) -> None:
        super(Dirt, self).__init__()

        assert colour in [Colour.green,  Colour.orange]

        self.__colour: Colour = colour

    def get_colour(self) -> Colour:
        '''
        Returns the `Colour` of the dirt.
        '''
        return self.__colour
