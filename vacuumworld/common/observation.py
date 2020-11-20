from typing import Dict, Iterable, List

from pystarworldsturbo.common.perception import Perception
from pystarworldsturbo.common.action_result import ActionResult

from .position_names import PositionNames
from ..model.environment.vwlocation import VWLocation



class Observation(Perception):
    def __init__(self, action_result: ActionResult, locations_dict: Dict[PositionNames, VWLocation]={}) -> None:
        super(Observation, self).__init__()

        assert locations_dict is not None

        for position_name in locations_dict:
            assert position_name in PositionNames

        self.__locations: Dict[PositionNames, VWLocation] = locations_dict
        self.__action_result: ActionResult = action_result

        self.__create_quick_api()

    def __create_quick_api(self) -> None:
        self.center: VWLocation = self.get_center()
        self.left: VWLocation = self.get_left()
        self.right: VWLocation = self.get_right()
        self.forwardleft: VWLocation = self.get_forwardleft()
        self.forwardright: VWLocation = self.get_forwardright()

    def get_latest_action_result(self) -> ActionResult:
        return self.__action_result

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

    def __str__(self) -> str:
        return "Action outcome: {}. Perceived locations: {}".format(self.__action_result.get_outcome(), self.__format_perceived_locations())

    def __format_perceived_locations(self) -> List[str]:
        return ["{}: {}".format(str(pos), str(loc)) for pos, loc in self.__locations.items()]
