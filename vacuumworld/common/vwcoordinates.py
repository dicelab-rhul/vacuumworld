from __future__ import annotations
from typing import Dict, List, Union, Tuple, Iterator
from random import randint

from .vworientation import VWOrientation


class VWCoord():
    '''
    This class specifies numerical coordinates.

    Each `VWCoord` object is characterised by two integers named `x` and `y`.
    '''
    def __init__(self, x: int, y: int) -> None:
        if not isinstance(x, int):
            raise TypeError("x must be an integer")

        if not isinstance(y, int):
            raise TypeError("y must be an integer")

        self.__x: int = x
        self.__y: int = y

    def get_x(self) -> int:
        '''
        Returns the `x` coordinate of this `VWCoord` as an `int`.
        '''
        return self.__x

    def get_y(self) -> int:
        '''
        Returns the `y` coordinate of this `VWCoord` as an `int`.
        '''
        return self.__y

    def in_bounds(self, min_x: int, max_x: int, min_y: int, max_y: int) -> bool:
        '''
        Returns whether or not this `VWCoord` is within the given inclusive bounds.
        '''
        return min_x <= self.__x <= max_x and min_y <= self.__y <= max_y

    def forward(self, orientation: VWOrientation) -> VWCoord:
        '''
        Returns a `VWCoord` that is one step forward from this `VWCoord` in the given `VWOrientation`.
        '''
        assert orientation in [VWOrientation.north, VWOrientation.south, VWOrientation.west, VWOrientation.east]

        if orientation == VWOrientation.north:
            return VWCoord(x=self.__x, y=self.__y - 1)
        elif orientation == VWOrientation.south:
            return VWCoord(x=self.__x, y=self.__y + 1)
        elif orientation == VWOrientation.west:
            return VWCoord(x=self.__x - 1, y=self.__y)
        else:
            return VWCoord(x=self.__x + 1, y=self.__y)

    def backward(self, orientation: VWOrientation) -> VWCoord:
        '''
        Returns a `VWCoord` that is one step backward from this `VWCoord` in the given `VWOrientation`.
        '''
        assert orientation in [VWOrientation.north, VWOrientation.south, VWOrientation.west, VWOrientation.east]

        if orientation == VWOrientation.north:
            return VWCoord(x=self.__x, y=self.__y + 1)
        elif orientation == VWOrientation.south:
            return VWCoord(x=self.__x, y=self.__y - 1)
        elif orientation == VWOrientation.west:
            return VWCoord(x=self.__x + 1, y=self.__y)
        else:
            return VWCoord(x=self.__x - 1, y=self.__y)

    def left(self, orientation: VWOrientation) -> VWCoord:
        '''
        Returns a `VWCoord` that is one step to the left from this `VWCoord` in the given `VWOrientation`.
        '''
        assert orientation in [VWOrientation.north, VWOrientation.south, VWOrientation.west, VWOrientation.east]

        if orientation == VWOrientation.north:
            return VWCoord(x=self.__x - 1, y=self.__y)
        elif orientation == VWOrientation.south:
            return VWCoord(x=self.__x + 1, y=self.__y)
        elif orientation == VWOrientation.west:
            return VWCoord(x=self.__x, y=self.__y + 1)
        else:
            return VWCoord(x=self.__x, y=self.__y - 1)

    def right(self, orientation: VWOrientation) -> VWCoord:
        '''
        Returns a `VWCoord` that is one step to the right from this `VWCoord` in the given `VWOrientation`.
        '''
        assert orientation in [VWOrientation.north, VWOrientation.south, VWOrientation.west, VWOrientation.east]

        if orientation == VWOrientation.north:
            return VWCoord(x=self.__x + 1, y=self.__y)
        elif orientation == VWOrientation.south:
            return VWCoord(x=self.__x - 1, y=self.__y)
        elif orientation == VWOrientation.west:
            return VWCoord(x=self.__x, y=self.__y - 1)
        else:
            return VWCoord(x=self.__x, y=self.__y + 1)

    def forwardleft(self, orientation: VWOrientation) -> VWCoord:
        '''
        Returns a `VWCoord` that is one step forward and one step to the left from this `VWCoord` in the given `VWOrientation`.
        '''
        assert orientation in [VWOrientation.north, VWOrientation.south, VWOrientation.west, VWOrientation.east]

        if orientation == VWOrientation.north:
            return VWCoord(x=self.__x - 1, y=self.__y - 1)
        elif orientation == VWOrientation.south:
            return VWCoord(x=self.__x + 1, y=self.__y + 1)
        elif orientation == VWOrientation.west:
            return VWCoord(x=self.__x - 1, y=self.__y + 1)
        else:
            return VWCoord(x=self.__x + 1, y=self.__y - 1)

    def forwardright(self, orientation: VWOrientation) -> VWCoord:
        '''
        Returns a `VWCoord` that is one step forward and one step to the right from this `VWCoord` in the given `VWOrientation`.
        '''
        assert orientation in [VWOrientation.north, VWOrientation.south, VWOrientation.west, VWOrientation.east]

        if orientation == VWOrientation.north:
            return VWCoord(x=self.__x + 1, y=self.__y - 1)
        elif orientation == VWOrientation.south:
            return VWCoord(x=self.__x - 1, y=self.__y + 1)
        elif orientation == VWOrientation.west:
            return VWCoord(x=self.__x - 1, y=self.__y - 1)
        else:
            return VWCoord(x=self.__x + 1, y=self.__y + 1)

    def clone(self) -> VWCoord:
        '''
        Returns a deep-copy of this `VWCoord`.
        '''
        return VWCoord(x=self.__x, y=self.__y)

    def to_json(self) -> Dict[str, int]:
        '''
        Returns a JSON representation of this `VWCoord`.
        '''
        return {
            "x": self.__x,
            "y": self.__y
        }

    def __add__(self, other: Union[int, VWCoord, List[int], Tuple[int, int]]) -> VWCoord:
        assert other is not None

        if isinstance(other, int):
            return VWCoord(x=self[0] + other, y=self[1] + other)
        elif isinstance(other, VWCoord):
            return VWCoord(x=self[0] + other[0], y=self[1] + other[1])
        else:
            assert type(other) in [list, tuple] and len(other) == len(self)
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return VWCoord(x=self[0] + other[0], y=self[1] + other[1])

    def __sub__(self, other: Union[int, VWCoord, List[int], Tuple[int, int]]) -> VWCoord:
        assert other is not None

        if isinstance(other, int):
            return VWCoord(x=self[0] - other, y=self[1] - other)
        elif isinstance(other, VWCoord):
            return VWCoord(x=self[0] - other[0], y=self[1] - other[1])
        else:
            assert type(other) in [list, tuple] and len(other) == len(self)
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return VWCoord(x=self[0] - other[0], y=self[1] - other[1])

    def __mul__(self, other: Union[int, VWCoord, List[int], Tuple[int, int]]) -> VWCoord:
        assert other is not None

        if isinstance(other, int):
            return VWCoord(x=self[0] * other, y=self[1] * other)
        elif isinstance(other, VWCoord):
            return VWCoord(x=self[0] * other[0], y=self[1] * other[1])
        else:
            assert type(other) in [list, tuple] and len(other) == len(self)
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return VWCoord(x=self[0] * other[0], y=self[1] * other[1])

    # Integer division.
    def __floordiv__(self, other: Union[int, VWCoord, List[int], Tuple[int, int]]) -> VWCoord:
        assert other is not None

        if isinstance(other, int):
            return VWCoord(x=self[0] // other, y=self[1] // other)
        elif isinstance(other, VWCoord):
            return VWCoord(x=self[0] // other[0], y=self[1] // other[1])
        else:
            assert type(other) in [list, tuple] and len(other) == len(self)
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return VWCoord(x=self[0] // other[0], y=self[1] // other[1])

    # We force `/` to work like `//`.
    def __truediv__(self, other: Union[int, VWCoord, List[int], Tuple[int, int]]) -> VWCoord:
        assert other is not None

        if isinstance(other, int):
            return self // other
        elif isinstance(other, VWCoord):
            return self // other
        else:
            assert type(other) in [list, tuple] and len(other) == len(self)
            assert isinstance(other[0], int) and isinstance(other[1], int)

            return self // (int(other[0]), int(other[1]))

    def __str__(self) -> str:
        return "({}, {})".format(self.__x, self.__y)

    def __eq__(self, other: object) -> bool:
        if not other or not isinstance(other, VWCoord):
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
    def random_between_inclusive(min_x: int, max_x: int, min_y: int, max_y: int) -> VWCoord:
        '''
        Returns a random `VWCoord` between the given inclusive bounds.
        '''
        assert min_x <= max_x
        assert min_y <= max_y

        return VWCoord(x=randint(min_x, max_x), y=randint(min_y, max_y))