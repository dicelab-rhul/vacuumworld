from pystarworldsturbo.elements.body import Body

from ...common.colour import Colour



class Dirt(Body):
    def __init__(self, colour: Colour) -> None:
        assert colour in [Colour.green,  Colour.orange]

        self.__colour: Colour = colour

    def get_colour(self) -> Colour:
        return self.__colour
