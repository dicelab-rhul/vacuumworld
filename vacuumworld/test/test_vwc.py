from vacuumworld.vwc import coord, agent, dirt, direction
from vacuumworld.vwc import observation, colour, orientation
from vacuumworld.vwc import location

import traceback

def test_coord():
    c1, c2 = coord(1,2), coord(2,3)
    assert c1[0] == 1
    assert c1[1] == 2

    assert c1 + c2 == coord(3,5)
    assert c1 - c2 == coord(-1,-1)
    assert c1 * c2 == coord(2, 6)
    assert coord(5,3) // coord(1, 2) == coord(5,1)
    assert coord(4,4) / coord(1, 2) == coord(4,2)

    assert c1 + 2 == coord(3,4)
    assert c1 - 1 == coord(0,1)
    assert c1 / 2 == coord(0,1)
    assert c2 // 2 == coord(1,1)
    assert c1 * 2 == coord(2,4)

def test_agent():
    a1 = agent('a1', colour.orange, orientation.north)
    a1.name
    a1.colour
    a1.orientation

def test_dirt():
    d1 = dirt('d1', colour.white)
    d1.name
    d1.colour

def test_location():
    l1 = location(coord(0,0), agent(None,None,None), dirt(1,1))
    
def test_observation():
    o1 = observation(None,1,None,3,4,5) #type checks? NamedTuple is a pain...
    assert [i for i in o1] == [1,3,4,5]

def test_direction():
    assert direction.left(orientation.north) == orientation.west
    assert direction.left(orientation.west) == orientation.south
    assert direction.left(orientation.south) == orientation.east
    assert direction.left(orientation.east) == orientation.north

    assert direction.right(orientation.north) == orientation.east
    assert direction.right(orientation.west) == orientation.north
    assert direction.right(orientation.south) == orientation.west
    assert direction.right(orientation.east) == orientation.south

   
def test(t):
    try:
        t()
        print("TEST PASSED: ", t.__name__)
    except Exception as e:
        print("TEST FAILED: ", t.__name__)
        traceback.print_exc()
    
    
test(test_coord)
test(test_agent)
test(test_dirt)
test(test_location)
test(test_observation)
test(test_direction)