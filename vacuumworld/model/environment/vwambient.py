from typing import Dict, List, Type
from math import floor, sqrt

from pystarworldsturbo.environment.ambient import Ambient
from pystarworldsturbo.common.action_result import ActionResult

from .vwlocation import VWLocation
from ..actor.appearance.vwactor_appearance import VWActorAppearance
from ..dirt.vwdirt_appearance import VWDirtAppearance
from ...common.vwcoordinates import VWCoord
from ...common.vwdirection import VWDirection
from ...common.vwobservation import VWObservation
from ...common.vwposition_names import VWPositionNames
from ...common.vworientation import VWOrientation
from ...model.actions.vwactions import VWAction


class VWAmbient(Ambient):
    '''
    This class acts as a wrapper for the grid, which is a `Dict[Coord, VWLocation]` mapping `VWCoord` objects to `VWLocation` objects.

    An API is provided to query and modify the grid.
    '''
    def __init__(self, grid: Dict[VWCoord, VWLocation]={}) -> None:
        self.__grid: Dict[VWCoord, VWLocation] = grid

    def get_grid(self) -> Dict[VWCoord, VWLocation]:
        '''
        Returns the grid as a `Dict[Coord, VWLocation]`, where each `VWCoord` is mapped to a `VWLocation`.
        '''
        return self.__grid

    def get_grid_dim(self) -> int:
        '''
        Returns the dimension of the grid as an `int`.

        The dimension of the grid is the square root of the number of `VWLocation` objects in the grid.
        '''
        number_of_locations: int = len(self.__grid)
        tmp: float = sqrt(number_of_locations)
        grid_dim: int = floor(tmp)

        assert grid_dim == tmp

        return int(grid_dim)

    def get_location_interface(self, coord: VWCoord) -> VWLocation:
        '''
        Returns the appearance of the `VWLocation` whose coordinates match the `VWCoord` argument `coord`.

        This method assumes (via assertion) that `coord` is in bounds.
        '''
        assert coord in self.__grid

        return self.__grid[coord]

    def is_actor_at(self, coord: VWCoord) -> bool:
        '''
        Returns whether or not the `VWLocation` whose coordinates match the `VWCoord` argument `coord` has a `VWActor`.

        If `coord` is not in bounds, this method returns `False`.
        '''
        return coord in self.__grid and self.__grid[coord].has_actor()

    def is_dirt_at(self, coord: VWCoord) -> bool:
        '''
        Returns whether or not the `VWLocation` whose coordinates match the `VWCoord` argument `coord` has a `VWDirt`.

        If `coord` is not in bounds, this method returns `False`.
        '''
        return coord in self.__grid and self.__grid[coord].has_dirt()

    def move_actor(self, from_coord: VWCoord, to_coord: VWCoord) -> None:
        '''
        Moves the `VWActor` from the `VWLocation` whose coordinates match the `VWCoord` argument `from_coord` to the `VWLocation` whose coordinates match the `VWCoord` argument `to_coord`.

        This method assumes the following via assertions:

        * A `VWActor` is at the `VWLocation` whose coordinates match the `VWCoord` argument `from_coord`.

        * The `VWLocation` whose coordinates match the `VWCoord` argument `to_coord` has no `VWActor`.

        * `from_coord` and `to_coord` are in bounds.
        '''
        assert from_coord in self.__grid and to_coord in self.__grid
        assert self.__grid[from_coord].has_actor()
        assert not self.__grid[to_coord].has_actor()

        actor: VWActorAppearance = self.__grid[from_coord].get_actor_appearance().or_else_raise()

        self.__grid[from_coord].remove_actor()
        self.__grid[to_coord].add_actor(actor_appearance=actor)

    def turn_actor(self, coord: VWCoord, direction: VWDirection) -> None:
        '''
        Rotates the `VWOrientation` of the `VWActor` at the `VWLocation` whose coordinates match the `VWCoord` argument `coord` as specified by the `VWDirection` argument `direction`.

        This method assumes the following via assertions:

        * A `VWActor` is at the `VWLocation` whose coordinates match the `VWCoord` argument `coord`.

        * `coord` is in bounds.
        '''
        assert coord in self.__grid and self.__grid[coord].has_actor()

        self.__grid[coord].get_actor_appearance().or_else_raise().turn(direction=direction)

    def drop_dirt(self, coord: VWCoord, dirt_appearance: VWDirtAppearance) -> None:
        '''
        Drops a `VWDirt` at the `VWLocation` whose coordinates match the `VWCoord` argument `coord`.

        The `VWDirtAppearance` of the `VWDirt` to drop is given as the `dirt_appearance` argument.

        This method assumes the following via assertions:

        * The `VWLocation` whose coordinates match the `VWCoord` argument `coord` has no `VWDirt`.

        * `coord` is in bounds.
        '''
        assert coord in self.__grid and not self.__grid[coord].has_dirt()

        self.__grid[coord].add_dirt(dirt_appearance=dirt_appearance)

    def remove_dirt(self, coord: VWCoord) -> None:
        '''
        Removes a `VWDirt` from the `VWLocation` whose coordinates match the `VWCoord` argument `coord`.

        This method assumes the following via assertions:

        * The `VWLocation` whose coordinates match the `VWCoord` argument `coord` has a `VWDirt`.

        * `coord` is in bounds.
        '''
        assert coord in self.__grid and self.__grid[coord].has_dirt()

        self.__grid[coord].remove_dirt()

    def generate_perception(self, actor_position: VWCoord, action_type: Type[VWAction], action_result:  ActionResult) -> VWObservation:
        '''
        Generates and returns a `VWObservation` perception for a `VWActor`.

        The `VWCoord` argument `actor_position` specifies the position of the `VWActor` whose perception is being generated.

        The `Type[VWAction]` argument `action_type` specifies the kind of the `VWAction` that the `VWActor` attempted.

        The `ActionResult` argument `action_result` specifies the result of the aforementioned attempted.

        The `VWObservation` returned by this method is generated as follows:

        * `VWPositionNames.center` is mapped to the `VWLocation` whose coordinates match the `VWCoord` argument `actor_position`.

        * For every other member of `VWPositionNames`, the corresponding `VWCoord` is calculated.

        * If such `VWCoord` is in bounds, then it is mapped to the `VWLocation` whose `VWCoord` matches it. Otherwise, that particular member of `VWPositionNames` is skipped.

        * Finally, `action_type` and `action_result` are added to the `VWObservation`, the former being mapped to the latter.

        This method assumes the following via assertions:

        * The `VWLocation` whose coordinates match the `VWCoord` argument `actor_position` has a `VWActor`.

        * `actor_position` is in bounds.
        '''
        assert actor_position in self.__grid and self.__grid[actor_position].has_actor()

        locations_dict: Dict[VWPositionNames, VWLocation] = {}

        orientation: VWOrientation = self.__grid[actor_position].get_actor_appearance().or_else_raise().get_orientation()

        forward_coord: VWCoord = actor_position.forward(orientation=orientation)
        left_coord: VWCoord = actor_position.left(orientation=orientation)
        right_coord: VWCoord = actor_position.right(orientation=orientation)
        forwardleft_coord: VWCoord = actor_position.forwardleft(orientation=orientation)
        forwardright_coord: VWCoord = actor_position.forwardright(orientation=orientation)

        locations_dict[VWPositionNames.center] = self.__grid[actor_position].deep_copy()

        if forward_coord in self.__grid:
            locations_dict[VWPositionNames.forward] = self.__grid[forward_coord].deep_copy()

        if left_coord in self.__grid:
            locations_dict[VWPositionNames.left] = self.__grid[left_coord].deep_copy()

        if right_coord in self.__grid:
            locations_dict[VWPositionNames.right] = self.__grid[right_coord].deep_copy()

        if forwardleft_coord in self.__grid:
            locations_dict[VWPositionNames.forwardleft] = self.__grid[forwardleft_coord].deep_copy()

        if forwardright_coord in self.__grid:
            locations_dict[VWPositionNames.forwardright] = self.__grid[forwardright_coord].deep_copy()

        return VWObservation(action_type=action_type, action_result=action_result, locations_dict=locations_dict)

    def __str__(self) -> str:
        grid_dim: int = self.get_grid_dim()
        locations_list: List[str] = []

        for i in range(grid_dim):
            for j in range(grid_dim):
                c: VWCoord = VWCoord(x=j, y=i)
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
