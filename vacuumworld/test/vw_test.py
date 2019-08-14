# -*- coding: utf-8 -*-
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


from ..vw import Grid
from ..vwc import coord


def test_wall_locations_exist():
    grid = Grid(5)
    assert coord(-1,-1) in grid.state.keys() or coord(-1, 5) in grid.state.keys() or coord(5,-1) in grid.state.keys() or  coord(5, 5) in grid.state.keys()
    
def test_location_exist(): # every location is properly assigned to a coordinate within the grid
    grid = Grid(5)
    assert not grid.state[coord(2, 2)]==None 

def test_agent_added_properly(): # whenever agent method is called agent is added properly to the grid
    grid = Grid(5)
    grid.agent('green','north')
    assert grid.agent_count==1 
   # assert grid.agent_count==2 
def test_agentPlacedProperly(): # whenever agent is placed Is  it placed properly
    grid = Grid(5)
    agent1 = grid.agent('green','north')
    grid.replace_agent((coord(2,1)), agent1)
    loc = grid.state[coord(2,1)]
    assert loc.agent==agent1
   # assert loc.agent==None  # in case of not properly placed agent
 
def test_dirtaddedProperly(): # whenever agent method is called agent is added properly to the grid
    grid = Grid(5)
    grid.dirt('green')
   # grid.dirt('white')     # should not be added
    assert grid.dirt_count==1 
   # assert grid.dirt_count==2      

def test_dirtPlacedProperly(): # whenever agent is placed Is  it placed properly
    grid = Grid(5)
    dirt1 = grid.dirt('green')
    grid.replace_dirt((coord(2,1)), dirt1)
    loc = grid.state[coord(2,1)]
    assert loc.dirt==dirt1
   # assert loc.agent==None  # in case of not properly placed agent
   
def test_dirtRemovedProperly():
    grid = Grid(4)
    dirt1 = grid.dirt('orange')
    grid.replace_dirt((coord(1,1)), dirt1)
    grid.remove_dirt(coord(1,1))
    loc = grid.state[coord(1,1)]
    assert loc.dirt==None

def test_agentRemovedProperly():
    grid = Grid(4)
    agent1 = grid.agent('orange','north')
    grid.replace_agent((coord(1,1)), agent1)
    grid.remove_agent(coord(1,1))
    loc = grid.state[coord(1,1)]
    assert loc.agent==None
def test_agentMoveProperly():
    grid = Grid(4)
    agent1 = grid.agent('orange','east')
    grid.replace_agent((coord(0,0)), agent1)
    grid.move_agent((coord(0,0)),(coord(1,0)))
    assert grid.state[coord(0,0)].agent==None   # location vacated
    assert grid.state[coord(1,0)].agent!=None   # location occupied 
    
def test_agentTurnProperly():
    grid = Grid(4)
    agent1 = grid.agent('orange','east')
    grid.replace_agent((coord(0,0)), agent1)
    grid.turn_agent((coord(0,0)),'south')
    assert grid.state[coord(0,0)].agent.orientation=='south'   # orientation has changed 
   # assert grid.state[coord(0,0)].agent.orientation=='south'  # orientation is same changed     
        
           
        