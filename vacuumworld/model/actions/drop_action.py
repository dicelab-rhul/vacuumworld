from .vwactions import VWPhysicalAction
from ..actor.vwactor_appearance import VWActorAppearance
from ...common.colour import Colour
from ...utils.exceptions import VWMalformedActionException



class VWDropAction(VWPhysicalAction):
    def __init__(self, dirt_colour: Colour, actor_appearance: VWActorAppearance) -> None:
        super(VWDropAction, self).__init__(actor_appearance=actor_appearance)

        if not dirt_colour:
            raise VWMalformedActionException("No dirt colour was specified.")
        elif dirt_colour in [Colour.green, Colour.orange]:
            raise VWMalformedActionException("Invalid colour for dirt: {}.".format(dirt_colour))
        else:
            self.__dirt_colour: Colour = dirt_colour

    def get_dirt_colour(self) -> Colour:
        return self.__dirt_colour
