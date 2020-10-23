# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 23:16:51 2019

@author: ben
"""

from random import choice, sample

from .location_interface import Location
from .vwenvironment import GridEnvironment, GridAmbient
from ..common.orientation import Orientation
from ..common.colour import Colour
from ..common.coordinates import Coord
from ..agent.agent_interface import Agent
from ..dirt.dirt_interface import Dirt


#--------------------------------------------------------

def init(grid, minds):
    return GridEnvironment(GridAmbient(grid, minds))

def minds(mind):
    return {colour:mind for colour in Colour}

def random_grid(size, white, green, orange, user, orange_dirt, green_dirt):
    assert green + white + orange + user <= size * size
    assert orange_dirt + green_dirt <= size * size

    grid = Grid(size)

    #for agents
    coords = sample([key for key,value in grid.state.items() if value is not None] , k = green + white + orange + user)
    agents = {Colour.white:white, Colour.orange:orange, Colour.green:green, Colour.user:user}

    for c, num in agents.items():
        for _ in range(num):
            grid.place_agent(coords.pop(-1), grid.agent(c, choice(Orientation)))

    #for dirts
    dirts = {Colour.orange:orange_dirt,Colour.green:green_dirt}
    coords = sample([key for key,value in grid.state.items() if value is not None] , k = orange_dirt + green_dirt)

    for c, num in dirts.items():
        for _ in range(num):
            grid.place_dirt(coords.pop(-1), grid.dirt(c))

    return grid

class Grid():
    DIRECTIONS = {Orientation.north:(0,-1), Orientation.south:(0,1), Orientation.west:(-1,0), Orientation.east:(1,0)}
    
    ID_PREFIX_DIRT = 'D-'
    ID_PREFIX_AGENT = 'A-'
    
    GRID_MIN_SIZE = 3
    GRID_MAX_SIZE = 13
    
    def __init__(self, dim):
        self.state = None
        self.reset(dim)
        self.agent_count = 0
        self.dirt_count = 0 
        self.cycle = 0
       
    def replace_all(self, grid):
        self.dim = grid.dim
        self.state = grid.state
        self.agent_count = grid.agent_count
        self.dirt_count = grid.dirt_count
        self.cycle = grid.cycle
       
    def reset(self, dim):
        self.cycle = 0
        self.state = {}

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
        self.dim = dim
        self.agent_count = 0
        self.dirt_count = 0
        
    def _get_agents(self):
        return {coord:location.agent for coord,location in self.state.items() if location and location.agent}
    
    def _get_dirts(self):
        return {coord:location.dirt for coord,location in self.state.items() if location and location.dirt}
        
    def _in_bounds(self, coordinate):
        return coordinate.x >= 0 and coordinate.x < self.dim and coordinate.y >= 0 and coordinate.y < self.dim
    
    @staticmethod
    def _as_coord(coordinate):
        if not isinstance(coordinate, Coord):
            return Coord(coordinate[0], coordinate[1])

        return coordinate
    
    @staticmethod
    def _as_colour(colour):
        if not isinstance(colour, Colour):
            return Colour[colour]

        return colour

    @staticmethod      
    def _as_orientation(orientation):
        if not isinstance(orientation, Orientation):
            return Orientation[orientation]

        return orientation
    
    def dirt(self, colour):
        colour = Grid._as_colour(colour)
        self.dirt_count += 1
        return Dirt(Grid.ID_PREFIX_DIRT + str(self.dirt_count), colour)
    
    def agent(self, colour, orientation):
        colour = Grid._as_colour(colour)
        orientation = Grid._as_orientation(orientation)
        self.agent_count += 1
        return Agent(Grid.ID_PREFIX_AGENT + str(self.agent_count), colour, orientation)            
    
    def replace_agent(self, coordinate, agent):
         coordinate = Grid._as_coord(coordinate)
         assert(self._in_bounds(coordinate))
         loc = self.state[coordinate]
         self.state[coordinate] = Location(coordinate, agent, loc.dirt)
         
    def replace_dirt(self, coordinate, dirt):
         coordinate = Grid._as_coord(coordinate)
         assert(self._in_bounds(coordinate))
         loc = self.state[coordinate]
         self.state[coordinate] = Location(coordinate, loc.agent, dirt)
        
    def place_agent(self, coordinate, agent):
        coordinate = Grid._as_coord(coordinate)
        assert(self._in_bounds(coordinate))
        assert(self.state[coordinate].agent == None)
        loc = self.state[coordinate]
        self.state[coordinate] = Location(coordinate, agent, loc.dirt)
        
    def place_dirt(self, coordinate, dirt):
        coordinate = Grid._as_coord(coordinate)
        assert(self._in_bounds(coordinate))
        assert(self.state[coordinate].dirt == None)
        loc = self.state[coordinate]
        self.state[coordinate] = Location(coordinate, loc.agent, dirt)
    
    def remove_dirt(self, coordinate):
        assert(self._in_bounds(coordinate))
        loc = self.state[coordinate]
        self.state[coordinate] = Location(coordinate, loc.agent, None)
        
    def remove_agent(self, coordinate):
        assert(self._in_bounds(coordinate))
        loc = self.state[coordinate]
        self.state[coordinate] = Location(coordinate, None, loc.dirt)
        
    def move_agent(self, _from, _to):
        _from = Grid._as_coord(_from)
        _to = Grid._as_coord(_to)
        assert(self.state[_from].agent != None)
        assert(self.state[_to].agent == None)
        
        from_loc = self.state[_from]
        to_loc = self.state[_to]
        self.state[_to] = Location(to_loc.coordinate, from_loc.agent, to_loc.dirt)
        self.state[_from] = Location(from_loc.coordinate, None, from_loc.dirt)
        
    def turn_agent(self, _coordinate, orientation):
        orientation = Grid._as_orientation(orientation)
        assert(self.state[_coordinate].agent != None)
        loc = self.state[_coordinate]
        ag = loc.agent
        self.state[_coordinate] = Location(_coordinate, Agent(ag.name, ag.colour, orientation), loc.dirt)
    
    def __str__(self):
        header = "{0}: size: {1}, agents: {2}, dirts: {3}, ".format(str(type(self)), self.dim, self.agent_count, self.dirt_count)
        filled = {coord:location for coord,location in self.state.items()  if location is not None and (location.agent is not None or location.dirt is not None)}
        body = "\n".join([str(location) for location in filled.values()])
        return "\n".join([header, body])
        
    def __repr__(self):
        return str(self)
