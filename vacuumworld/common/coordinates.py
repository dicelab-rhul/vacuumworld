from __future__ import annotations
from typing import Dict, NamedTuple, List, Union, Tuple, cast
from random import randint

from .orientation import Orientation


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Union[int, List[int], Tuple[int, int]]) -> Coord:
        assert other is not None

        if isinstance(other, int):
            return Coord(self[0] + other, self[1] + other)
        else:
            assert type(other) in [list, tuple] and len(other) == 2
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return Coord(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other: Union[int, List[int], Tuple[int, int]]) -> Coord:
        assert other is not None

        if isinstance(other, int):
            return Coord(self[0] - other, self[1] - other)
        else:
            assert type(other) in [list, tuple] and len(other) == 2
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return Coord(self[0] - other[0], self[1] - other[1])

    def __mul__(self, other: Union[int, List[int], Tuple[int, int]]) -> Coord:
        assert other is not None

        if isinstance(other, int):
            return Coord(self[0] * other, self[1] * other)
        else:
            assert type(other) in [list, tuple] and len(other) == 2
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return Coord(self[0] * other[0], self[1] * other[1])

    # Integer division.
    def __floordiv__(self, other: Union[int, List[int], Tuple[int, int]]) -> Coord:
        assert other is not None

        if isinstance(other, int):
            return Coord(self[0] // other, self[1] // other)
        else:
            assert type(other) in [list, tuple] and len(other) == 2
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return Coord(self[0] // other[0], self[1] // other[1])

    # We force `/` to work like `//`.
    def __truediv__(self, other: Union[int, List[int], Tuple[int, int]]) -> Coord:
        assert other is not None

        if isinstance(other, int):
            return self // other
        else:
            assert type(other) in [list, tuple] and len(other) == 2
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return self // (int(other[0]), int(other[1]))

    def __str__(self) -> str:
        return "({}, {})".format(self.x, self.y)

    def forward(self, orientation: Orientation) -> Coord:
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.x, y=self.y - 1)
        elif orientation == Orientation.south:
            return Coord(x=self.x, y=self.y + 1)
        elif orientation == Orientation.west:
            return Coord(x=self.x - 1, y=self.y)
        else:
            return Coord(x=self.x + 1, y=self.y)

    def backward(self, orientation: Orientation) -> Coord:
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.x, y=self.y + 1)
        elif orientation == Orientation.south:
            return Coord(x=self.x, y=self.y - 1)
        elif orientation == Orientation.west:
            return Coord(x=self.x + 1, y=self.y)
        else:
            return Coord(x=self.x - 1, y=self.y)

    def left(self, orientation: Orientation) -> Coord:
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.x - 1, y=self.y)
        elif orientation == Orientation.south:
            return Coord(x=self.x + 1, y=self.y)
        elif orientation == Orientation.west:
            return Coord(x=self.x, y=self.y + 1)
        else:
            return Coord(x=self.x, y=self.y - 1)

    def right(self, orientation: Orientation) -> Coord:
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.x + 1, y=self.y)
        elif orientation == Orientation.south:
            return Coord(x=self.x - 1, y=self.y)
        elif orientation == Orientation.west:
            return Coord(x=self.x, y=self.y - 1)
        else:
            return Coord(x=self.x, y=self.y + 1)

    def forwardleft(self, orientation: Orientation) -> Coord:
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.x - 1, y=self.y - 1)
        elif orientation == Orientation.south:
            return Coord(x=self.x + 1, y=self.y + 1)
        elif orientation == Orientation.west:
            return Coord(x=self.x - 1, y=self.y + 1)
        else:
            return Coord(x=self.x + 1, y=self.y - 1)

    def forwardright(self, orientation: Orientation) -> Coord:
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.x + 1, y=self.y - 1)
        elif orientation == Orientation.south:
            return Coord(x=self.x - 1, y=self.y + 1)
        elif orientation == Orientation.west:
            return Coord(x=self.x - 1, y=self.y - 1)
        else:
            return Coord(x=self.x + 1, y=self.y + 1)

    def clone(self) -> Coord:
        return Coord(x=self.x, y=self.y)

    def to_json(self) -> Dict[str, int]:
        return {
            "x": self.x,
            "y": self.y
        }

    def __eq__(self, o: object) -> bool:
        if not o or type(o) != Coord:
            return False
        else:
            o = cast(typ=Coord, val=o)

            return self.x == o.x and self.y == o.y

    def __hash__(self) -> int:
        prime: int = 31
        result: int = 1
        result = prime * result + self.x
        result = prime * result + self.y

        return result

    @staticmethod
    def random_between_inclusive(min_x: int, max_x: int, min_y: int, max_y: int) -> Coord:
        assert min_x <= max_x
        assert min_y <= max_y

        return Coord(x=randint(min_x, max_x), y=randint(min_y, max_y))
