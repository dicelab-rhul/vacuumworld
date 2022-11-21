#!/usr/bin/env python3

from unittest import main, TestCase
from random import randint
from typing import NamedTuple, Type

from vacuumworld import VacuumWorld
from vacuumworld.common.vwcoordinates import VWCoord
from vacuumworld.common.vwcolour import VWColour
from vacuumworld.common.vworientation import VWOrientation
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.model.actor.appearance.vwactor_appearance import VWActorAppearance
from vacuumworld.model.dirt.vwdirt_appearance import VWDirtAppearance
from vacuumworld.vwconfig_manager import VWConfigManager


class TestLocationAndCoordinates(TestCase):
    def __init__(self, args) -> None:
        super(TestLocationAndCoordinates, self).__init__(args)

        self.__config: dict = VWConfigManager.load_config_from_file(config_file_path=VacuumWorld.CONFIG_FILE_PATH)
        self.__min_grid_size: int = self.__config["min_environment_dim"]
        self.__max_grid_size: int = self.__config["max_environment_dim"]
        self.__number_of_runs: int = 100

    def test_coord(self) -> None:
        for _ in range(self.__number_of_runs):
            c: VWCoord = VWCoord.random_between_inclusive(min_x=0, max_x=self.__max_grid_size-1, min_y=0, max_y=self.__max_grid_size-1)

            self.assertIn(c.get_x(), range(0, self.__max_grid_size))
            self.assertIn(c.get_y(), range(0, self.__max_grid_size))

            self.assertIn(c.get_x(), c)
            self.assertIn(c.get_y(), c)

            self.assertEqual(c.get_x(), c[0])
            self.assertEqual(c.get_y(), c[1])

            other: VWCoord = VWCoord(x=c.get_x(), y=c.get_y())

            self.assertEqual(c, other)
            self.assertEqual(hash(c), hash(other))
            self.assertEqual(str(c), str(other))

            self.assertEqual(c.forward(orientation=VWOrientation.north), VWCoord(x=c.get_x(), y=c.get_y()-1))
            self.assertEqual(c.forward(orientation=VWOrientation.south), VWCoord(x=c.get_x(), y=c.get_y()+1))
            self.assertEqual(c.forward(orientation=VWOrientation.west), VWCoord(x=c.get_x()-1, y=c.get_y()))
            self.assertEqual(c.forward(orientation=VWOrientation.east), VWCoord(x=c.get_x()+1, y=c.get_y()))

            self.assertEqual(c.backward(orientation=VWOrientation.north), VWCoord(x=c.get_x(), y=c.get_y()+1))
            self.assertEqual(c.backward(orientation=VWOrientation.south), VWCoord(x=c.get_x(), y=c.get_y()-1))
            self.assertEqual(c.backward(orientation=VWOrientation.west), VWCoord(x=c.get_x()+1, y=c.get_y()))
            self.assertEqual(c.backward(orientation=VWOrientation.east), VWCoord(x=c.get_x()-1, y=c.get_y()))

            self.assertEqual(c.left(orientation=VWOrientation.north), VWCoord(x=c.get_x()-1, y=c.get_y()))
            self.assertEqual(c.left(orientation=VWOrientation.south), VWCoord(x=c.get_x()+1, y=c.get_y()))
            self.assertEqual(c.left(orientation=VWOrientation.west), VWCoord(x=c.get_x(), y=c.get_y()+1))
            self.assertEqual(c.left(orientation=VWOrientation.east), VWCoord(x=c.get_x(), y=c.get_y()-1))

            self.assertEqual(c.right(orientation=VWOrientation.north), VWCoord(x=c.get_x()+1, y=c.get_y()))
            self.assertEqual(c.right(orientation=VWOrientation.south), VWCoord(x=c.get_x()-1, y=c.get_y()))
            self.assertEqual(c.right(orientation=VWOrientation.west), VWCoord(x=c.get_x(), y=c.get_y()-1))
            self.assertEqual(c.right(orientation=VWOrientation.east), VWCoord(x=c.get_x(), y=c.get_y()+1))

            self.assertEqual(c.forwardleft(orientation=VWOrientation.north), VWCoord(x=c.get_x()-1, y=c.get_y()-1))
            self.assertEqual(c.forwardleft(orientation=VWOrientation.south), VWCoord(x=c.get_x()+1, y=c.get_y()+1))
            self.assertEqual(c.forwardleft(orientation=VWOrientation.west), VWCoord(x=c.get_x()-1, y=c.get_y()+1))
            self.assertEqual(c.forwardleft(orientation=VWOrientation.east), VWCoord(x=c.get_x()+1, y=c.get_y()-1))

            self.assertEqual(c.forwardright(orientation=VWOrientation.north), VWCoord(x=c.get_x()+1, y=c.get_y()-1))
            self.assertEqual(c.forwardright(orientation=VWOrientation.south), VWCoord(x=c.get_x()-1, y=c.get_y()+1))
            self.assertEqual(c.forwardright(orientation=VWOrientation.west), VWCoord(x=c.get_x()-1, y=c.get_y()-1))
            self.assertEqual(c.forwardright(orientation=VWOrientation.east), VWCoord(x=c.get_x()+1, y=c.get_y()+1))

    def test_coord_back_compatibility(self) -> None:
        '''
        This method tests that `VWCoord` works in the same way as the old `Coord` (child of `NamedTuple`) class.
        '''
        for _ in range(self.__number_of_runs):
            x, y = randint(0, self.__max_grid_size-1), randint(0, self.__max_grid_size-1)
            c: VWCoord = VWCoord(x=x, y=y)

            self.assertEqual(c.get_x(), x)
            self.assertEqual(c.get_y(), y)
            self.assertEqual(c[0], x)
            self.assertEqual(c[1], y)

            self.assertIn(x, c)
            self.assertIn(y, c)

            other: VWCoord = VWCoord(x=x, y=y)

            self.assertEqual(c, other)
            self.assertEqual(hash(c), hash(other))
            self.assertEqual(str(c), str(other))

            old_coord: Type[NamedTuple] = NamedTuple("old_coord", x=int, y=int)
            oc: old_coord = old_coord(x=x, y=y)

            self.assertEqual(c.get_x(), oc.x)
            self.assertEqual(c.get_y(), oc.y)

    def test_location(self) -> None:
        for _ in range(100):
            grid_size: int = randint(self.__min_grid_size, self.__max_grid_size)

            a1: VWActorAppearance = VWActorAppearance(actor_id="foo", progressive_id="1", colour=VWColour.green, orientation=VWOrientation.east)
            a2: VWActorAppearance = VWActorAppearance(actor_id="bar", progressive_id="2", colour=VWColour.orange, orientation=VWOrientation.north)
            u1: VWActorAppearance = VWActorAppearance(actor_id="foobar", progressive_id="3", colour=VWColour.user, orientation=VWOrientation.west)
            u2: VWActorAppearance = VWActorAppearance(actor_id="barfoo", progressive_id="4", colour=VWColour.user, orientation=VWOrientation.south)
            d1: VWDirtAppearance = VWDirtAppearance(dirt_id="running", progressive_id="5", colour=VWColour.green)
            d2: VWDirtAppearance = VWDirtAppearance(dirt_id="out_of", progressive_id="6", colour=VWColour.orange)
            d3: VWDirtAppearance = VWDirtAppearance(dirt_id="ideas", progressive_id="7", colour=VWColour.orange)

            c: VWCoord = VWCoord.random_between_inclusive(min_x=0, max_x=self.__max_grid_size-1, min_y=0, max_y=self.__max_grid_size-1)
            f: VWCoord = c.forward(orientation=a1.get_orientation())
            l: VWCoord = c.left(orientation=a1.get_orientation())
            r: VWCoord = c.right(orientation=a1.get_orientation())
            fl: VWCoord = c.forwardleft(orientation=a1.get_orientation())
            fr: VWCoord = c.forwardright(orientation=a1.get_orientation())

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
