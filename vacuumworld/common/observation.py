from __future__ import annotations
from typing import Dict, Iterable, List, Optional, Type, Tuple, Union
from json import dumps

from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.common.perception import Perception
from pystarworldsturbo.common.action_result import ActionResult

from .position_names import PositionNames
from .orientation import Orientation
from ..model.environment.vwlocation import VWLocation
from ..model.actions.vwactions import VWAction
from ..model.actions.idle_action import VWIdleAction


class Observation(Perception):
    def __init__(self, action_type: Type[VWAction], action_result: ActionResult, locations_dict: Dict[PositionNames, VWLocation]={}) -> None:
        super(Observation, self).__init__()

        assert locations_dict is not None

        for position_name in locations_dict:
            assert position_name in PositionNames

        self.__locations: Dict[PositionNames, VWLocation] = locations_dict
        self.__action_results: List[Tuple[Type[VWAction], ActionResult]] = [(action_type, action_result)]

    def get_latest_actions_results(self) -> List[Tuple[Type[VWAction], ActionResult]]:
        return self.__action_results

    def get_latest_actions_results_as_dict(self) -> Dict[Type[VWAction], Union[ActionResult, List[ActionResult]]]:
        to_return: Dict[Type[VWAction], Union[ActionResult, List[ActionResult]]] = {}

        for elm in self.__action_results:
            action_type: Type[VWAction] = elm[0]
            action_result: ActionResult = elm[1]

            if action_type not in to_return:
                to_return[action_type.__name__] = action_result.get_outcome()
            elif isinstance(to_return[action_type.__name__], list):
                    to_return[action_type.__name__].append(action_result.get_outcome())
            else:
                to_return[action_type.__name__] = [to_return[action_type.__name__], action_result.get_outcome()]

        return to_return

    def __format_latest_action_results(self) -> str:
        return ", ".join(["{}: {}".format(action_type.__name__, action_result.get_outcome()) for action_type, action_result in self.__action_results])

    def merge_action_result_with_previous_observations(self, observations: Iterable[Observation]) -> None:
        assert len(self.__action_results) == 1

        previous_results: List[Tuple[Type[VWAction], ActionResult]] = []

        for observation in observations:
            assert len(observation.get_latest_actions_results()) == 1

            previous_results += observation.get_latest_actions_results()

        self.__action_results = previous_results + self.__action_results

    def is_empty(self) -> bool:
        return not self.__locations

    def get_locations(self) -> Dict[PositionNames, VWLocation]:
        return self.__locations

    def get_location_at(self, position_name: PositionNames) -> Optional[VWLocation]:
        if position_name in self.__locations:
            return self.__locations[position_name]
        else:
            return None

    def get_center(self) -> Optional[VWLocation]:
        if PositionNames.center in self.__locations:
            return self.__locations[PositionNames.center]
        else:
            return None

    def get_forward(self) -> Optional[VWLocation]:
        if PositionNames.forward in self.__locations:
            return self.__locations[PositionNames.forward]
        else:
            return None

    def get_left(self) -> Optional[VWLocation]:
        if PositionNames.left in self.__locations:
            return self.__locations[PositionNames.left]
        else:
            return None

    def get_right(self) -> Optional[VWLocation]:
        if PositionNames.right in self.__locations:
            return self.__locations[PositionNames.right]
        else:
            return None

    def get_forwardleft(self) -> Optional[VWLocation]:
        if PositionNames.forwardleft in self.__locations:
            return self.__locations[PositionNames.forwardleft]
        else:
            return None

    def get_forwardright(self) -> Optional[VWLocation]:
        if PositionNames.forwardright in self.__locations:
            return self.__locations[PositionNames.forwardright]
        else:
            return None

    def is_wall_immediately_ahead(self) -> bool:
        actor_orientation: Orientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_center().has_wall_on(orientation=actor_orientation)

    def is_wall_immediately_behind(self) -> bool:
        actor_orientation: Orientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_center().has_wall_on(orientation=actor_orientation.get_opposite())

    def is_wall_immediately_to_the_left(self) -> bool:
        actor_orientation: Orientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_center().has_wall_on(orientation=actor_orientation.get_left())

    def is_wall_immediately_to_the_right(self) -> bool:
        actor_orientation: Orientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_center().has_wall_on(orientation=actor_orientation.get_right())

    def is_wall_one_step_ahead(self) -> bool:
        if self.is_wall_immediately_ahead():
            return False

        assert self.get_forward() is not None

        actor_orientation: Orientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_forward().has_wall_on(orientation=actor_orientation)

    def is_wall_one_step_to_the_left(self) -> bool:
        if self.is_wall_immediately_to_the_left():
            return False

        assert self.get_left() is not None

        actor_orientation: Orientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_left().has_wall_on(orientation=actor_orientation.get_left())

    def is_wall_one_step_to_the_right(self) -> bool:
        if self.is_wall_immediately_to_the_right():
            return False

        assert self.get_right() is not None

        actor_orientation: Orientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_right().has_wall_on(orientation=actor_orientation.get_right())

    def is_wall_visible_somewhere_ahead(self) -> bool:
        return self.is_wall_immediately_ahead() or self.is_wall_one_step_ahead()

    def is_wall_visible_somewhere_to_the_left(self) -> bool:
        return self.is_wall_immediately_to_the_left() or self.is_wall_one_step_to_the_left()

    def is_wall_visible_somewhere_to_the_right(self) -> bool:
        return self.is_wall_immediately_to_the_right() or self.is_wall_one_step_to_the_right()

    def is_wall_visible_ahead(self, immediately_ahead: bool) -> bool:
        if immediately_ahead:
            return self.is_wall_immediately_ahead()
        elif self.is_wall_immediately_ahead():
            return False  # If the wall is immediately ahead, it is not one step ahead.
        else:
            return self.is_wall_one_step_ahead()

    def is_wall_visible_to_the_left(self, immediately_to_the_left: bool) -> bool:
        if immediately_to_the_left:
            return self.is_wall_immediately_to_the_left()
        elif self.is_wall_immediately_to_the_left():
            return False  # If the wall is immediately to the left, it is not one step to the left.
        else:
            return self.is_wall_one_step_to_the_left()

    def is_wall_visible_to_the_right(self, immediately_to_the_right: bool) -> bool:
        if immediately_to_the_right:
            return self.is_wall_immediately_to_the_right()
        elif self.is_wall_immediately_to_the_right():
            return False  # If the wall is immediately to the right, it is not one step to the right.
        else:
            return self.is_wall_one_step_to_the_right()

    @staticmethod
    def create_empty_observation() -> Observation:
        return Observation(action_type=VWIdleAction, action_result=ActionResult(outcome=ActionOutcome.impossible), locations_dict={})

    def __iter__(self) -> Iterable:
        for location in self.__locations.values():
            yield location

    def __str__(self) -> str:
        return "Actions outcomes: [{}]. Perceived locations: {}".format(self.__format_latest_action_results(), self.__format_perceived_locations())

    def __format_perceived_locations(self) -> List[str]:
        return ["{}: {}".format(pos.name, loc) for pos, loc in self.__locations.items()]

    def pretty_format(self) -> str:
        observation_dict: dict = {
            "Action outcomes": [{action_type.__name__: action_result.get_outcome()} for action_type, action_result in self.__action_results],
            "Perceived locations": {pos.name: loc.pretty_format() for pos, loc in self.__locations.items()}
        }

        return dumps(observation_dict, indent=4)
