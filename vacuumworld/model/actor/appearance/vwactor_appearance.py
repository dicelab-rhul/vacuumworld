from __future__ import annotations
from typing import cast

from pystarworldsturbo.elements.actor_appearance import ActorAppearance

from ....common.vwcolour import VWColour
from ....common.vworientation import VWOrientation
from ....common.vwdirection import VWDirection
from ....common.vwvalidator import VWValidator


class VWActorAppearance(ActorAppearance):
    '''
    This class represents the appearance of a `VWActor`.
    '''
    def __init__(self, actor_id: str, progressive_id: str, colour: VWColour, orientation: VWOrientation) -> None:
        super(VWActorAppearance, self).__init__(actor_id=actor_id, progressive_id=progressive_id)

        assert colour is not None and orientation is not None

        self.__colour: VWColour = colour
        self.__orientation: VWOrientation = orientation
        self.__previous_orientation: VWOrientation = self.__orientation

    def get_colour(self) -> VWColour:
        '''
        Returns the `VWColour` of the `VWActor` this `VWActorAppearance` refers to.
        '''
        return self.__colour

    def get_orientation(self) -> VWOrientation:
        '''
        Returns the current `VWOrientation` of the `VWActor` this `VWActorAppearance` refers to.
        '''
        return self.__orientation

    def is_facing_north(self) -> bool:
        '''
        Returns whether or not the `VWActor` this `VWActorAppearance` refers to is facing `VWOrientation.north`.
        '''
        return self.__orientation == VWOrientation.north

    def is_facing_east(self) -> bool:
        '''
        Returns whether or not the `VWActor` this `VWActorAppearance` refers to is facing `VWOrientation.east`.
        '''
        return self.__orientation == VWOrientation.east

    def is_facing_south(self) -> bool:
        '''
        Returns whether or not the `VWActor` this `VWActorAppearance` refers to is facing `VWOrientation.south`.
        '''
        return self.__orientation == VWOrientation.south

    def is_facing_west(self) -> bool:
        '''
        Returns whether or not the `VWActor` this `VWActorAppearance` refers to is facing `VWOrientation.west`.
        '''
        return self.__orientation == VWOrientation.west

    def is_facing(self, orientation: VWOrientation) -> bool:
        '''
        Returns whether or not the `VWActor` this `VWActorAppearance` refers to is facing the `VWOrientation` passed as argument.
        '''
        return self.__orientation == orientation

    def get_previous_orientation(self) -> VWOrientation:
        '''
        Returns the backed-up `VWOrientation` of the `VWActor` this `VWActorAppearance` refers to.

        A `VWOrientation` is normally backed up just before a turn left/right.

        If no `VWOrientation` was ever backed up, the returned backed-up `VWOrientation` should be equal to the current `VWOrientation`.
        '''
        return self.__previous_orientation

    def turn(self, direction: VWDirection) -> None:
        '''
        WARNING: this method needs to be public, but is not part of the `VWDirtAppearance` API.

        Turns the `VWOrientation` of this `VWActorAppearance` according to the `direction` argument, and backs-up the old `VWOrientation` (overwriting the previous back-up).
        '''
        self.__previous_orientation = self.__orientation
        self.__orientation = self.__orientation.get(direction=direction)

    def deep_copy(self) -> VWActorAppearance:
        '''
        WARNING: this method needs to be public, but is not part of the `VWActorAppearance` API.

        Returns a deep-copy of this `VWActorAppearance`.
        '''
        return VWActorAppearance(actor_id=self.get_id(), progressive_id=self.get_progressive_id(), colour=self.__colour, orientation=self.__orientation)

    # Note that the actor IDs, progressive IDs, and the user difficulty level are not stored.
    # Therefore, on load the actors will have fresh IDs and progressive IDs, and the user will be in whichever mode is the default one.
    def to_json(self) -> dict[str, str]:
        '''
        Returns a JSON representation of this `VWActorAppearance`.

        No ID, progressive ID, or `VWUserDifficulty` (if applicable) are included.
        '''
        return {
            "colour": str(self.__colour),
            "orientation": str(self.__orientation)
        }

    def to_json_with_ids(self) -> dict[str, str]:
        '''
        Returns a JSON representation of this `VWActorAppearance`.

        The ID, progressive ID, are included.

        `VWUserDifficulty` is not included (if applicable).
        '''
        return {
            "id": self.get_id(),
            "progressive_id": self.get_progressive_id(),
            "colour": str(self.__colour),
            "orientation": str(self.__orientation)
        }

    def equals_except_ids(self, obj: VWActorAppearance) -> bool:
        '''
        Returns whether or not this `VWActorAppearance` is equal to the one (`obj`) passed as argument, without considering the IDs, and the progressive IDs.

        Two `VWActor` instances are equal, according to this method, if the `VWColour`, the `VWOrientation`, and the previous `VWOrientation` (with respect to an environmental cycle) of both instances are equal.
        '''
        if self is obj:
            return True

        if not VWValidator.does_type_match(t=VWActorAppearance, obj=obj):
            return False

        return self.__colour == obj.get_colour() and self.__orientation == obj.get_orientation() and self.__previous_orientation == obj.get_previous_orientation()

    def __str__(self) -> str:
        return f"actor(ID: {self.get_id()}, progressive ID: {self.get_progressive_id()}, colour: {self.__colour}, orientation: {self.__orientation})"

    def __eq__(self, o: object) -> bool:
        if not o or not VWValidator.does_type_match(t=VWActorAppearance, obj=o):
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
