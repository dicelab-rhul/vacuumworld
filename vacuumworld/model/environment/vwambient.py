from typing import Dict

from pystarworldsturbo.environment.ambient import Ambient

from .vwlocation import VWLocation
from ..actor.vwactor_appearance import VWActorAppearance
from ..dirt.dirt_appearance import VWDirtAppearance
from ...common.coordinates import Coord
from ...common.direction import Direction
from ...common.observation import Observation
from ...common.position_names import PositionNames
from ...common.orientation import Orientation



class VWAmbient(Ambient):
    def __init__(self, grid: Dict[Coord, VWLocation]={}) -> None:
        self.__grid: Dict[Coord, VWLocation] = grid


    def get_grid(self) -> Dict[Coord, VWLocation]:
        return self.__grid

    def get_location_interface(self, coord: Coord) -> VWLocation:
        if coord not in self.__grid:
            return None
        else:
            return self.__grid[coord]

    def is_actor_at(self, coord: Coord) -> bool:
        return coord in self.__grid and self.__grid[coord].has_actor()

    def is_dirt_at(self, coord: Coord) -> bool:
        return coord in self.__grid and self.__grid[coord].has_dirt()

    def move_actor(self, from: Coord, to: Coord) -> None:
        assert from in self.__grid and to in self.__grid
        assert self.__grid[from].has_actor()
        assert not self.__grid[to].has_actor()

        actor: VWActorAppearance = self.__grid[from].get_actor_appearance()

        self.__grid[from].remove_actor()
        self.__grid[to].add_actor(actor_appearance=actor)

    def turn_actor(self, coord: Coord, direction: Direction) -> None:
        assert coord in self.__grid and self.__grid[coord].has_actor()

        self.__grid[coord].get_actor_appearance().turn(direction=direction)

    def drop_dirt(self, coord: Coord, dirt_appearance: VWDirtAppearance) -> None:
        assert coord in self.__grid and not self.__grid[coord].has_dirt()

        self.__grid[coord].add_dirt(dirt_appearance=dirt_appearance)

    def remove_dirt(self, coord: Coord) -> None:
        assert coord in self.__grid and self.__grid[coord].has_dirt()

        self.__grid[coord].remove_dirt()

    def generate_perception(self, coord: Coord) -> Observation:
        assert coord in self.__grid and self.__grid[coord].has_actor()

        locations_dict: Dict[PositionNames, VWLocation] = {}

        orientation: Orientation = self.__grid[coord].get_actor_appearance().get_orientation()
        
        forward_coord: Coord = coord.forward(orientation=orientation)
        left_coord: Coord = coord.left(orientation=orientation)
        right_coord: Coord = coord.right(orientation=orientation)
        forwardleft_coord: Coord = coord.forwardleft(orientation=orientation)
        forwardright_coord: Coord = coord.forwardright(orientation=orientation)

        locations_dict[PositionNames.center] = self.__grid[coord].deep_copy()

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

        return Observation(locations_dict=locations_dict)
