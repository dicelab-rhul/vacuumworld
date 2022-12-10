from .vwactions import VWPhysicalAction
from ...common.vwcolour import VWColour
from ...common.vwexceptions import VWMalformedActionException


class VWDropAction(VWPhysicalAction):
    '''
    This class is a `VWPhysicalAction` that drops a `VWDirt` of the specified `VWColour` onto the `VWUser`'s current location.
    '''
    def __init__(self, dirt_colour: VWColour) -> None:
        super(VWDropAction, self).__init__()

        if not dirt_colour:
            raise VWMalformedActionException("No dirt colour was specified.")
        elif dirt_colour not in [VWColour.green, VWColour.orange]:
            raise VWMalformedActionException("Invalid colour for dirt: {}.".format(dirt_colour))
        else:
            self.__dirt_colour: VWColour = dirt_colour

    def get_dirt_colour(self) -> VWColour:
        '''
        Returns the colour of the `VWDirt` to be dropped by this `VWDropAction` as a `VWColour`.
        '''
        return self.__dirt_colour
