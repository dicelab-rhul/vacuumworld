#!/usr/bin/env python3

from unittest import main, TestCase
from random import randint

from vacuumworld.common.coordinates import Coord
from vacuumworld.common.colour import Colour
from vacuumworld.common.orientation import Orientation
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.model.actor.vwactor_appearance import VWActorAppearance
from vacuumworld.model.dirt.dirt_appearance import VWDirtAppearance
from vacuumworld.config_manager import ConfigManager

import os


class TestLocationAndCoordinates(TestCase):
    def __init__(self, args) -> None:
        super(TestLocationAndCoordinates, self).__init__(args)

        self.__config_file_name: str = "config.json"
        self.__vw_dir_name: str = "vacuumworld"
        self.__config_file_path: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), self.__vw_dir_name, self.__config_file_name)
        self.__config_manager: ConfigManager = ConfigManager(config_file_path=self.__config_file_path)
        self.__config: dict = self.__config_manager.load_config()
        self.__min_grid_size: int = self.__config["min_environment_dim"]
        self.__max_grid_size: int = self.__config["max_environment_dim"]

    def test_coord(self) -> None:
        for _ in range(100):
            c: Coord = Coord.random_between_inclusive(min_x=0, max_x=self.__max_grid_size-1, min_y=0, max_y=self.__max_grid_size-1)

            self.assertIn(c.x, range(0, self.__max_grid_size))
            self.assertIn(c.y, range(0, self.__max_grid_size))

            self.assertEqual(c.forward(orientation=Orientation.north), Coord(c.x, c.y-1))
            self.assertEqual(c.forward(orientation=Orientation.south), Coord(c.x, c.y+1))
            self.assertEqual(c.forward(orientation=Orientation.west), Coord(c.x-1, c.y))
            self.assertEqual(c.forward(orientation=Orientation.east), Coord(c.x+1, c.y))

            self.assertEqual(c.backward(orientation=Orientation.north), Coord(c.x, c.y+1))
            self.assertEqual(c.backward(orientation=Orientation.south), Coord(c.x, c.y-1))
            self.assertEqual(c.backward(orientation=Orientation.west), Coord(c.x+1, c.y))
            self.assertEqual(c.backward(orientation=Orientation.east), Coord(c.x-1, c.y))

            self.assertEqual(c.left(orientation=Orientation.north), Coord(c.x-1, c.y))
            self.assertEqual(c.left(orientation=Orientation.south), Coord(c.x+1, c.y))
            self.assertEqual(c.left(orientation=Orientation.west), Coord(c.x, c.y+1))
            self.assertEqual(c.left(orientation=Orientation.east), Coord(c.x, c.y-1))

            self.assertEqual(c.right(orientation=Orientation.north), Coord(c.x+1, c.y))
            self.assertEqual(c.right(orientation=Orientation.south), Coord(c.x-1, c.y))
            self.assertEqual(c.right(orientation=Orientation.west), Coord(c.x, c.y-1))
            self.assertEqual(c.right(orientation=Orientation.east), Coord(c.x, c.y+1))

            self.assertEqual(c.forwardleft(orientation=Orientation.north), Coord(c.x-1, c.y-1))
            self.assertEqual(c.forwardleft(orientation=Orientation.south), Coord(c.x+1, c.y+1))
            self.assertEqual(c.forwardleft(orientation=Orientation.west), Coord(c.x-1, c.y+1))
            self.assertEqual(c.forwardleft(orientation=Orientation.east), Coord(c.x+1, c.y-1))

            self.assertEqual(c.forwardright(orientation=Orientation.north), Coord(c.x+1, c.y-1))
            self.assertEqual(c.forwardright(orientation=Orientation.south), Coord(c.x-1, c.y+1))
            self.assertEqual(c.forwardright(orientation=Orientation.west), Coord(c.x-1, c.y-1))
            self.assertEqual(c.forwardright(orientation=Orientation.east), Coord(c.x+1, c.y+1))

    def test_location(self) -> None:
        for _ in range(100):
            grid_size: int = randint(self.__min_grid_size, self.__max_grid_size)

            a1: VWActorAppearance = VWActorAppearance(actor_id="foo", progressive_id="1", colour=Colour.green, orientation=Orientation.east)
            a2: VWActorAppearance = VWActorAppearance(actor_id="bar", progressive_id="2", colour=Colour.orange, orientation=Orientation.north)
            u1: VWActorAppearance = VWActorAppearance(actor_id="foobar", progressive_id="3", colour=Colour.user, orientation=Orientation.west)
            u2: VWActorAppearance = VWActorAppearance(actor_id="barfoo", progressive_id="4", colour=Colour.user, orientation=Orientation.south)
            d1: VWDirtAppearance = VWDirtAppearance(dirt_id="running", progressive_id="5", colour=Colour.green)
            d2: VWDirtAppearance = VWDirtAppearance(dirt_id="out_of", progressive_id="6", colour=Colour.orange)
            d3: VWDirtAppearance = VWDirtAppearance(dirt_id="ideas", progressive_id="7", colour=Colour.orange)

            c: Coord = Coord.random_between_inclusive(min_x=0, max_x=self.__max_grid_size-1, min_y=0, max_y=self.__max_grid_size-1)
            f: Coord = c.forward(orientation=a1.get_orientation())
            l: Coord = c.left(orientation=a1.get_orientation())
            r: Coord = c.right(orientation=a1.get_orientation())
            fl: Coord = c.forwardleft(orientation=a1.get_orientation())
            fr: Coord = c.forwardright(orientation=a1.get_orientation())

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
            self.assertEqual(left.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=l, grid_size=grid_size))

            self.assertEqual(right.get_coord(), r)
            self.assertEqual(right.get_actor_appearance(), a2)
            self.assertEqual(right.get_dirt_appearance(), d1)
            self.assertEqual(right.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=r, grid_size=grid_size))

            self.assertEqual(forward.get_coord(), f)
            self.assertIsNone(forward.get_actor_appearance())
            self.assertEqual(forward.get_dirt_appearance(), d2)
            self.assertEqual(forward.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=f, grid_size=grid_size))

            self.assertEqual(forwardleft.get_coord(), fl)
            self.assertEqual(forwardleft.get_actor_appearance(), u1)
            self.assertIsNone(forwardleft.get_dirt_appearance())
            self.assertEqual(forwardleft.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=fl, grid_size=grid_size))

            self.assertEqual(forwardright.get_coord(), fr)
            self.assertEqual(forwardright.get_actor_appearance(), u2)
            self.assertEqual(forwardright.get_dirt_appearance(), d3)
            self.assertEqual(forwardright.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=fr, grid_size=grid_size))


if __name__ == "__main__":
    main()
