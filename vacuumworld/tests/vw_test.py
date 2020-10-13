# -*- coding: utf-8 -*-
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(myPath))


from ..vw import Grid
from ..vwc import Coord, Orientation

def test_wall_locations_exist():
    grid = Grid(5)
    assert Coord(-1,-1) in grid.state.keys() or Coord(-1, 5) in grid.state.keys() or Coord(5,-1) in grid.state.keys() or  Coord(5, 5) in grid.state.keys()
    
def test_location_exist(): # every location is properly assigned to a coordinate within the grid
    grid = Grid(5)
    assert not grid.state[Coord(2, 2)]==None 

def test_agent_added_properly(): # whenever agent method is called agent is added properly to the grid
    grid = Grid(5)
    grid.agent('green','north')
    assert grid.agent_count==1 
   # assert grid.agent_count==2 
   
def test_agent_placed_properly(): # whenever agent is placed Is  it placed properly
    grid = Grid(5)
    agent1 = grid.agent('green','north')
    grid.replace_agent((Coord(2,1)), agent1)
    loc = grid.state[Coord(2,1)]
    assert loc.agent==agent1
   # assert loc.agent==None  # in case of not properly placed agent
 
def test_dirt_added_properly(): # whenever agent method is called agent is added properly to the grid
    grid = Grid(5)
    grid.dirt('green')
   # grid.dirt('white')     # should not be added
    assert grid.dirt_count==1 
   # assert grid.dirt_count==2      

def test_dirt_placed_properly(): # whenever agent is placed Is  it placed properly
    grid = Grid(5)
    dirt1 = grid.dirt('green')
    grid.replace_dirt((Coord(2,1)), dirt1)
    loc = grid.state[Coord(2,1)]
    assert loc.dirt==dirt1
   # assert loc.agent==None  # in case of not properly placed agent
   
def test_dirt_removed_properly():
    grid = Grid(4)
    dirt1 = grid.dirt('orange')
    grid.replace_dirt((Coord(1,1)), dirt1)
    grid.remove_dirt(Coord(1,1))
    loc = grid.state[Coord(1,1)]
    assert loc.dirt==None

def test_agent_removed_properly():
    grid = Grid(4)
    agent1 = grid.agent('orange','north')
    grid.replace_agent((Coord(1,1)), agent1)
    grid.remove_agent(Coord(1,1))
    loc = grid.state[Coord(1,1)]
    assert loc.agent==None
def test_agent_move_properly():
    grid = Grid(4)
    agent1 = grid.agent('orange','east')
    grid.replace_agent((Coord(0,0)), agent1)
    grid.move_agent((Coord(0,0)),(Coord(1,0)))
    assert grid.state[Coord(0,0)].agent==None   # location vacated
    assert grid.state[Coord(1,0)].agent!=None   # location occupied 
    
def test_agent_turn_properly():
    grid = Grid(4)
    agent1 = grid.agent('orange', 'east')
    grid.replace_agent((Coord(0,0)), agent1)
    grid.turn_agent((Coord(0,0)),'south')
    assert grid.state[Coord(0,0)].agent.orientation == Orientation.south   # orientation has changed 
   # assert grid.state[coord(0,0)].agent.orientation=='south'  # orientation is same changed     