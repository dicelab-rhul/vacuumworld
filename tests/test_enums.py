#!/usr/bin/env python3

from unittest import main, TestCase

from vacuumworld.common.colour import Colour
from vacuumworld.common.orientation import Orientation
from vacuumworld.common.direction import Direction
from vacuumworld.common.position_names import PositionNames
from vacuumworld.model.actor.user_difficulty import UserDifficulty


class TestEnums(TestCase):
    def test_colour(self) -> None:
        self.assertEqual("white", Colour.white.value)
        self.assertEqual("white", repr(Colour.white))
        self.assertEqual("white", str(Colour.white))
        self.assertEqual(Colour("white"), Colour.white)

        self.assertEqual("green", Colour.green.value)
        self.assertEqual("green", repr(Colour.green))
        self.assertEqual("green", str(Colour.green))
        self.assertEqual(Colour("green"), Colour.green)

        self.assertEqual("orange", Colour.orange.value)
        self.assertEqual("orange", repr(Colour.orange))
        self.assertEqual("orange", str(Colour.orange))
        self.assertEqual(Colour("orange"), Colour.orange)

        self.assertEqual("user", Colour.user.value)
        self.assertEqual("user", repr(Colour.user))
        self.assertEqual("user", str(Colour.user))
        self.assertEqual(Colour("user"), Colour.user)

    def test_direction(self) -> None:
        self.assertEqual("left", Direction.left.value)
        self.assertEqual("left", repr(Direction.left))
        self.assertEqual("left", str(Direction.left))
        self.assertEqual(Direction("left"), Direction.left)

        self.assertEqual("right", Direction.right.value)
        self.assertEqual("right", repr(Direction.right))
        self.assertEqual("right", str(Direction.right))
        self.assertEqual(Direction("right"), Direction.right)

    def test_orientation(self) -> None:
        self.assertEqual("north", Orientation.north.value)
        self.assertEqual("north", repr(Orientation.north))
        self.assertEqual("north", str(Orientation.north))
        self.assertEqual(Orientation("north"), Orientation.north)
        self.assertEqual(Orientation.north.get_left(), Orientation.west)
        self.assertEqual(Orientation.north.left(), Orientation.west)
        self.assertEqual(Orientation.north.get(direction=Direction.left), Orientation.west)
        self.assertEqual(Orientation.north.get_right(), Orientation.east)
        self.assertEqual(Orientation.north.right(), Orientation.east)
        self.assertEqual(Orientation.north.get(direction=Direction.right), Orientation.east)

        self.assertEqual("south", Orientation.south.value)
        self.assertEqual("south", repr(Orientation.south))
        self.assertEqual("south", str(Orientation.south))
        self.assertEqual(Orientation("south"), Orientation.south)
        self.assertEqual(Orientation.south.get_left(), Orientation.east)
        self.assertEqual(Orientation.south.left(), Orientation.east)
        self.assertEqual(Orientation.south.get(direction=Direction.left), Orientation.east)
        self.assertEqual(Orientation.south.get_right(), Orientation.west)
        self.assertEqual(Orientation.south.right(), Orientation.west)
        self.assertEqual(Orientation.south.get(direction=Direction.right), Orientation.west)

        self.assertEqual("west", Orientation.west.value)
        self.assertEqual("west", repr(Orientation.west))
        self.assertEqual("west", str(Orientation.west))
        self.assertEqual(Orientation("west"), Orientation.west)
        self.assertEqual(Orientation.west.get_left(), Orientation.south)
        self.assertEqual(Orientation.west.left(), Orientation.south)
        self.assertEqual(Orientation.west.get(direction=Direction.left), Orientation.south)
        self.assertEqual(Orientation.west.get_right(), Orientation.north)
        self.assertEqual(Orientation.west.right(), Orientation.north)
        self.assertEqual(Orientation.west.get(direction=Direction.right), Orientation.north)

        self.assertEqual("east", Orientation.east.value)
        self.assertEqual("east", repr(Orientation.east))
        self.assertEqual("east", str(Orientation.east))
        self.assertEqual(Orientation("east"), Orientation.east)
        self.assertEqual(Orientation.east.get_left(), Orientation.north)
        self.assertEqual(Orientation.east.left(), Orientation.north)
        self.assertEqual(Orientation.east.get(direction=Direction.left), Orientation.north)
        self.assertEqual(Orientation.east.get_right(), Orientation.south)
        self.assertEqual(Orientation.east.right(), Orientation.south)
        self.assertEqual(Orientation.east.get(direction=Direction.right), Orientation.south)

    def test_position_names(self) -> None:
        self.assertEqual("center", PositionNames.center.value)
        self.assertEqual("center", repr(PositionNames.center))
        self.assertEqual("center", str(PositionNames.center))
        self.assertEqual(PositionNames("center"), PositionNames.center)

        self.assertEqual("left", PositionNames.left.value)
        self.assertEqual("left", repr(PositionNames.left))
        self.assertEqual("left", str(PositionNames.left))
        self.assertEqual(PositionNames("left"), PositionNames.left)

        self.assertEqual("right", PositionNames.right.value)
        self.assertEqual("right", repr(PositionNames.right))
        self.assertEqual("right", str(PositionNames.right))
        self.assertEqual(PositionNames("right"), PositionNames.right)

        self.assertEqual("forward", PositionNames.forward.value)
        self.assertEqual("forward", repr(PositionNames.forward))
        self.assertEqual("forward", str(PositionNames.forward))
        self.assertEqual(PositionNames("forward"), PositionNames.forward)

        self.assertEqual("forwardleft", PositionNames.forwardleft.value)
        self.assertEqual("forwardleft", repr(PositionNames.forwardleft))
        self.assertEqual("forwardleft", str(PositionNames.forwardleft))
        self.assertEqual(PositionNames("forwardleft"), PositionNames.forwardleft)

        self.assertEqual("forwardright", PositionNames.forwardright.value)
        self.assertEqual("forwardright", repr(PositionNames.forwardright))
        self.assertEqual("forwardright", str(PositionNames.forwardright))
        self.assertEqual(PositionNames("forwardright"), PositionNames.forwardright)

    def test_user_difficulty(self) -> None:
        self.assertEqual(0, UserDifficulty.easy.value)
        self.assertEqual("0", repr(UserDifficulty.easy))
        self.assertEqual("0", str(UserDifficulty.easy))
        self.assertEqual(UserDifficulty(0), UserDifficulty.easy)

        self.assertEqual(1, UserDifficulty.hard.value)
        self.assertEqual("1", repr(UserDifficulty.hard))
        self.assertEqual("1", str(UserDifficulty.hard))
        self.assertEqual(UserDifficulty(1), UserDifficulty.hard)

        self.assertEqual(UserDifficulty.easy.opposite(), UserDifficulty.hard)
        self.assertEqual(UserDifficulty.hard.opposite(), UserDifficulty.easy)


if __name__ == "__main__":
    main()
