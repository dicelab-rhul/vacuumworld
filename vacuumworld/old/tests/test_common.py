from vacuumworld.core.common.coordinates import Coord
from vacuumworld.core.common.direction import Direction
from vacuumworld.core.common.orientation import Orientation
from vacuumworld.core.common.colour import Colour
from vacuumworld.core.common.observation import Observation
from vacuumworld.core.environment.location_interface import Location
from vacuumworld.core.agent.agent_interface import Actor
from vacuumworld.core.dirt.dirt_interface import DirtInterface


import traceback



def test_coord() -> None:
    c1: Coord = Coord(1,2)
    c2: Coord = Coord(2,3)

    assert c1[0] == 1
    assert c1[1] == 2

    assert c1 + c2 == Coord(3,5)
    assert c1 - c2 == Coord(-1,-1)
    assert c1 * c2 == Coord(2, 6)
    assert Coord(5,3) // Coord(1, 2) == Coord(5,1)
    assert Coord(4,4) / Coord(1, 2) == Coord(4,2)

    assert c1 + 2 == Coord(3,4)
    assert c1 - 1 == Coord(0,1)
    assert c1 / 2 == Coord(0,1)
    assert c2 // 2 == Coord(1,1)
    assert c1 * 2 == Coord(2,4)


def test_agent() -> None:
    a1: Actor = Actor('a1', Colour.orange, Orientation.north)
    a1.name
    a1.colour
    a1.orientation


def test_dirt() -> None:
    d1: DirtInterface = DirtInterface('d1', Colour.white)
    d1.name
    d1.colour


def test_location() -> None:
    assert Location(Coord(0,0), Actor(None,None,None), DirtInterface(1,1)) is not None


def test_observation() -> None:
    o1: Observation = Observation(None,1,None,3,4,5) #type checks? NamedTuple is a pain...
    assert [i for i in o1] == [1,3,4,5]


def test_direction() -> None:
    assert Direction.left(Orientation.north) == Orientation.west
    assert Direction.left(Orientation.west) == Orientation.south
    assert Direction.left(Orientation.south) == Orientation.east
    assert Direction.left(Orientation.east) == Orientation.north

    assert Direction.right(Orientation.north) == Orientation.east
    assert Direction.right(Orientation.west) == Orientation.north
    assert Direction.right(Orientation.south) == Orientation.west
    assert Direction.right(Orientation.east) == Orientation.south

   
def test(t)  -> None:
    try:
        t()
        print("TEST PASSED: ", t.__name__)
    except Exception:
        print("TEST FAILED: ", t.__name__)
        traceback.print_exc()
    
    
test(test_coord)
test(test_agent)
test(test_dirt)
test(test_location)
test(test_observation)
test(test_direction)
