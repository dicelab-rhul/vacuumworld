from pystarworldsturbo.elements.body import Body

from ...common.vwcolour import VWColour


class VWDirt(Body):
    '''
    This class represents a piece of dirt.

    A `VWDirt` object is a `Body` object with a `VWColour` attribute.
    '''
    def __init__(self, colour: VWColour) -> None:
        super(VWDirt, self).__init__()

        assert colour in [VWColour.green,  VWColour.orange]

        self.__colour: VWColour = colour

    def get_colour(self) -> VWColour:
        '''
        Returns the `VWColour` of the dirt.
        '''
        return self.__colour
