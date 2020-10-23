from typing import NamedTuple



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

    # TODO: add assertions or checks on the nature of `other`

    def __add__(self, other):
        if isinstance(other, int):
            return Coord(self[0] + other, self[1] + other)
        return Coord(self[0] + other[0], self[1] + other[1])
    
    def __sub__(self, other):
        if isinstance(other, int):
            return Coord(self[0] - other, self[1] - other)
        return Coord(self[0] - other[0], self[1] - other[1])
    
    def __mul__(self, other):
        if isinstance(other, int):
            return Coord(self[0] * other, self[1] * other)
        return Coord(self[0] * other[0], self[1] * other[1])
    
    def __truediv__(self, other):
        if isinstance(other, int):
            return Coord(self[0] // other, self[1] // other)
        return Coord(self[0] // other[0], self[1] // other[1])

    def __floordiv__(self, other):
        return self / other

coord = Coord
