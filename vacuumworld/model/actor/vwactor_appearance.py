from pystarworldsturbo.elements.actor_appearance import ActorAppearance

from ...common.colour import Colour
from ...common.orientation import Orientation
from ...common.direction import Direction



class VWActorAppearance(ActorAppearance):
    def __init__(self, actor_id: str, progressive_id: str, colour: Colour, orientation: Orientation) -> None:
        super(VWActorAppearance, self).__init__(actor_id=actor_id, progressive_id=progressive_id)

        self.__colour: Colour = colour
        self.__orientation: Orientation = orientation
        self.__previous_orientation: Orientation = self.__orientation

    def get_colour(self) -> Colour:
        return self.__colour

    def get_orientation(self) -> Orientation:
        return self.__orientation

    def get_previous_orientation(self) -> Orientation:
        return self.__previous_orientation

    def turn(self, direction: Direction) -> None:
        self.__previous_orientation = self.__orientation
        self.__orientation = self.__orientation.get(direction=direction)

    def deep_copy(self) -> "VWActorAppearance":
        return VWActorAppearance(actor_id=self.get_id(), progressive_id=self.get_progressive_id(), colour=self.__colour, orientation=self.__orientation)
