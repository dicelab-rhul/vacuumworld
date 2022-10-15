#!/usr/bin/env python3

from unittest import main, TestCase

from vacuumworld.common.coordinates import Coord
from vacuumworld.common.colour import Colour
from vacuumworld.common.orientation import Orientation
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.model.actor.vwactor_appearance import VWActorAppearance
from vacuumworld.model.dirt.dirt_appearance import VWDirtAppearance


class TestLocationAndCoordinates(TestCase):
    def test_coord(self) -> None:
        c: Coord = Coord(4, 5)  # TODO: use random coordinates.

        self.assertEqual(c.x, 4)
        self.assertEqual(c.y, 5)

        self.assertEqual(c.forward(orientation=Orientation.north), Coord(4, 4))
        self.assertEqual(c.forward(orientation=Orientation.south), Coord(4, 6))
        self.assertEqual(c.forward(orientation=Orientation.west), Coord(3, 5))
        self.assertEqual(c.forward(orientation=Orientation.east), Coord(5, 5))

        self.assertEqual(c.backward(orientation=Orientation.north), Coord(4, 6))
        self.assertEqual(c.backward(orientation=Orientation.south), Coord(4, 4))
        self.assertEqual(c.backward(orientation=Orientation.west), Coord(5, 5))
        self.assertEqual(c.backward(orientation=Orientation.east), Coord(3, 5))

        self.assertEqual(c.left(orientation=Orientation.north), Coord(3, 5))
        self.assertEqual(c.left(orientation=Orientation.south), Coord(5, 5))
        self.assertEqual(c.left(orientation=Orientation.west), Coord(4, 6))
        self.assertEqual(c.left(orientation=Orientation.east), Coord(4, 4))

        self.assertEqual(c.right(orientation=Orientation.north), Coord(5, 5))
        self.assertEqual(c.right(orientation=Orientation.south), Coord(3, 5))
        self.assertEqual(c.right(orientation=Orientation.west), Coord(4, 4))
        self.assertEqual(c.right(orientation=Orientation.east), Coord(4, 6))

        self.assertEqual(c.forwardleft(orientation=Orientation.north), Coord(3, 4))
        self.assertEqual(c.forwardleft(orientation=Orientation.south), Coord(5, 6))
        self.assertEqual(c.forwardleft(orientation=Orientation.west), Coord(3, 6))
        self.assertEqual(c.forwardleft(orientation=Orientation.east), Coord(5, 4))

        self.assertEqual(c.forwardright(orientation=Orientation.north), Coord(5, 4))
        self.assertEqual(c.forwardright(orientation=Orientation.south), Coord(3, 6))
        self.assertEqual(c.forwardright(orientation=Orientation.west), Coord(3, 4))
        self.assertEqual(c.forwardright(orientation=Orientation.east), Coord(5, 6))

    def test_location(self) -> None:
        a1: VWActorAppearance = VWActorAppearance(actor_id="foo", progressive_id="1", colour=Colour.green, orientation=Orientation.east)
        a2: VWActorAppearance = VWActorAppearance(actor_id="bar", progressive_id="2", colour=Colour.orange, orientation=Orientation.north)
        u1: VWActorAppearance = VWActorAppearance(actor_id="foobar", progressive_id="3", colour=Colour.user, orientation=Orientation.west)
        u2: VWActorAppearance = VWActorAppearance(actor_id="barfoo", progressive_id="4", colour=Colour.user, orientation=Orientation.south)
        d1: VWDirtAppearance = VWDirtAppearance(dirt_id="running", progressive_id="5", colour=Colour.green)
        d2: VWDirtAppearance = VWDirtAppearance(dirt_id="out_of", progressive_id="6", colour=Colour.orange)
        d3: VWDirtAppearance = VWDirtAppearance(dirt_id="ideas", progressive_id="7", colour=Colour.orange)
        c: Coord = Coord(4, 4)  # TODO: use random coordinates.
        f: Coord = c.forward(orientation=a1.get_orientation())
        l: Coord = c.left(orientation=a1.get_orientation())
        r: Coord = c.right(orientation=a1.get_orientation())
        fl: Coord = c.forwardleft(orientation=a1.get_orientation())
        fr: Coord = c.forwardright(orientation=a1.get_orientation())
        grid_size: int = 10  # TODO: use a random grid size.

        center: VWLocation = VWLocation(coord=c, actor_appearance=a1, dirt_appearance=None, wall=VWEnvironment.generate_wall_from_coordinates(coord=c, grid_size=grid_size))
        left: VWLocation = VWLocation(coord=l, actor_appearance=None, dirt_appearance=None, wall=VWEnvironment.generate_wall_from_coordinates(coord=l, grid_size=grid_size))
        right: VWLocation = VWLocation(coord=r, actor_appearance=a2, dirt_appearance=d1, wall=VWEnvironment.generate_wall_from_coordinates(coord=r, grid_size=grid_size))
        forward: VWLocation = VWLocation(coord=f, actor_appearance=None, dirt_appearance=d2, wall=VWEnvironment.generate_wall_from_coordinates(coord=f, grid_size=grid_size))
        forwardleft: VWLocation = VWLocation(coord=fl, actor_appearance=u1, dirt_appearance=None, wall=VWEnvironment.generate_wall_from_coordinates(coord=fl, grid_size=grid_size))
        forwardright: VWLocation = VWLocation(coord=fr, actor_appearance=u2, dirt_appearance=d3, wall=VWEnvironment.generate_wall_from_coordinates(coord=fr, grid_size=grid_size))

        self.assertEqual(center.get_coord(), c)
        self.assertEqual(center.get_actor_appearance(), a1)
        self.assertIsNone(center.get_dirt_appearance())
        self.assertEqual(center.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=c, grid_size=grid_size))

        self.assertEqual(left.get_coord(), l)
        self.assertIsNone(left.get_actor_appearance())
        self.assertIsNone(left.get_dirt_appearance())
        self.assertEqual(center.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=l, grid_size=grid_size))

        self.assertEqual(right.get_coord(), r)
        self.assertEqual(right.get_actor_appearance(), a2)
        self.assertEqual(right.get_dirt_appearance(), d1)
        self.assertEqual(center.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=r, grid_size=grid_size))

        self.assertEqual(forward.get_coord(), f)
        self.assertIsNone(forward.get_actor_appearance())
        self.assertEqual(forward.get_dirt_appearance(), d2)
        self.assertEqual(center.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=f, grid_size=grid_size))

        self.assertEqual(forwardleft.get_coord(), fl)
        self.assertEqual(forwardleft.get_actor_appearance(), u1)
        self.assertIsNone(forwardleft.get_dirt_appearance())
        self.assertEqual(center.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=fl, grid_size=grid_size))

        self.assertEqual(forwardright.get_coord(), fr)
        self.assertEqual(forwardright.get_actor_appearance(), u2)
        self.assertEqual(forwardright.get_dirt_appearance(), d3)
        self.assertEqual(center.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=fr, grid_size=grid_size))


if __name__ == "__main__":
    main()
