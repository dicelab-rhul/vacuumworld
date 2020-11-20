#!/usr/bin/env python3

from vacuumworld.common.colour import Colour
from vacuumworld.common.orientation import Orientation
from vacuumworld.common.direction import Direction
from vacuumworld.common.position_names import PositionNames
from vacuumworld.model.actor.user_difficulty import UserDifficulty



def test_colour() ->  None:
    assert "white" == Colour.white.value
    assert "white" == repr(Colour.white)
    assert "white" == str(Colour.white)
    assert Colour("white") == Colour.white

    assert "green" == Colour.green.value
    assert "green" == repr(Colour.green)
    assert "green" == str(Colour.green)
    assert Colour("green") == Colour.green

    assert "orange" == Colour.orange.value
    assert "orange" == repr(Colour.orange)
    assert "orange" == str(Colour.orange)
    assert Colour("orange") == Colour.orange

    assert "user" == Colour.user.value
    assert "user" == repr(Colour.user)
    assert "user" == str(Colour.user)
    assert Colour("user") == Colour.user


def test_direction() -> None:
    assert "left" == Direction.left.value
    assert "left" == repr(Direction.left)
    assert "left" == str(Direction.left)
    assert Direction("left") == Direction.left

    assert "right" == Direction.right.value
    assert "right" == repr(Direction.right)
    assert "right" == str(Direction.right)
    assert Direction("right") == Direction.right


def test_orientation() -> None:
    assert "north" == Orientation.north.value
    assert "north" == repr(Orientation.north)
    assert "north" == str(Orientation.north)
    assert Orientation("north") == Orientation.north
    assert Orientation.north.get_left() == Orientation.west
    assert Orientation.north.left() == Orientation.west
    assert Orientation.north.get(direction=Direction.left) == Orientation.west
    assert Orientation.north.get_right() == Orientation.east
    assert Orientation.north.right() == Orientation.east
    assert Orientation.north.get(direction=Direction.right) == Orientation.east

    assert "south" == Orientation.south.value
    assert "south" == repr(Orientation.south)
    assert "south" == str(Orientation.south)
    assert Orientation("south") == Orientation.south
    assert Orientation.south.get_left() == Orientation.east
    assert Orientation.south.left() == Orientation.east
    assert Orientation.south.get(direction=Direction.left) == Orientation.east
    assert Orientation.south.get_right() == Orientation.west
    assert Orientation.south.right() == Orientation.west
    assert Orientation.south.get(direction=Direction.right) == Orientation.west

    assert "west" == Orientation.west.value
    assert "west" == repr(Orientation.west)
    assert "west" == str(Orientation.west)
    assert Orientation("west") == Orientation.west
    assert Orientation.west.get_left() == Orientation.south
    assert Orientation.west.left() == Orientation.south
    assert Orientation.west.get(direction=Direction.left) == Orientation.south
    assert Orientation.west.get_right() == Orientation.north
    assert Orientation.west.right() == Orientation.north
    assert Orientation.west.get(direction=Direction.right) == Orientation.north

    assert "east" == Orientation.east.value
    assert "east" == repr(Orientation.east)
    assert "east" == str(Orientation.east)
    assert Orientation("east") == Orientation.east
    assert Orientation.east.get_left() == Orientation.north
    assert Orientation.east.left() == Orientation.north
    assert Orientation.east.get(direction=Direction.left) == Orientation.north
    assert Orientation.east.get_right() == Orientation.south
    assert Orientation.east.right() == Orientation.south
    assert Orientation.east.get(direction=Direction.right) == Orientation.south

def test_position_names() -> None:
    assert "center" == PositionNames.center.value
    assert "center" == repr(PositionNames.center)
    assert "center" == str(PositionNames.center)
    assert PositionNames("center") == PositionNames.center

    assert "left" == PositionNames.left.value
    assert "left" == repr(PositionNames.left)
    assert "left" == str(PositionNames.left)
    assert PositionNames("left") == PositionNames.left

    assert "right" == PositionNames.right.value
    assert "right" == repr(PositionNames.right)
    assert "right" == str(PositionNames.right)
    assert PositionNames("right") == PositionNames.right

    assert "forward" == PositionNames.forward.value
    assert "forward" == repr(PositionNames.forward)
    assert "forward" == str(PositionNames.forward)
    assert PositionNames("forward") == PositionNames.forward

    assert "forwardleft" == PositionNames.forwardleft.value
    assert "forwardleft" == repr(PositionNames.forwardleft)
    assert "forwardleft" == str(PositionNames.forwardleft)
    assert PositionNames("forwardleft") == PositionNames.forwardleft

    assert "forwardright" == PositionNames.forwardright.value
    assert "forwardright" == repr(PositionNames.forwardright)
    assert "forwardright" == str(PositionNames.forwardright)
    assert PositionNames("forwardright") == PositionNames.forwardright


def test_user_difficulty() -> None:
    assert 0 == UserDifficulty.easy.value
    assert "0" == repr(UserDifficulty.easy)
    assert "0" == str(UserDifficulty.easy)
    assert UserDifficulty(0) == UserDifficulty.easy

    assert 1 == UserDifficulty.hard.value
    assert "1" == repr(UserDifficulty.hard)
    assert "1" == str(UserDifficulty.hard)
    assert UserDifficulty(1) == UserDifficulty.hard

    assert UserDifficulty.easy.toggle() == UserDifficulty.hard
    assert UserDifficulty.hard.toggle() == UserDifficulty.easy


def test_all() -> None:
    test_colour()
    test_direction()
    test_orientation()
    test_position_names()
    test_user_difficulty()


if __name__ == "__main__":
    test_all()
