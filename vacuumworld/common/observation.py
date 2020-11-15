from typing import Dict, Iterable

from pystarworldsturbo.common.perception import Perception

from .position_names import PositionNames
from ..model.environment.vwlocation import VWLocation



class Observation(Perception):
    def __init__(self, locations_dict: Dict[PositionNames, VWLocation]={}) -> None:
        super(Observation, self).__init__()

        assert locations_dict is not None

        for position_name in locations_dict:
            assert position_name in PositionNames

        self.__locations: Dict[PositionNames, VWLocation]

    def get_center(self) -> VWLocation:
        if PositionNames.center in self.__locations:
            return self.__locations[PositionNames.center]
        else:
            return None

    def get_forward(self) -> VWLocation:
        if PositionNames.forward in self.__locations:
            return self.__locations[PositionNames.forward]
        else:
            return None

    def get_left(self) -> VWLocation:
        if PositionNames.left in self.__locations:
            return self.__locations[PositionNames.left]
        else:
            return None

    def get_right(self) -> VWLocation:
        if PositionNames.right in self.__locations:
            return self.__locations[PositionNames.right]
        else:
            return None

    def get_forwardleft(self) -> VWLocation:
        if PositionNames.forwardleft in self.__locations:
            return self.__locations[PositionNames.forwardleft]
        else:
            return None

    def get_forwardright(self) -> VWLocation:
        if PositionNames.forwardright in self.__locations:
            return self.__locations[PositionNames.forwardright]
        else:
            return None

    def __iter__(self) -> Iterable:
        return self.__locations.values()