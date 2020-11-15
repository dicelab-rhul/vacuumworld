from vacuumworld.core.environment.location_interface import Location
from vacuumworld.core.dirt.dirt_interface import DirtInterface
from vacuumworld.core.agent.agent_interface import Actor

from vacuumworld.core.common.coordinates import Coord
from vacuumworld.core.common.orientation import Orientation
from vacuumworld.core.environment.vw import Grid

import sys
import os



myPath: str = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(myPath))


def test_wall_locations_exist() -> None:
    grid: Grid = Grid(5)
    assert Coord(-1,-1) in grid.state.keys() and Coord(-1, 5) in grid.state.keys() and Coord(5,-1) in grid.state.keys() and Coord(5, 5) in grid.state.keys()


def test_location_exist() -> None: # every location is properly assigned to a coordinate within the grid
    grid: Grid = Grid(5)
    assert grid.state[Coord(2, 2)] is not None 


def test_agent_added_properly() -> None: # whenever agent method is called agent is added properly to the grid
    grid: Grid = Grid(5)
    grid.agent('green','north')
    assert grid.agent_count == 1


def test_agent_placed_properly() -> None: # whenever agent is placed Is  it placed properly
    grid: Grid = Grid(5)
    agent1: Actor = grid.agent('green','north')
    grid.replace_agent((Coord(2,1)), agent1)
    loc = grid.state[Coord(2,1)]
    assert loc.agent == agent1


def test_dirt_added_properly() -> None: # whenever agent method is called agent is added properly to the grid
    grid: Grid = Grid(5)
    grid.dirt('green')
    assert grid.dirt_count == 1 
     

def test_dirt_placed_properly() -> None: # whenever agent is placed Is  it placed properly
    grid: Grid = Grid(5)
    dirt1: DirtInterface = grid.dirt('green')
    grid.replace_dirt((Coord(2,1)), dirt1)
    loc: Location = grid.state[Coord(2,1)]
    assert loc.dirt == dirt1


def test_dirt_removed_properly() -> None:
    grid: Grid = Grid(4)
    dirt1: DirtInterface = grid.dirt('orange')
    grid.replace_dirt((Coord(1,1)), dirt1)
    grid.remove_dirt(Coord(1,1))
    loc: Location = grid.state[Coord(1,1)]
    assert loc.dirt is None


def test_agent_removed_properly() -> None:
    grid: Grid = Grid(4)
    agent1: Actor = grid.agent('orange','north')
    grid.replace_agent((Coord(1,1)), agent1)
    grid.remove_agent(Coord(1,1))
    loc = grid.state[Coord(1,1)]
    assert loc.agent is None


def test_agent_move_properly() -> None:
    grid: Grid = Grid(4)
    agent1: Actor = grid.agent('orange','east')
    grid.replace_agent((Coord(0,0)), agent1)
    grid.move_agent((Coord(0,0)),(Coord(1,0)))
    assert grid.state[Coord(0,0)].agent==None   # location vacated
    assert grid.state[Coord(1,0)].agent!=None   # location occupied 


def test_agent_turn_properly() -> None:
    grid: Grid = Grid(4)
    agent1: Actor = grid.agent('orange', 'east')
    grid.replace_agent((Coord(0,0)), agent1)
    grid.turn_agent((Coord(0,0)),'south')
    assert grid.state[Coord(0,0)].agent.orientation == Orientation.south   # orientation has changed 
