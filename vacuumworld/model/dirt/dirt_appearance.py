from pystarworldsturbo.common.identifiable import Identifiable

from ...common.colour import Colour



class VWDirtAppearance(Identifiable):
    def __init__(self, dirt_id: str, progressive_id: str, colour: Colour) -> None:
        super(VWDirtAppearance, self).__init__(identifiable_id=dirt_id, progressive_id=progressive_id)

        self.__colour: Colour = colour

    def get_colour(self) -> Colour:
        return self.__colour

    def deep_copy(self) -> "VWDirtAppearance":
        return VWDirtAppearance(dirt_id=self.get_id(), progressive_id=self.get_progressive_id(), colour=self.__colour)

    def __str__(self) -> str:
        return "dirt(colour: {})".format(self.__colour)
