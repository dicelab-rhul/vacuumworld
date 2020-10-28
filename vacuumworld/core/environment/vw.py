"""
Created on Sun Jun  2 23:16:51 2019

@author: ben
"""

from typing import Dict, Tuple, Union, List

from .location_interface import Location
from ..common.orientation import Orientation
from ..common.colour import Colour
from ..common.coordinates import Coord
from ..agent.agent_interface import Agent
from ..dirt.dirt_interface import Dirt



class Grid():
    DIRECTIONS: Dict[Orientation, Tuple[int, int]] = {Orientation.north:(0,-1), Orientation.south:(0,1), Orientation.west:(-1,0), Orientation.east:(1,0)}
    
    ID_PREFIX_DIRT: str = "D-"
    ID_PREFIX_AGENT = "A-"
    
    GRID_MIN_SIZE: int = 3
    GRID_MAX_SIZE: int= 13
    
    def __init__(self, dim: int) -> None:
        self.state: Dict[Coord, Location] = None
        self.reset(dim)
        self.agent_count: int = 0
        self.dirt_count: int = 0 
        self.cycle: int = 0
       
    def replace_all(self, grid: "Grid") -> None:
        self.dim = grid.dim
        self.state = grid.state
        self.agent_count = grid.agent_count
        self.dirt_count = grid.dirt_count
        self.cycle = grid.cycle
       
    def reset(self, dim: int) -> None:
        self.cycle: int = 0
        self.state: Dict[Coord, Location] = {}

        for i in range(dim):
            for j in range(dim):
                self.state[Coord(j,i)] = Location(Coord(j,i), None, None)

            self.state[Coord(-1, i)] = None
            self.state[Coord(i, -1)] = None
            self.state[Coord(dim, i)] = None
            self.state[Coord(i, dim)] = None

        self.state[Coord(-1,-1)] = None
        self.state[Coord(-1, dim)] = None
        self.state[Coord(dim,-1)] = None
        self.state[Coord(dim, dim)] = None
        self.dim: int = dim
        self.agent_count: int = 0
        self.dirt_count: int = 0
        
    def _get_agents(self) -> Dict[Coord, Agent]:
        return {coord:location.agent for coord,location in self.state.items() if location and location.agent}
    
    def _get_dirts(self) -> Dict[Coord, Dirt]:
        return {coord:location.dirt for coord,location in self.state.items() if location and location.dirt}
        
    def _in_bounds(self, coordinate: Coord) -> bool:
        return coordinate.x >= 0 and coordinate.x < self.dim and coordinate.y >= 0 and coordinate.y < self.dim
    
    @staticmethod
    def _as_coord(coordinate: Union[Coord, List[int], Tuple[int, int]]) -> Coord:
        if not isinstance(coordinate, Coord):
            return Coord(coordinate[0], coordinate[1])

        return coordinate
    
    @staticmethod
    def _as_colour(colour: Union[Colour, str]) -> Colour:
        if not isinstance(colour, Colour):
            return Colour[colour]

        return colour

    @staticmethod      
    def _as_orientation(orientation: Union[Orientation, str]) -> Orientation:
        if not isinstance(orientation, Orientation):
            return Orientation[orientation]

        return orientation
    
    def dirt(self, colour: Union[Colour, str]) -> Dirt:
        colour: Colour = Grid._as_colour(colour)
        self.dirt_count += 1

        return Dirt(Grid.ID_PREFIX_DIRT + str(self.dirt_count), colour)
    
    def agent(self, colour: Union[Colour, str], orientation: Union[Orientation, str]) -> Agent:
        colour: Colour = Grid._as_colour(colour)
        orientation: Orientation = Grid._as_orientation(orientation)
        self.agent_count += 1

        return Agent(Grid.ID_PREFIX_AGENT + str(self.agent_count), colour, orientation)            
    
    def replace_agent(self, coordinate: Union[Coord, List[int], Tuple[int, int]], agent) -> None:
         coordinate: Coord = Grid._as_coord(coordinate)
         assert(self._in_bounds(coordinate))
         loc: Location = self.state[coordinate]
         self.state[coordinate] = Location(coordinate, agent, loc.dirt)
         
    def replace_dirt(self, coordinate: Union[Coord, List[int], Tuple[int, int]], dirt) -> None:
         coordinate: Coord = Grid._as_coord(coordinate)
         assert(self._in_bounds(coordinate))
         loc: Location = self.state[coordinate]
         self.state[coordinate] = Location(coordinate, loc.agent, dirt)
        
    def place_agent(self, coordinate: Union[Coord, List[int], Tuple[int, int]], agent) -> None:
        coordinate: Coord = Grid._as_coord(coordinate)
        assert(self._in_bounds(coordinate))
        assert(self.state[coordinate].agent == None)
        loc: Location = self.state[coordinate]
        self.state[coordinate] = Location(coordinate, agent, loc.dirt)
        
    def place_dirt(self, coordinate: Union[Coord, List[int], Tuple[int, int]], dirt) -> None:
        coordinate: Coord = Grid._as_coord(coordinate)
        assert(self._in_bounds(coordinate))
        assert(self.state[coordinate].dirt == None)
        loc: Location = self.state[coordinate]
        self.state[coordinate] = Location(coordinate, loc.agent, dirt)
    
    def remove_dirt(self, coordinate: Union[Coord, List[int], Tuple[int, int]]) -> None:
        assert(self._in_bounds(coordinate))
        loc: Location = self.state[coordinate]
        self.state[coordinate] = Location(coordinate, loc.agent, None)
        
    def remove_agent(self, coordinate: Union[Coord, List[int], Tuple[int, int]]) -> None:
        assert(self._in_bounds(coordinate))
        loc: Location = self.state[coordinate]
        self.state[coordinate] = Location(coordinate, None, loc.dirt)
        
    def move_agent(self, _from: Union[Coord, List[int], Tuple[int, int]], _to: Union[Coord, List[int], Tuple[int, int]]) -> None:
        _from: Coord = Grid._as_coord(_from)
        _to: Coord = Grid._as_coord(_to)
        assert(self.state[_from].agent != None)
        assert(self.state[_to].agent == None)
        
        from_loc: Location = self.state[_from]
        to_loc: Location = self.state[_to]
        self.state[_to] = Location(to_loc.coordinate, from_loc.agent, to_loc.dirt)
        self.state[_from] = Location(from_loc.coordinate, None, from_loc.dirt)
        
    def turn_agent(self, _coordinate: Union[Coord, List[int], Tuple[int, int]], orientation: Union[Orientation, str]) -> None:
        orientation: Orientation = Grid._as_orientation(orientation)
        assert(self.state[_coordinate].agent != None)
        loc: Location = self.state[_coordinate]
        ag: Agent = loc.agent
        self.state[_coordinate] = Location(_coordinate, Agent(ag.name, ag.colour, orientation), loc.dirt)
    
    def __str__(self) -> str:
        header: str = "{0}: size: {1}, agents: {2}, dirts: {3}, ".format(str(type(self)), self.dim, self.agent_count, self.dirt_count)
        filled: Dict[Coord, Location] = {coord:location for coord,location in self.state.items()  if location is not None and (location.agent is not None or location.dirt is not None)}
        body: str = "\n".join([str(location) for location in filled.values()])

        return "\n".join([header, body])
        
    def __repr__(self) -> str:
        return str(self)
