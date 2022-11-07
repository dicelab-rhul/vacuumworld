from .vwactions import VWPhysicalAction
from ...common.colour import Colour
from ...common.exceptions import VWMalformedActionException


class VWDropAction(VWPhysicalAction):
    '''
    This class is a `VWPhysicalAction` that drops a `Dirt` of the specified `Colour` onto the `VWUser`'s current location.
    '''
    def __init__(self, dirt_colour: Colour) -> None:
        super(VWDropAction, self).__init__()

        if not dirt_colour:
            raise VWMalformedActionException("No dirt colour was specified.")
        elif dirt_colour not in [Colour.green, Colour.orange]:
            raise VWMalformedActionException("Invalid colour for dirt: {}.".format(dirt_colour))
        else:
            self.__dirt_colour: Colour = dirt_colour

    def get_dirt_colour(self) -> Colour:
        '''
        Returns the colour of the `Dirt` to be dropped by this `VWDropAction` as a `Colour`.
        '''
        return self.__dirt_colour
