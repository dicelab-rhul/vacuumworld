from typing import NamedTuple, Type, List, Union, Tuple
from vacuumworld.core.common.orientation import Orientation



class Coord(NamedTuple):
    '''
        A coordinate ``(x,y)``. Standard arethmetic operations ``(+ - * / //)`` can be performed on this object.
        
        Note that division (/ //) is always integer division.
        
        Attributes:
            * ``x (int)``: x component.
            * ``y (int)``: y component.
    '''
    x : int
    y : int

    def __add__(self, other: Union[int, List[int], Tuple[int, int]]) -> "Coord":
        if isinstance(other, int):
            return Coord(self[0] + other, self[1] + other)
        return Coord(self[0] + other[0], self[1] + other[1])
    
    def __sub__(self, other: Union[int, List[int], Tuple[int, int]]) -> "Coord":
        if isinstance(other, int):
            return Coord(self[0] - other, self[1] - other)
        return Coord(self[0] - other[0], self[1] - other[1])
    
    def __mul__(self, other: Union[int, List[int], Tuple[int, int]]) -> "Coord":
        if isinstance(other, int):
            return Coord(self[0] * other, self[1] * other)
        return Coord(self[0] * other[0], self[1] * other[1])
    
    def __truediv__(self, other: Union[int, List[int], Tuple[int, int]]) -> "Coord":
        if isinstance(other, int):
            return Coord(self[0] // other, self[1] // other)
        return Coord(self[0] // other[0], self[1] // other[1])

    def __floordiv__(self, other: Union[int, float]) -> "Coord":
        return self / other

    def forward(self, orientation: Orientation) -> "Coord":
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.x, y=self.y - 1)
        elif orientation == Orientation.south:
            return Coord(x=self.x, y=self.y + 1)
        elif orientation == Orientation.west:
            return Coord(x=self.x - 1, y=self.y)
        else:
            return Coord(x=self.x + 1, y=self.y)

    def backward(self, orientation: Orientation) -> "Coord":
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.x, y=self.y + 1)
        elif orientation == Orientation.south:
            return Coord(x=self.x, y=self.y - 1)
        elif orientation == Orientation.west:
            return Coord(x=self.x + 1, y=self.y)
        else:
            return Coord(x=self.x - 1, y=self.y)

    def left(self, orientation: Orientation) -> "Coord":
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.x - 1, y=self.y)
        elif orientation == Orientation.south:
            return Coord(x=self.x + 1, y=self.y)
        elif orientation == Orientation.west:
            return Coord(x=self.x, y=self.y + 1)
        else:
            return Coord(x=self.x, y=self.y - 1)

    def right(self, orientation: Orientation) -> "Coord":
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.x + 1, y=self.y)
        elif orientation == Orientation.south:
            return Coord(x=self.x - 1, y=self.y)
        elif orientation == Orientation.west:
            return Coord(x=self.x, y=self.y - 1)
        else:
            return Coord(x=self.x, y=self.y + 1)

    def forwardleft(self, orientation: Orientation) -> "Coord":
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.x - 1, y=self.y - 1)
        elif orientation == Orientation.south:
            return Coord(x=self.x + 1, y=self.y + 1)
        elif orientation == Orientation.west:
            return Coord(x=self.x - 1, y=self.y + 1)
        else:
            return Coord(x=self.x + 1, y=self.y - 1)

    def forwardright(self, orientation: Orientation) -> "Coord":
        assert orientation in [Orientation.north, Orientation.south, Orientation.west, Orientation.east]

        if orientation == Orientation.north:
            return Coord(x=self.x + 1, y=self.y - 1)
        elif orientation == Orientation.south:
            return Coord(x=self.x - 1, y=self.y + 1)
        elif orientation == Orientation.west:
            return Coord(x=self.x - 1, y=self.y - 1)
        else:
            return Coord(x=self.x + 1, y=self.y + 1)


coord: Type = Coord
