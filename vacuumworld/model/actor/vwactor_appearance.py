from __future__ import annotations
from typing import Dict, cast

from pystarworldsturbo.elements.actor_appearance import ActorAppearance

from ...common.colour import Colour
from ...common.orientation import Orientation
from ...common.direction import Direction


class VWActorAppearance(ActorAppearance):
    def __init__(self, actor_id: str, progressive_id: str, colour: Colour, orientation: Orientation) -> None:
        super(VWActorAppearance, self).__init__(actor_id=actor_id, progressive_id=progressive_id)

        assert colour is not None and orientation is not None

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

    def deep_copy(self) -> VWActorAppearance:
        return VWActorAppearance(actor_id=self.get_id(), progressive_id=self.get_progressive_id(), colour=self.__colour, orientation=self.__orientation)

    # Note that the actor IDs, progressive IDs, and the user difficulty level are not stored.
    # Therefore, on load the actors will have fresh IDs and progressive IDs, and the user will be in easy mode.
    def to_json(self) -> Dict[str, str]:
        return {
            "colour": str(self.__colour),
            "orientation": str(self.__orientation)
        }

    def equals_except_ids(self, obj: VWActorAppearance) -> bool:
        if self is obj:
            return True

        if type(obj) != VWActorAppearance:
            return False

        return self.__colour == obj.get_colour() and self.__orientation == obj.get_orientation() and self.__previous_orientation == obj.get_previous_orientation()

    def __str__(self) -> str:
        return "actor(ID: {}, progressive ID: {}, colour: {}, orientation: {})".format(self.get_id(), self.get_progressive_id(), self.__colour, self.__orientation)

    def __eq__(self, o: object) -> bool:
        if not o or type(o) != VWActorAppearance:
            return False

        o = cast(typ=VWActorAppearance, val=o)

        if self.get_id() != o.get_id() or self.get_progressive_id() != o.get_progressive_id():
            return False

        return self.__colour == o.get_colour() and self.__orientation == o.get_orientation() and self.__previous_orientation == o.get_previous_orientation()

    def __hash__(self) -> int:
        prime: int = 31
        result: int = 1
        result = prime * result + self.__colour.__hash__()
        result = prime * result + self.__orientation.__hash__()
        result = prime * result + self.__previous_orientation.__hash__()

        return result
