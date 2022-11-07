from __future__ import annotations
from typing import Dict, List, Union, Tuple, Iterator
from random import randint

from .orientation import Orientation


class Coord():
    def __init__(self, x: int, y: int) -> None:
        if not isinstance(x, int):
            raise TypeError("x must be an integer")

        if not isinstance(y, int):
            raise TypeError("y must be an integer")

        self.__x: int = x
        self.__y: int = y

        # Fallback for 4.2.7.
        # TODO: remove when 4.2.7 is no longer supported.
        self.x: int = self.get_x()
        self.y: int = self.get_y()

    def get_x(self) -> int:
        '''
        Returns the `x` coordinate as an `int`.
        '''
        return self.__x

    def get_y(self) -> int:
        '''
        Returns the `y` coordinate as an `int`.
        '''
        return self.__y

    def in_bounds(self, min_x: int, max_x: int, min_y: int, max_y: int) -> bool:
        '''
        Returns whether or not the current `Coord` is within the given inclusive bounds.
        '''
        return min_x <= self.__x <= max_x and min_y <= self.__y <= max_y

    def forward(self, orientation: Orientation) -> Coord:
        '''
        Returns a `Coord` that is one step forward from the current `Coord` in the given `Orientation`.
        '''
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.__x, y=self.__y - 1)
        elif orientation == Orientation.south:
            return Coord(x=self.__x, y=self.__y + 1)
        elif orientation == Orientation.west:
            return Coord(x=self.__x - 1, y=self.__y)
        else:
            return Coord(x=self.__x + 1, y=self.__y)

    def backward(self, orientation: Orientation) -> Coord:
        '''
        Returns a `Coord` that is one step backward from the current `Coord` in the given `Orientation`.
        '''
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.__x, y=self.__y + 1)
        elif orientation == Orientation.south:
            return Coord(x=self.__x, y=self.__y - 1)
        elif orientation == Orientation.west:
            return Coord(x=self.__x + 1, y=self.__y)
        else:
            return Coord(x=self.__x - 1, y=self.__y)

    def left(self, orientation: Orientation) -> Coord:
        '''
        Returns a `Coord` that is one step to the left from the current `Coord` in the given `Orientation`.
        '''
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.__x - 1, y=self.__y)
        elif orientation == Orientation.south:
            return Coord(x=self.__x + 1, y=self.__y)
        elif orientation == Orientation.west:
            return Coord(x=self.__x, y=self.__y + 1)
        else:
            return Coord(x=self.__x, y=self.__y - 1)

    def right(self, orientation: Orientation) -> Coord:
        '''
        Returns a `Coord` that is one step to the right from the current `Coord` in the given `Orientation`.
        '''
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.__x + 1, y=self.__y)
        elif orientation == Orientation.south:
            return Coord(x=self.__x - 1, y=self.__y)
        elif orientation == Orientation.west:
            return Coord(x=self.__x, y=self.__y - 1)
        else:
            return Coord(x=self.__x, y=self.__y + 1)

    def forwardleft(self, orientation: Orientation) -> Coord:
        '''
        Returns a `Coord` that is one step forward and one step to the left from the current `Coord` in the given `Orientation`.
        '''
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.__x - 1, y=self.__y - 1)
        elif orientation == Orientation.south:
            return Coord(x=self.__x + 1, y=self.__y + 1)
        elif orientation == Orientation.west:
            return Coord(x=self.__x - 1, y=self.__y + 1)
        else:
            return Coord(x=self.__x + 1, y=self.__y - 1)

    def forwardright(self, orientation: Orientation) -> Coord:
        '''
        Returns a `Coord` that is one step forward and one step to the right from the current `Coord` in the given `Orientation`.
        '''
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.__x + 1, y=self.__y - 1)
        elif orientation == Orientation.south:
            return Coord(x=self.__x - 1, y=self.__y + 1)
        elif orientation == Orientation.west:
            return Coord(x=self.__x - 1, y=self.__y - 1)
        else:
            return Coord(x=self.__x + 1, y=self.__y + 1)

    def clone(self) -> Coord:
        '''
        Returns a deep-copy of the current `Coord`.
        '''
        return Coord(x=self.__x, y=self.__y)

    def to_json(self) -> Dict[str, int]:
        '''
        Returns a JSON representation of the current `Coord`.
        '''
        return {
            "x": self.__x,
            "y": self.__y
        }

    def __add__(self, other: Union[int, Coord, List[int], Tuple[int, int]]) -> Coord:
        assert other is not None

        if isinstance(other, int):
            return Coord(x=self[0] + other, y=self[1] + other)
        elif isinstance(other, Coord):
            return Coord(x=self[0] + other[0], y=self[1] + other[1])
        else:
            assert type(other) in [list, tuple] and len(other) == len(self)
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return Coord(x=self[0] + other[0], y=self[1] + other[1])

    def __sub__(self, other: Union[int, Coord, List[int], Tuple[int, int]]) -> Coord:
        assert other is not None

        if isinstance(other, int):
            return Coord(x=self[0] - other, y=self[1] - other)
        elif isinstance(other, Coord):
            return Coord(x=self[0] - other[0], y=self[1] - other[1])
        else:
            assert type(other) in [list, tuple] and len(other) == len(self)
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return Coord(x=self[0] - other[0], y=self[1] - other[1])

    def __mul__(self, other: Union[int, Coord, List[int], Tuple[int, int]]) -> Coord:
        assert other is not None

        if isinstance(other, int):
            return Coord(x=self[0] * other, y=self[1] * other)
        elif isinstance(other, Coord):
            return Coord(x=self[0] * other[0], y=self[1] * other[1])
        else:
            assert type(other) in [list, tuple] and len(other) == len(self)
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return Coord(x=self[0] * other[0], y=self[1] * other[1])

    # Integer division.
    def __floordiv__(self, other: Union[int, Coord, List[int], Tuple[int, int]]) -> Coord:
        assert other is not None

        if isinstance(other, int):
            return Coord(x=self[0] // other, y=self[1] // other)
        elif isinstance(other, Coord):
            return Coord(x=self[0] // other[0], y=self[1] // other[1])
        else:
            assert type(other) in [list, tuple] and len(other) == len(self)
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return Coord(x=self[0] // other[0], y=self[1] // other[1])

    # We force `/` to work like `//`.
    def __truediv__(self, other: Union[int, Coord, List[int], Tuple[int, int]]) -> Coord:
        assert other is not None

        if isinstance(other, int):
            return self // other
        elif isinstance(other, Coord):
            return self // other
        else:
            assert type(other) in [list, tuple] and len(other) == len(self)
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return self // (int(other[0]), int(other[1]))

    def __str__(self) -> str:
        return "({}, {})".format(self.__x, self.__y)

    def __eq__(self, other: object) -> bool:
        if not other or not isinstance(other, Coord):
            return False

        return self.__x == other.get_x() and self.__y == other.get_y()

    def __hash__(self) -> int:
        return hash((self.__x, self.__y))

    def __iter__(self) -> Iterator[int]:
        for i in [self.__x, self.__y]:
            yield i

    def __getitem__(self, index: int) -> int:
        assert index in [0, 1]

        if index == 0:
            return self.__x
        else:
            return self.__y

    @staticmethod
    def random_between_inclusive(min_x: int, max_x: int, min_y: int, max_y: int) -> Coord:
        '''
        Returns a random `Coord` between the given inclusive bounds.
        '''
        assert min_x <= max_x
        assert min_y <= max_y

        return Coord(x=randint(min_x, max_x), y=randint(min_y, max_y))
