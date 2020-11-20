from __future__ import annotations

from pystarworldsturbo.common.identifiable import Identifiable

from ...common.colour import Colour



class VWDirtAppearance(Identifiable):
    def __init__(self, dirt_id: str, progressive_id: str, colour: Colour) -> None:
        super(VWDirtAppearance, self).__init__(identifiable_id=dirt_id, progressive_id=progressive_id)

        self.__colour: Colour = colour

        self.__create_quick_api()

    def __create_quick_api(self) -> None:
        self.colour: Colour = self.__colour

    def get_colour(self) -> Colour:
        return self.__colour

    def deep_copy(self) -> VWDirtAppearance:
        return VWDirtAppearance(dirt_id=self.get_id(), progressive_id=self.get_progressive_id(), colour=self.__colour)

    def __str__(self) -> str:
        return "dirt(colour: {})".format(self.__colour)

    def __eq__(self, o: object) -> bool:
        if not o or type(o) != VWDirtAppearance:
            return False
        else:
            return self.__colour == o.get_colour() and self.get_id() == o.get_id() and self.get_progressive_id() == o.get_progressive_id()
