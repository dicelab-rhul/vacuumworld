from __future__ import annotations
from typing import cast, Dict

from pystarworldsturbo.common.identifiable import Identifiable

from ...common.colour import Colour


class VWDirtAppearance(Identifiable):
    '''
    This class specifies the appearance of a `VWDirt`.

    A `VWDirt` (and, therefore, its `VWDirtAppearance`) is only characterised by its `Colour`.
    '''
    def __init__(self, dirt_id: str, progressive_id: str, colour: Colour) -> None:
        super(VWDirtAppearance, self).__init__(identifiable_id=dirt_id, progressive_id=progressive_id)

        assert colour is not None

        self.__colour: Colour = colour

    def get_colour(self) -> Colour:
        '''
        Returns the `Colour` of the `Dirt` this `VWDirtAppearance` refers to.
        '''
        return self.__colour

    def deep_copy(self) -> VWDirtAppearance:
        '''
        WARNING: this method needs to be public, but is not part of the `VWDirtAppearance` API.

        Returns a deep-copy of this `VWDirtAppearance`.
        '''
        return VWDirtAppearance(dirt_id=self.get_id(), progressive_id=self.get_progressive_id(), colour=self.__colour)

    def to_json(self) -> Dict[str, str]:
        '''
        Returns a JSON representation of this `VWDirtAppearance`.
        '''
        return {
            "colour": str(self.__colour)
        }

    def equals_except_ids(self, obj: VWDirtAppearance) -> bool:
        '''
        Returns whether or not this `VWDirtAppearance` is equal to the one (`obj`) passed as argument, without considering the IDs.

        Two `VWDirtAppearance` instances are equal, according to this method, if the `Colour` of both instances is equal.
        '''
        if self is obj:
            return True

        if type(obj) != VWDirtAppearance:
            return False

        return self.__colour == obj.get_colour()

    def __str__(self) -> str:
        return "dirt(colour: {})".format(self.__colour)

    def __eq__(self, o: object) -> bool:
        if not o or type(o) != VWDirtAppearance:
            return False
        else:
            o = cast(typ=VWDirtAppearance, val=o)

            return self.__colour == o.get_colour() and self.get_id() == o.get_id() and self.get_progressive_id() == o.get_progressive_id()

    def __hash__(self) -> int:
        prime: int = 31
        result: int = 1
        result = prime * result + self.__colour.__hash__()

        return result
