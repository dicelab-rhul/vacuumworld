from typing import Dict, List, Type
from math import floor, sqrt

from pystarworldsturbo.environment.ambient import Ambient
from pystarworldsturbo.common.action_result import ActionResult

from .vwlocation import VWLocation
from ..actor.vwactor_appearance import VWActorAppearance
from ..dirt.dirt_appearance import VWDirtAppearance
from ...common.coordinates import Coord
from ...common.direction import Direction
from ...common.observation import Observation
from ...common.position_names import PositionNames
from ...common.orientation import Orientation
from ...model.actions.vwactions import VWAction


class VWAmbient(Ambient):
    '''
    This class acts as a wrapper for the grid, which is a `Dict[Coord, VWLocation]` mapping `Coord` objects to `VWLocation` objects.

    An API is provided to query and modify the grid.
    '''
    def __init__(self, grid: Dict[Coord, VWLocation]={}) -> None:
        self.__grid: Dict[Coord, VWLocation] = grid

    def get_grid(self) -> Dict[Coord, VWLocation]:
        '''
        Returns the grid as a `Dict[Coord, VWLocation]`, where each `Coord` is mapped to a `VWLocation`.
        '''
        return self.__grid

    def get_grid_dim(self) -> int:
        '''
        Returns the dimension of the grid as an `int`.

        The dimension of the grid is the square root of the number of `VWLocation` objects in the grid.
        '''
        number_of_locations: int = len(self.__grid)
        grid_dim: int = sqrt(number_of_locations)

        assert floor(grid_dim) == grid_dim

        return int(grid_dim)

    def get_location_interface(self, coord: Coord) -> VWLocation:
        '''
        Returns the appearance of the `VWLocation` whose coordinates match the `Coord` argument.

        This method assumes (via assertion) that `coord` is in bounds.
        '''
        assert coord in self.__grid

        return self.__grid[coord]

    def is_actor_at(self, coord: Coord) -> bool:
        '''
        Returns whether or not the `VWLocation` whose coordinates match the `Coord` argument has a `VWActor`.

        If `coord` is not in bounds, this method returns `False`.
        '''
        return coord in self.__grid and self.__grid[coord].has_actor()

    def is_dirt_at(self, coord: Coord) -> bool:
        '''
        Returns whether or not the `VWLocation` whose coordinates match the `Coord` argument has a `Dirt`.

        If `coord` is not in bounds, this method returns `False`.
        '''
        return coord in self.__grid and self.__grid[coord].has_dirt()

    def move_actor(self, from_coord: Coord, to_coord: Coord) -> None:
        '''
        Moves the `VWActor` from the `VWLocation` whose coordinates match the `Coord` argument `from_coord` to the `VWLocation` whose coordinates match the `Coord` argument `to_coord`.

        This method assumes the following via assertions:

        * A `VWActor` is at the `VWLocation` whose coordinates match the `Coord` argument `from_coord`.

        * The `VWLocation` whose coordinates match the `Coord` argument `to_coord` has no `VWActor`.

        * `from_coord` and `to_coord` are in bounds.
        '''
        assert from_coord in self.__grid and to_coord in self.__grid
        assert self.__grid[from_coord].has_actor()
        assert not self.__grid[to_coord].has_actor()

        actor: VWActorAppearance = self.__grid[from_coord].get_actor_appearance()

        self.__grid[from_coord].remove_actor()
        self.__grid[to_coord].add_actor(actor_appearance=actor)

    def turn_actor(self, coord: Coord, direction: Direction) -> None:
        '''
        Rotates the `Orientation` of the `VWActor` at the `VWLocation` whose coordinates match the `Coord` argument `coord` as specified by the `Direction` argument `direction`.

        This method assumes the following via assertions:

        * A `VWActor` is at the `VWLocation` whose coordinates match the `Coord` argument `coord`.

        * `coord` is in bounds.
        '''
        assert coord in self.__grid and self.__grid[coord].has_actor()

        self.__grid[coord].get_actor_appearance().turn(direction=direction)

    def drop_dirt(self, coord: Coord, dirt_appearance: VWDirtAppearance) -> None:
        '''
        Drops a `Dirt` at the `VWLocation` whose coordinates match the `Coord` argument `coord`.

        The `VWDirtAppearance` of the `Dirt` to drop is given as the `dirt_appearance` argument.

        This method assumes the following via assertions:

        * The `VWLocation` whose coordinates match the `Coord` argument `coord` has no `Dirt`.

        * `coord` is in bounds.
        '''
        assert coord in self.__grid and not self.__grid[coord].has_dirt()

        self.__grid[coord].add_dirt(dirt_appearance=dirt_appearance)

    def remove_dirt(self, coord: Coord) -> None:
        '''
        Removes a `Dirt` from the `VWLocation` whose coordinates match the `Coord` argument `coord`.

        This method assumes the following via assertions:

        * The `VWLocation` whose coordinates match the `Coord` argument `coord` has a `Dirt`.

        * `coord` is in bounds.
        '''
        assert coord in self.__grid and self.__grid[coord].has_dirt()

        self.__grid[coord].remove_dirt()

    def generate_perception(self, actor_position: Coord, action_type: Type[VWAction], action_result:  ActionResult) -> Observation:
        '''
        Generates and returns an `Observation` perception for a `VWActor`.

        The `Coord` argument `actor_position` specifies the position of the `VWActor` whose perception is being generated.

        The `Type[VWAction]` argument `action_type` specifies the kind of the `VWAction` that the `VWActor` attempted.

        The `ActionResult` argument `action_result` specifies the result of the aforementioned attempted.

        The `Observation` returned by this method is generated as follows:

        * `PositionNames.center` is mapped to the `VWLocation` whose coordinates match the `Coord` argument `actor_position`.

        * For every other member of `PositionNames`, the corresponding `Coord` is calculated.

        * If such `Coord` is in bounds, then it is mapped to the `VWLocation` whose `Coord` matches it. Otherwise, that particular member of `PositionNames` is skipped.

        * Finally, `action_type` and `action_result` are added to the `Observation`, the former being mapped to the latter.

        This method assumes the following via assertions:

        * The `VWLocation` whose coordinates match the `Coord` argument `actor_position` has a `VWActor`.

        * `actor_position` is in bounds.
        '''
        assert actor_position in self.__grid and self.__grid[actor_position].has_actor()

        locations_dict: Dict[PositionNames, VWLocation] = {}

        orientation: Orientation = self.__grid[actor_position].get_actor_appearance().get_orientation()

        forward_coord: Coord = actor_position.forward(orientation=orientation)
        left_coord: Coord = actor_position.left(orientation=orientation)
        right_coord: Coord = actor_position.right(orientation=orientation)
        forwardleft_coord: Coord = actor_position.forwardleft(orientation=orientation)
        forwardright_coord: Coord = actor_position.forwardright(orientation=orientation)

        locations_dict[PositionNames.center] = self.__grid[actor_position].deep_copy()

        if forward_coord in self.__grid:
            locations_dict[PositionNames.forward] = self.__grid[forward_coord]

        if left_coord in self.__grid:
            locations_dict[PositionNames.left] = self.__grid[left_coord]

        if right_coord in self.__grid:
            locations_dict[PositionNames.right] = self.__grid[right_coord]

        if forwardleft_coord in self.__grid:
            locations_dict[PositionNames.forwardleft] = self.__grid[forwardleft_coord]

        if forwardright_coord in self.__grid:
            locations_dict[PositionNames.forwardright] = self.__grid[forwardright_coord]

        return Observation(action_type=action_type, action_result=action_result, locations_dict=locations_dict)

    def __str__(self) -> str:
        grid_dim: int = self.get_grid_dim()
        locations_list: List[str] = []

        for i in range(grid_dim):
            for j in range(grid_dim):
                c: Coord = Coord(x=j, y=i)
                locations_list.append(self.__grid[c].visualise())

        partial_representation: str = VWAmbient.__compactify(grid_dim=grid_dim, locations_list=locations_list)
        streamlined_representation: str = VWAmbient.__streamline(grid_dim=grid_dim, partial_representation=partial_representation)

        return VWAmbient.__highlight_walls(streamlined_representation=streamlined_representation)

    @staticmethod
    def __compactify(grid_dim: int, locations_list: List[str]) -> str:
        partial_representation: str = ""

        for _ in range(grid_dim):
            tmp: List[str] = locations_list[:grid_dim]

            for i in range(4):
                for location in tmp:
                    partial_representation += location.split("\n")[i]
                partial_representation += "\n"

            if len(locations_list) > grid_dim:
                locations_list = locations_list[grid_dim:]

        return partial_representation

    @staticmethod
    def __streamline(grid_dim: int, partial_representation: str) -> str:
        p1_new: str = (chr(164) * 7 * grid_dim) + "\n"
        p1: str = p1_new * 2

        p2: str = p1_new
        p2_new: str = p2[grid_dim - 1:]

        return partial_representation.replace(p1, p1_new[grid_dim - 1:]).replace(p2, p2_new).replace(f"{chr(164)}{chr(164)} ", f"{chr(164)} ").replace(f" {chr(164)}{chr(164)}", f" {chr(164)}").replace(f"{chr(164)}{chr(164)}(", f"{chr(164)}(").replace(f"){chr(164)}{chr(164)}", f"){chr(164)}")

    @staticmethod
    def __highlight_walls(streamlined_representation: str) -> str:
        tokens: List[str] = streamlined_representation.split("\n")

        tokens[0] = tokens[0].replace(chr(164), "#")
        tokens[-2] = tokens[-2].replace(chr(164), "#")

        for i in range(len(tokens) - 1):
            if tokens[i][0] == chr(164):
                tokens[i] = "#" + tokens[i][1:]
            if tokens[i][-1] == chr(164):
                tokens[i] = tokens[i][:-1] + "#"

        return "\n".join(tokens)
