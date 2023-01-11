from __future__ import annotations
from typing import cast, Dict, Union, Any
from random import randint
from pyoptional.pyoptional import PyOptional

from pystarworldsturbo.environment.location_appearance import LocationAppearance

from ...common.vwcoordinates import VWCoord
from ...common.vwcolour import VWColour
from ...common.vworientation import VWOrientation
from ..dirt.vwdirt_appearance import VWDirtAppearance
from ..actor.appearance.vwactor_appearance import VWActorAppearance


class VWLocation(LocationAppearance):
    '''
    This class specifies the appearance of a four-sided location of a `VWENvironment` grid.

    A `VWLocation` is identified by its `VWCoord`, and may contain any of the following:

    * A `VWActorAppearance` (the appearance of a `VWActor`).

    * A `VWDirtAppearance` (the appearance of a `VWDirt`).

    * Both of the above.

    * None of the above.

    Each of the four sides of `VWLocation` may contain a (`bool`) wall. However, the sides exhibiting a wall must be consecutive.
    '''
    def __init__(self, coord: VWCoord, actor_appearance: PyOptional[VWActorAppearance]=PyOptional.empty(), dirt_appearance: PyOptional[VWDirtAppearance]=PyOptional.empty(), wall: Dict[VWOrientation, bool]={orientation: False for orientation in VWOrientation}) -> None:
        assert coord is not None

        self.__coord: VWCoord = coord
        self.__actor_appearance: PyOptional[VWActorAppearance] = actor_appearance
        self.__dirt_appearance: PyOptional[VWDirtAppearance] = dirt_appearance
        self.__wall: Dict[VWOrientation, bool] = wall

    def get_coord(self) -> VWCoord:
        '''
        Returns the `VWCoord` of this `VWLocation`.
        '''
        return self.__coord

    def get_actor_appearance(self) -> PyOptional[VWActorAppearance]:
        '''
        Returns a `PyOptional` wrapping the `VWActorAppearance` of the `VWActor` who is at this `VWLocation`, if any. Otherwise, returns an empty `PyOptional`.
        '''
        return self.__actor_appearance

    def remove_actor(self) -> None:
        '''
        WARNING: this method needs to be public, but is not part of the `VWLocation` API.

        Removes the `VWActorAppearance` from this `VWLocation`.

        This method assumes (via assertion) that this `VWLocation` has a `VWActorAppearance` in it.
        '''
        assert self.__actor_appearance.is_present()

        self.__actor_appearance = PyOptional.empty()

    def add_actor(self, actor_appearance: VWActorAppearance) -> None:
        '''
        WARNING: this method needs to be public, but is not part of the `VWLocation` API.

        Adds a `VWActorAppearance` to this `VWLocation` if one was not there.

        This method assumes (via assertion) that this `VWLocation` has no `VWActorAppearance` in it.
        '''
        assert self.__actor_appearance.is_empty()

        self.__actor_appearance = PyOptional.of(actor_appearance)

    def has_actor(self) -> bool:
        '''
        Returns whether or not this `VWLocation` has a `VWActor` in it, i.e., whether or not this `VWLocation` contains a `VWActorAppearance`.
        '''
        return self.__actor_appearance.is_present()

    def has_cleaning_agent(self) -> bool:
        '''
        Returns whether or not this `VWLocation` has a `VWCleaningAgent` in it, i.e., whether or not this `VWLocation` contains the `VWActorAppearance` of a `VWCleaningAgent`.
        '''
        return self.__actor_appearance.filter(lambda actor_appearance: actor_appearance.get_colour() in [VWColour.white, VWColour.green, VWColour.orange]).is_present()

    def has_user(self) -> bool:
        '''
        Returns whether or not this `VWLocation` has a `VWUser` in it, i.e., whether or not this `VWLocation` contains a `VWActorAppearance` of a `VWUser`.
        '''
        return self.__actor_appearance.filter(lambda actor_appearance: actor_appearance.get_colour() == VWColour.user).is_present()

    def is_empty(self) -> bool:
        '''
        Returns whether or not this `VWLocation` is empty.

        A `VWLocation` is empty if it contains no `VWActorAppearance` and no `VWDirtAppearance`.
        '''
        return not self.has_actor() and not self.has_dirt()

    def get_dirt_appearance(self) -> PyOptional[VWDirtAppearance]:
        '''
        Returns a `PyOptional` wrapping the `VWDirtAppearance` of the `VWDirt` which is at this `VWLocation`, if any. Otherwise, returns an empty `PyOptional`.
        '''
        return self.__dirt_appearance

    def remove_dirt(self) -> None:
        '''
        WARNING: this method needs to be public, but is not part of the `VWLocation` API.

        Removes the `VWDirtAppearance` from this `VWLocation`.

        This method assumes (via assertion) that this `VWLocation` has a `VWDirtAppearance` in it.
        '''
        assert self.__dirt_appearance.is_present()

        self.__dirt_appearance = PyOptional.empty()

    def add_dirt(self, dirt_appearance: VWDirtAppearance) -> None:
        '''
        WARNING: this method needs to be public, but is not part of the `VWLocation` API.

        Adds a `VWDirtAppearance` to this `VWLocation` if one was not there.

        This method assumes (via assertion) that this `VWLocation` has no `VWDirtAppearance` in it.
        '''
        assert self.__dirt_appearance.is_empty()

        self.__dirt_appearance = PyOptional.of(dirt_appearance)

    def has_dirt(self) -> bool:
        '''
        Returns whether or not this `VWLocation` has a `VWDirt` in it, i.e., whether or not this `VWLocation` contains a `VWDirtAppearance`.
        '''
        return self.__dirt_appearance.is_present()

    def get_wall_info(self) -> Dict[VWOrientation, bool]:
        '''
        Returns a `Dict` mapping each `VWOrientation` to a `bool` specifying whether or not there is a wall on the side of this `VWLocation` identified by that particular `VWOrientation`.
        '''
        return self.__wall

    def has_wall_on_north(self) -> bool:
        '''
        Returns whether or not this `VWLocation` has a wall on its `VWOrientation.north` side.
        '''
        return self.__wall[VWOrientation.north]

    def has_wall_on_south(self) -> bool:
        '''
        Returns whether or not this `VWLocation` has a wall on its `VWOrientation.south` side.
        '''
        return self.__wall[VWOrientation.south]

    def has_wall_on_west(self) -> bool:
        '''
        Returns whether or not this `VWLocation` has a wall on its `VWOrientation.west` side.
        '''
        return self.__wall[VWOrientation.west]

    def has_wall_on_east(self) -> bool:
        '''
        Returns whether or not this `VWLocation` has a wall on its `VWOrientation.east` side.
        '''
        return self.__wall[VWOrientation.east]

    def has_wall_on(self, orientation: VWOrientation) -> bool:
        '''
        Returns whether or not this `VWLocation` has a wall on the side identified by the `orientation` argument.
        '''
        return self.__wall[orientation]

    def has_wall_somewhere(self) -> bool:
        '''
        Returns whether or not this `VWLocation` has a wall on at least one side.
        '''
        return self.has_wall_on_north() or self.has_wall_on_south() or self.has_wall_on_west() or self.has_wall_on_east()

    def is_corner(self) -> bool:
        '''
        Returns whether or not this `VWLocation` is a corner of the `VWEnvironment` grid.

        A `VWLocation` is a corner if it has a wall on at least two consecutive sides.

        The above definition means that a 1x1 grid has exactly one corner.
        '''
        for orientation in VWOrientation:
            if self.has_wall_on(orientation):
                if self.has_wall_on(orientation=VWOrientation.get_left(orientation)) or self.has_wall_on(orientation=VWOrientation.get_right(orientation)):
                    return True

        return False

    def is_edge(self) -> bool:
        '''
        Returns whether or not this `VWLocation` is an edge of the `VWEnvironment` grid.

        A `VWLocation` is an edge if it has exactly three sides without a wall (and a wall on the remaining side).

        The above definition means that a 1x1 grid has no edges.
        '''
        for orientation in VWOrientation:
            if self.has_wall_on(orientation):
                return all(not self.has_wall_on(o) for o in VWOrientation if o != orientation)

        return False

    def deep_copy(self) -> VWLocation:
        '''
        WARNING: this method is for testing only. It is not part of the `VWLocation` API.

        Returns a deep-copy of this `VWLocation`.
        '''
        if self.__actor_appearance.is_empty() and self.__dirt_appearance.is_empty():
            return VWLocation(coord=self.__coord, actor_appearance=PyOptional.empty(), dirt_appearance=PyOptional.empty(), wall=self.__wall)
        elif self.__actor_appearance.is_present() and self.__dirt_appearance.is_empty():
            return VWLocation(coord=self.__coord, actor_appearance=self.__actor_appearance.map(lambda a: a.deep_copy()), dirt_appearance=PyOptional.empty(), wall=self.__wall)
        elif self.__actor_appearance.is_empty() and self.__dirt_appearance.is_present():
            return VWLocation(coord=self.__coord, actor_appearance=PyOptional.empty(), dirt_appearance=self.__dirt_appearance.map(lambda d: d.deep_copy()), wall=self.__wall)
        else:
            return VWLocation(coord=self.__coord, actor_appearance=self.__actor_appearance.map(lambda a: a.deep_copy()), dirt_appearance=self.__dirt_appearance.map(lambda d: d.deep_copy()), wall=self.__wall)

    def to_json(self, include_ids: bool=False) -> Dict[str, Dict[str, Any]]:
        '''
        Returns a JSON representation of this `VWLocation`.

        No `VWActor` IDs, no `VWActor` progressive IDs, and no `VWUserDifficulty` are included.
        '''
        location: Dict[str, Dict[str, Any]] = {
            "coords": self.__coord.to_json(),
            "wall": {
                str(VWOrientation.north): self.has_wall_on_north(),
                str(VWOrientation.south): self.has_wall_on_south(),
                str(VWOrientation.west): self.has_wall_on_west(),
                str(VWOrientation.east): self.has_wall_on_east()
            }
        }

        if self.has_actor():
            location["actor"] = self.__actor_appearance.map(lambda a: a.to_json() if not include_ids else a.to_json_with_ids()).or_else_raise()

        if self.has_dirt():
            location["dirt"] = self.__dirt_appearance.map(lambda d: d.to_json() if not include_ids else d.to_json_with_ids()).or_else_raise()

        return location

    def pretty_format(self, include_ids: bool=True) -> Dict[str, Union[Dict[str, str], Dict[str, int], Dict[str, bool]]]:
        '''
        Returns a pretty-formatted JSON string representation of this `VWLocation`.

        Unlike `to_json()`, the IDs and progressive IDs of each `VWActor` are included by default.
        '''
        return self.to_json(include_ids=include_ids)

    def __str__(self) -> str:
        return "(coord: {}, actor: {}, dirt: {}, wall: {})".format(str(self.__coord), str(self.__actor_appearance), str(self.__dirt_appearance), str(self.__wall))

    def __eq__(self, o: object) -> bool:
        if not o or type(o) != VWLocation:
            return False
        else:
            o = cast(typ=VWLocation, val=o)

            return self.__coord == o.get_coord() and self.__actor_appearance == o.get_actor_appearance() and self.__dirt_appearance == o.get_dirt_appearance() and self.__wall == o.get_wall_info()

    def __hash__(self) -> int:
        prime: int = 31
        result: int = 1

        result = prime * result + self.__coord.__hash__()

        if self.__actor_appearance:
            result = prime * result + self.__actor_appearance.__hash__()
        else:
            result = prime * result + 0

        if self.__dirt_appearance:
            result = prime * result + self.__dirt_appearance.__hash__()
        else:
            result = prime * result + 0

        if self.has_wall_on_north():
            result = prime * result + self.__wall[VWOrientation.north].__hash__()

        if self.has_wall_on_south():
            result = prime * result + self.__wall[VWOrientation.south].__hash__()

        if self.has_wall_on_west():
            result = prime * result + self.__wall[VWOrientation.west].__hash__()

        if self.has_wall_on_east():
            result = prime * result + self.__wall[VWOrientation.east].__hash__()

        return result

    def visualise(self) -> str:
        '''
        Returns an ASCII representation of this `VWLocation`.
        '''
        s: str = chr(164) * 7 + "\n{}{}{}\n".format(chr(164), str(self.__coord).replace(" ", ""), chr(164))

        if self.is_empty():
            s += f"{chr(164)}     {chr(164)}\n"
        elif not self.has_actor() and self.has_dirt():
            s += f"{chr(164)}  " + str(self.__dirt_appearance.map(lambda d: d.get_colour()).or_else_raise())[0] + f"  {chr(164)}\n"
        elif not self.has_dirt():
            s += f"{chr(164)}  " + str(self.__actor_appearance.map(lambda a: a.get_colour()).or_else_raise())[0].upper() + f"  {chr(164)}\n"
        else:
            s += f"{chr(164)} " + str(self.__actor_appearance.map(lambda a: a.get_colour()).or_else_raise())[0].upper() + "+" + str(self.__dirt_appearance.map(lambda d: d.get_colour()).or_else_raise())[0] + f" {chr(164)}\n"

        return s + chr(164) * 7

    @staticmethod
    def random_wall() -> Dict[VWOrientation, bool]:
        '''
        WARNING: this method is for testing only. It is not part of the `VWLocation` API.

        Generates and returns a random `Dict` mapping each `VWOrientation` to a `bool` specifying whether or not there is a wall on the side identified by that particular `VWOrientation`.
        '''
        wall: Dict[VWOrientation, bool] = {orientation: False for orientation in VWOrientation}
        roll: int = randint(1, 8)

        if roll == 1:
            wall[VWOrientation.north] = True
        elif roll == 2:
            wall[VWOrientation.south] = True
        elif roll == 3:
            wall[VWOrientation.east] = True
        elif roll == 4:
            wall[VWOrientation.west] = True
        elif roll == 5:
            wall[VWOrientation.north] = True
            wall[VWOrientation.east] = True
        elif roll == 6:
            wall[VWOrientation.north] = True
            wall[VWOrientation.west] = True
        elif roll == 7:
            wall[VWOrientation.south] = True
            wall[VWOrientation.east] = True
        elif roll == 8:
            wall[VWOrientation.south] = True
            wall[VWOrientation.west] = True

        return wall
