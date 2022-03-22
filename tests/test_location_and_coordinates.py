#!/usr/bin/env python3

from typing import Dict
from vacuumworld.common.coordinates import Coord
from vacuumworld.common.colour import Colour
from vacuumworld.common.orientation import Orientation
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.model.actor.vwactor_appearance import VWActorAppearance
from vacuumworld.model.dirt.dirt_appearance import VWDirtAppearance



def test_coord() -> None:
    c: Coord = Coord(4, 5)

    assert c.x == 4 and c.y == 5

    assert c.forward(orientation=Orientation.north) == Coord(4, 4)
    assert c.forward(orientation=Orientation.south) == Coord(4, 6)
    assert c.forward(orientation=Orientation.west) == Coord(3, 5)
    assert c.forward(orientation=Orientation.east) == Coord(5, 5)

    assert c.backward(orientation=Orientation.north) == Coord(4, 6)
    assert c.backward(orientation=Orientation.south) == Coord(4, 4)
    assert c.backward(orientation=Orientation.west) == Coord(5, 5)
    assert c.backward(orientation=Orientation.east) == Coord(3, 5)

    assert c.left(orientation=Orientation.north) == Coord(3, 5)
    assert c.left(orientation=Orientation.south) == Coord(5, 5)
    assert c.left(orientation=Orientation.west) == Coord(4, 6)
    assert c.left(orientation=Orientation.east) == Coord(4, 4)

    assert c.right(orientation=Orientation.north) == Coord(5, 5)
    assert c.right(orientation=Orientation.south) == Coord(3, 5)
    assert c.right(orientation=Orientation.west) == Coord(4, 4)
    assert c.right(orientation=Orientation.east) == Coord(4, 6)

    assert c.forwardleft(orientation=Orientation.north) == Coord(3, 4)
    assert c.forwardleft(orientation=Orientation.south) == Coord(5, 6)
    assert c.forwardleft(orientation=Orientation.west) == Coord(3, 6)
    assert c.forwardleft(orientation=Orientation.east) == Coord(5, 4)

    assert c.forwardright(orientation=Orientation.north) == Coord(5, 4)
    assert c.forwardright(orientation=Orientation.south) == Coord(3, 6)
    assert c.forwardright(orientation=Orientation.west) == Coord(3, 4)
    assert c.forwardright(orientation=Orientation.east) == Coord(5, 6)


def test_location() -> None:
    a1: VWActorAppearance = VWActorAppearance(actor_id="foo", progressive_id="1", colour=Colour.green, orientation=Orientation.east)
    a2: VWActorAppearance = VWActorAppearance(actor_id="bar", progressive_id="2", colour=Colour.orange, orientation=Orientation.north)
    u1: VWActorAppearance = VWActorAppearance(actor_id="foobar", progressive_id="3", colour=Colour.user, orientation=Orientation.west)
    u2: VWActorAppearance = VWActorAppearance(actor_id="barfoo", progressive_id="4", colour=Colour.user, orientation=Orientation.south)
    d1: VWDirtAppearance = VWDirtAppearance(dirt_id="running", progressive_id="5", colour=Colour.green)
    d2: VWDirtAppearance = VWDirtAppearance(dirt_id="out_of", progressive_id="6", colour=Colour.orange)
    d3: VWDirtAppearance = VWDirtAppearance(dirt_id="ideas", progressive_id="7", colour=Colour.orange)
    c: Coord = Coord(4,4)
    f: Coord = c.forward(orientation=a1.get_orientation())
    l: Coord = c.left(orientation=a1.get_orientation())
    r: Coord = c.right(orientation=a1.get_orientation())
    fl: Coord = c.forwardleft(orientation=a1.get_orientation())
    fr: Coord = c.forwardright(orientation=a1.get_orientation())
    
    # TODO: use non-trivial walls.
    sample_wall: Dict[Orientation, bool] = {Orientation.north: False, Orientation.south: False, Orientation.west: False, Orientation.east: False}

    # TODO: customise the wall depending on the coordinates.
    center: VWLocation = VWLocation(coord=c, actor_appearance=a1, dirt_appearance=None, wall=sample_wall)
    left: VWLocation = VWLocation(coord=l, actor_appearance=None, dirt_appearance=None, wall=sample_wall)
    right: VWLocation = VWLocation(coord=r, actor_appearance=a2, dirt_appearance=d1, wall=sample_wall)
    forward: VWLocation = VWLocation(coord=f, actor_appearance=None, dirt_appearance=d2, wall=sample_wall)
    forwardleft: VWLocation = VWLocation(coord=fl, actor_appearance=u1, dirt_appearance=None, wall=sample_wall)
    forwardright: VWLocation = VWLocation(coord=fr, actor_appearance=u2, dirt_appearance=d3, wall=sample_wall)

    assert center.get_coord() == c
    assert center.get_actor_appearance() == a1
    assert center.get_dirt_appearance() == None

    assert left.get_coord() == l
    assert left.get_actor_appearance() == None
    assert left.get_dirt_appearance() == None

    assert right.get_coord() == r
    assert right.get_actor_appearance() == a2
    assert right.get_dirt_appearance() == d1

    assert forward.get_coord() == f
    assert forward.get_actor_appearance() == None
    assert forward.get_dirt_appearance() == d2

    assert forwardleft.get_coord() == fl
    assert forwardleft.get_actor_appearance() == u1
    assert forwardleft.get_dirt_appearance() == None

    assert forwardright.get_coord() == fr
    assert forwardright.get_actor_appearance() == u2
    assert forwardright.get_dirt_appearance() == d3
    
    # TODO: check for walls.


def test_all() -> None:
    test_coord()
    test_location()


if __name__ == "__main__":
    test_all()
