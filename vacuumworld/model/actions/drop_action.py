from .vwactions import VWPhysicalAction
from ...common.colour import Colour
from ...common.exceptions import VWMalformedActionException


class VWDropAction(VWPhysicalAction):
    def __init__(self, dirt_colour: Colour) -> None:
        super(VWDropAction, self).__init__()

        if not dirt_colour:
            raise VWMalformedActionException("No dirt colour was specified.")
        elif dirt_colour not in [Colour.green, Colour.orange]:
            raise VWMalformedActionException("Invalid colour for dirt: {}.".format(dirt_colour))
        else:
            self.__dirt_colour: Colour = dirt_colour

    def get_dirt_colour(self) -> Colour:
        return self.__dirt_colour
