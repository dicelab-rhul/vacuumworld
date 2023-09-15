from __future__ import annotations
from typing import cast, Dict

from pystarworldsturbo.common.identifiable import Identifiable

from ...common.vwcolour import VWColour
from ...common.vwvalidator import VWValidator


class VWDirtAppearance(Identifiable):
    '''
    This class specifies the appearance of a `VWDirt`.

    A `VWDirt` (and, therefore, its `VWDirtAppearance`) is only characterised by its `VWColour`.
    '''
    def __init__(self, dirt_id: str, progressive_id: str, colour: VWColour) -> None:
        super(VWDirtAppearance, self).__init__(identifiable_id=dirt_id, progressive_id=progressive_id)

        assert colour is not None

        self.__colour: VWColour = colour

    def get_colour(self) -> VWColour:
        '''
        Returns the `VWColour` of the `VWDirt` this `VWDirtAppearance` refers to.
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

        No ID, progressive ID, or `VWUserDifficulty` (if applicable) are included.
        '''
        return {
            "colour": str(self.__colour)
        }

    def to_json_with_ids(self) -> Dict[str, str]:
        '''
        Returns a JSON representation of this `VWDirtAppearance`, including its ID and progressive ID.
        '''
        return {
            "id": self.get_id(),
            "progressive_id": self.get_progressive_id(),
            "colour": str(self.__colour)
        }

    def equals_except_ids(self, obj: VWDirtAppearance) -> bool:
        '''
        Returns whether or not this `VWDirtAppearance` is equal to the one (`obj`) passed as argument, without considering the IDs.

        Two `VWDirtAppearance` instances are equal, according to this method, if the `VWColour` of both instances is equal.
        '''
        if self is obj:
            return True

        if not VWValidator.does_type_match(t=VWDirtAppearance, obj=obj):
            return False

        return self.__colour == obj.get_colour()

    def __str__(self) -> str:
        return "dirt(colour: {})".format(self.__colour)

    def __eq__(self, o: object) -> bool:
        if not o or not VWValidator.does_type_match(t=VWDirtAppearance, obj=o):
            return False
        else:
            o = cast(typ=VWDirtAppearance, val=o)

            return self.__colour == o.get_colour() and self.get_id() == o.get_id() and self.get_progressive_id() == o.get_progressive_id()

    def __hash__(self) -> int:
        prime: int = 31
        result: int = 1
        result = prime * result + self.__colour.__hash__()

        return result
