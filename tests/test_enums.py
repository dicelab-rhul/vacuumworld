#!/usr/bin/env python3

from unittest import main, TestCase

from vacuumworld.common.vwcolour import VWColour
from vacuumworld.common.vworientation import VWOrientation
from vacuumworld.common.vwdirection import VWDirection
from vacuumworld.common.vwposition_names import VWPositionNames
from vacuumworld.common.vwuser_difficulty import VWUserDifficulty


class TestEnums(TestCase):
    '''
    This class tests the enums in the `vacuumworld.common` package: `VWColour`, `VWDirection`, `VWOrientation`, `VWPositionNames`, and `VWUserDifficulty`.
    '''
    def test_colour(self) -> None:
        '''
        Tests the `VWColour` enum.
        '''
        self.assertEqual("white", VWColour.white.value)
        self.assertEqual("white", repr(VWColour.white))
        self.assertEqual("white", str(VWColour.white))
        self.assertEqual(VWColour("white"), VWColour.white)

        self.assertEqual("green", VWColour.green.value)
        self.assertEqual("green", repr(VWColour.green))
        self.assertEqual("green", str(VWColour.green))
        self.assertEqual(VWColour("green"), VWColour.green)

        self.assertEqual("orange", VWColour.orange.value)
        self.assertEqual("orange", repr(VWColour.orange))
        self.assertEqual("orange", str(VWColour.orange))
        self.assertEqual(VWColour("orange"), VWColour.orange)

        self.assertEqual("user", VWColour.user.value)
        self.assertEqual("user", repr(VWColour.user))
        self.assertEqual("user", str(VWColour.user))
        self.assertEqual(VWColour("user"), VWColour.user)

    def test_direction(self) -> None:
        '''
        Tests the `VWDirection` enum.
        '''
        self.assertEqual("left", VWDirection.left.value)
        self.assertEqual("left", repr(VWDirection.left))
        self.assertEqual("left", str(VWDirection.left))
        self.assertEqual(VWDirection("left"), VWDirection.left)

        self.assertEqual("right", VWDirection.right.value)
        self.assertEqual("right", repr(VWDirection.right))
        self.assertEqual("right", str(VWDirection.right))
        self.assertEqual(VWDirection("right"), VWDirection.right)

    def test_orientation(self) -> None:
        '''
        Tests the `VWOrientation` enum.
        '''
        self.assertEqual("north", VWOrientation.north.value)
        self.assertEqual("north", repr(VWOrientation.north))
        self.assertEqual("north", str(VWOrientation.north))
        self.assertEqual(VWOrientation("north"), VWOrientation.north)
        self.assertEqual(VWOrientation.north.get_left(), VWOrientation.west)
        self.assertEqual(VWOrientation.north.get(direction=VWDirection.left), VWOrientation.west)
        self.assertEqual(VWOrientation.north.get_right(), VWOrientation.east)
        self.assertEqual(VWOrientation.north.get(direction=VWDirection.right), VWOrientation.east)
        self.assertEqual(VWOrientation.north.get_opposite(), VWOrientation.south)

        self.assertEqual("south", VWOrientation.south.value)
        self.assertEqual("south", repr(VWOrientation.south))
        self.assertEqual("south", str(VWOrientation.south))
        self.assertEqual(VWOrientation("south"), VWOrientation.south)
        self.assertEqual(VWOrientation.south.get_left(), VWOrientation.east)
        self.assertEqual(VWOrientation.south.get(direction=VWDirection.left), VWOrientation.east)
        self.assertEqual(VWOrientation.south.get_right(), VWOrientation.west)
        self.assertEqual(VWOrientation.south.get(direction=VWDirection.right), VWOrientation.west)
        self.assertEqual(VWOrientation.south.get_opposite(), VWOrientation.north)

        self.assertEqual("west", VWOrientation.west.value)
        self.assertEqual("west", repr(VWOrientation.west))
        self.assertEqual("west", str(VWOrientation.west))
        self.assertEqual(VWOrientation("west"), VWOrientation.west)
        self.assertEqual(VWOrientation.west.get_left(), VWOrientation.south)
        self.assertEqual(VWOrientation.west.get(direction=VWDirection.left), VWOrientation.south)
        self.assertEqual(VWOrientation.west.get_right(), VWOrientation.north)
        self.assertEqual(VWOrientation.west.get(direction=VWDirection.right), VWOrientation.north)
        self.assertEqual(VWOrientation.west.get_opposite(), VWOrientation.east)

        self.assertEqual("east", VWOrientation.east.value)
        self.assertEqual("east", repr(VWOrientation.east))
        self.assertEqual("east", str(VWOrientation.east))
        self.assertEqual(VWOrientation("east"), VWOrientation.east)
        self.assertEqual(VWOrientation.east.get_left(), VWOrientation.north)
        self.assertEqual(VWOrientation.east.get(direction=VWDirection.left), VWOrientation.north)
        self.assertEqual(VWOrientation.east.get_right(), VWOrientation.south)
        self.assertEqual(VWOrientation.east.get(direction=VWDirection.right), VWOrientation.south)
        self.assertEqual(VWOrientation.east.get_opposite(), VWOrientation.west)

    def test_position_names(self) -> None:
        '''
        Tests the `VWPositionNames` enum.
        '''
        self.assertEqual("center", VWPositionNames.center.value)
        self.assertEqual("center", repr(VWPositionNames.center))
        self.assertEqual("center", str(VWPositionNames.center))
        self.assertEqual(VWPositionNames("center"), VWPositionNames.center)

        self.assertEqual("left", VWPositionNames.left.value)
        self.assertEqual("left", repr(VWPositionNames.left))
        self.assertEqual("left", str(VWPositionNames.left))
        self.assertEqual(VWPositionNames("left"), VWPositionNames.left)

        self.assertEqual("right", VWPositionNames.right.value)
        self.assertEqual("right", repr(VWPositionNames.right))
        self.assertEqual("right", str(VWPositionNames.right))
        self.assertEqual(VWPositionNames("right"), VWPositionNames.right)

        self.assertEqual("forward", VWPositionNames.forward.value)
        self.assertEqual("forward", repr(VWPositionNames.forward))
        self.assertEqual("forward", str(VWPositionNames.forward))
        self.assertEqual(VWPositionNames("forward"), VWPositionNames.forward)

        self.assertEqual("forwardleft", VWPositionNames.forwardleft.value)
        self.assertEqual("forwardleft", repr(VWPositionNames.forwardleft))
        self.assertEqual("forwardleft", str(VWPositionNames.forwardleft))
        self.assertEqual(VWPositionNames("forwardleft"), VWPositionNames.forwardleft)

        self.assertEqual("forwardright", VWPositionNames.forwardright.value)
        self.assertEqual("forwardright", repr(VWPositionNames.forwardright))
        self.assertEqual("forwardright", str(VWPositionNames.forwardright))
        self.assertEqual(VWPositionNames("forwardright"), VWPositionNames.forwardright)

    def test_user_difficulty(self) -> None:
        '''
        Tests the `VWUserDifficulty` enum.
        '''
        self.assertEqual(0, VWUserDifficulty.easy.value)
        self.assertEqual("0", repr(VWUserDifficulty.easy))
        self.assertEqual("0", str(VWUserDifficulty.easy))
        self.assertEqual(VWUserDifficulty(0), VWUserDifficulty.easy)

        self.assertEqual(1, VWUserDifficulty.hard.value)
        self.assertEqual("1", repr(VWUserDifficulty.hard))
        self.assertEqual("1", str(VWUserDifficulty.hard))
        self.assertEqual(VWUserDifficulty(1), VWUserDifficulty.hard)

        self.assertEqual(VWUserDifficulty.easy.opposite(), VWUserDifficulty.hard)
        self.assertEqual(VWUserDifficulty.hard.opposite(), VWUserDifficulty.easy)


if __name__ == "__main__":
    main()
