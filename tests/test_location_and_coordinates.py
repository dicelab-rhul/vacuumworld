#!/usr/bin/env python3

from unittest import main, TestCase
from random import randint
from typing import NamedTuple, Type, Any
from pyoptional.pyoptional import PyOptional

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
    '''
    This class tests the `VWCoord` and `VWLocation` classes.
    '''
    def __init__(self, args: Any) -> None:
        super(TestLocationAndCoordinates, self).__init__(args)

        self.__config: dict[str, Any] = VWConfigManager.load_config_from_file(config_file_path=VacuumWorld.CONFIG_FILE_PATH)
        self.__min_grid_size: int = self.__config["min_environment_dim"]
        self.__max_grid_size: int = self.__config["max_environment_dim"]
        self.__number_of_runs: int = 100

    def test_coord(self) -> None:
        '''
        Tests the creation of `VWCoord` objects.
        '''
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
        Tests that `VWCoord` works in the same way as the old `Coord` (child of `NamedTuple`) class.
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
            oc = old_coord(x=x, y=y)

            self.assertEqual(c.get_x(), oc.x)
            self.assertEqual(c.get_y(), oc.y)

    def test_location(self) -> None:
        '''
        Tests the creation of `VWLocation` objects.
        '''
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

            center: VWLocation = VWLocation(coord=c, actor_appearance=PyOptional.of(a1), wall=VWEnvironment.generate_wall_from_coordinates(coord=c, grid_size=grid_size))
            left: VWLocation = VWLocation(coord=l, wall=VWEnvironment.generate_wall_from_coordinates(coord=l, grid_size=grid_size))
            right: VWLocation = VWLocation(coord=r, actor_appearance=PyOptional.of(a2), dirt_appearance=PyOptional.of(d1), wall=VWEnvironment.generate_wall_from_coordinates(coord=r, grid_size=grid_size))
            forward: VWLocation = VWLocation(coord=f, dirt_appearance=PyOptional.of(d2), wall=VWEnvironment.generate_wall_from_coordinates(coord=f, grid_size=grid_size))
            forwardleft: VWLocation = VWLocation(coord=fl, actor_appearance=PyOptional.of(u1), wall=VWEnvironment.generate_wall_from_coordinates(coord=fl, grid_size=grid_size))
            forwardright: VWLocation = VWLocation(coord=fr, actor_appearance=PyOptional.of(u2), dirt_appearance=PyOptional.of(d3), wall=VWEnvironment.generate_wall_from_coordinates(coord=fr, grid_size=grid_size))

            self.assertEqual(center.get_coord(), c)
            self.assertEqual(center.get_actor_appearance().or_else_raise(), a1)
            self.assertTrue(center.get_dirt_appearance().is_empty())
            self.assertEqual(center.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=c, grid_size=grid_size))

            self.assertEqual(left.get_coord(), l)
            self.assertTrue(left.get_actor_appearance().is_empty())
            self.assertTrue(left.get_dirt_appearance().is_empty())
            self.assertEqual(left.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=l, grid_size=grid_size))

            self.assertEqual(right.get_coord(), r)
            self.assertEqual(right.get_actor_appearance().or_else_raise(), a2)
            self.assertEqual(right.get_dirt_appearance().or_else_raise(), d1)
            self.assertEqual(right.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=r, grid_size=grid_size))

            self.assertEqual(forward.get_coord(), f)
            self.assertTrue(forward.get_actor_appearance().is_empty())
            self.assertEqual(forward.get_dirt_appearance().or_else_raise(), d2)
            self.assertEqual(forward.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=f, grid_size=grid_size))

            self.assertEqual(forwardleft.get_coord(), fl)
            self.assertEqual(forwardleft.get_actor_appearance().or_else_raise(), u1)
            self.assertTrue(forwardleft.get_dirt_appearance().is_empty())
            self.assertEqual(forwardleft.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=fl, grid_size=grid_size))

            self.assertEqual(forwardright.get_coord(), fr)
            self.assertEqual(forwardright.get_actor_appearance().or_else_raise(), u2)
            self.assertEqual(forwardright.get_dirt_appearance().or_else_raise(), d3)
            self.assertEqual(forwardright.get_wall_info(), VWEnvironment.generate_wall_from_coordinates(coord=fr, grid_size=grid_size))


if __name__ == "__main__":
    main()
