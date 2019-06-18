#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 23:16:51 2019

@author: ben
"""


from .vwc import location, dirt, agent, coord
from inspect import signature

#--------------------------------------------------------

AGENT_COLOURS = set(['user', 'orange', 'green', 'white'])
DIRT_COLOURS = set(['orange', 'green'])
DIRECTIONS = {'north':(0,-1), 'south':(0,1), 'west':(0,-1), 'east':(0,1)}

def __validate_agent(agent, colour):
    agent_dir = set(dir(agent))
    
    if not 'do' in agent_dir:
        print('ERROR:' + colour + ' agent must define the do method')
        return False
    else:
        if not callable(agent.do):
            print('ERROR:' + colour + 'agent do must be callable')
            return False
        else:
            if len(signature(agent.do).parameters) != 0:
                print('ERROR:' + colour + ': agent do must be defined with no arguments, do(self) or d()')
                return False
        
    if not 'perceive' in agent_dir:
        print('ERROR:' + colour + ' agent must define the perceive method')
        return False
    else:
        if not callable(agent.perceive):
            print('ERROR:' + colour + ' agent perceive must be callable')
            return False
        else:
             if len(signature(agent.perceive).parameters) != 1:
                print('ERROR:' + colour + ' agent perceive must be defined with one argument, perceive(self, percept) or perceive(percept)')
                return False
        
    if not 'speak' in agent_dir:
        print('ERROR:' + colour + ':agent must define the speak method')
        return False
    else:
        if not callable(agent.speak):
            print('ERROR:' + colour + ' agent speak must be callable')
            return False
        else:
             if len(signature(agent.speak).parameters) != 0:
                print('ERROR:' + colour + ' agent speak must be defined with no arguments, speak(self) or speak()')
                return False
    return True
   
    
#change the name to grid if you want!
class Environment:
    
    ID_PREFIX_DIRT = 'D-'
    ID_PREFIX_AGENT = 'A-'
    
    GRID_MIN_SIZE = 3
    GRID_MAX_SIZE = 13
    
    def __init__(self, dim):
       self.reset(dim)
       self.agent_count = 0
       self.dirt_count = 0 
       
    def reset(self, dim):
        self.state = {}
        for i in range(dim):
            for j in range(dim):
                self.state[coord(j,i)] = location(coord(j,i), None, None)
        self.dim = dim
        self.agent_count = 0
        self.dirt_count = 0
        
    def _in_bounds(self, coordinate):
        return coordinate.x >= 0 and coordinate.x < self.dim and coordinate.y >= 0 and coordinate.y < self.dim
    
    def _as_coord(self, coordinate):
        if not isinstance(coordinate, coord):
            return coord(coordinate[0], coordinate[1])
    
    def dirt(self, colour):
        assert(colour in DIRT_COLOURS)
        self.dirt_count += 1
        return dirt(Environment.ID_PREFIX_DIRT + str(self.dirt_count), colour)
    
    def agent(self, colour, direction):
        print('agent!')
        assert(colour in AGENT_COLOURS)
        assert(direction in DIRECTIONS.keys())
        self.agent_count += 1
        return agent(Environment.ID_PREFIX_AGENT + str(self.agent_count), colour, direction)            
    
    def replace_agent(self, coordinate, agent):
         coordinate = self._as_coord(coordinate)
         assert(self._in_bounds(coordinate))
         loc = self.state[coordinate]
         self.state[coordinate] = location(coordinate, agent, loc.dirt)
         
    def replace_dirt(self, coordinate, dirt):
         coordinate = self._as_coord(coordinate)
         assert(self._in_bounds(coordinate))
         loc = self.state[coordinate]
         self.state[coordinate] = location(coordinate, loc.agent, dirt)
        
    def place_agent(self, coordinate, agent):
        coordinate = self._as_coord(coordinate)
        assert(self._in_bounds(coordinate))
        assert(self.state[coordinate].agent == None)
        loc = self.state[coordinate]
        self.state[coordinate] = location(coordinate, agent, loc.dirt)
        
    def place_dirt(self, coordinate, dirt):
        coordinate = self._as_coord(coordinate)
        assert(self._in_bounds(coordinate))
        assert(self.state[coordinate].dirt == None)
        loc = self.state[coordinate]
        self.state[coordinate] = location(coordinate, loc.agent, dirt)
        
    def move_agent(self, _from, _to):
        _from = self._as_coord(_from)
        _to = self._as_coord(_to)
        assert(self.state[_from].agent != None)
        assert(self.state[_to].agent == None)
        from_loc = self.state[_from]
        to_loc = self.state[_to]
        self.state[_to] = location(to_loc.coordinate, to_loc.dirt, from_loc.agent)
        self.state[_from] = location(from_loc.coordinate, from_loc.dirt, None)
        
    def turn_agent(self, _coordinate, direction):
        assert(self.state[_coordinate].agent != None)
        loc = self.state[_coordinate]
        ag = loc.agent
        self.state[_coordinate] = location(_coordinate, loc.dirt, agent(ag.name, ag.colour, direction))
