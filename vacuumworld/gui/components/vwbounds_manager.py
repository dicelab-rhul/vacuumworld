from typing import cast

from pystarworldsturbo.utils.json.json_value import JSONValue


class VWBoundsManager():
    '''
    This class provides a quick way to check if two `int` numbers are within the bounds of the `grid_size` specified in the `config` argument.
    '''
    def __init__(self, config: dict[str, JSONValue]) -> None:
        self.__config: dict[str, JSONValue] = config

    def in_bounds(self, x: int, y: int) -> bool:
        '''
        WARNING: this method must only be used by the GUI, as the lower bound is `1` (not `0`) and the upper bound is `grid_size - 1` (not `grid_size`), both inclusive.

        Returns whether or not the provided `x` and `y` integers are within the bounds of the `grid_size` specified in the `config` argument.
        '''
        return x < cast(int, self.__config["grid_size"]) and x > 0 and y < cast(int, self.__config["grid_size"]) and y > 0
