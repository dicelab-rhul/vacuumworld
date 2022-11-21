from __future__ import annotations
from typing import Dict, Iterable, List, Optional, Type, Tuple, Union, Iterator
from json import dumps

from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.common.perception import Perception
from pystarworldsturbo.common.action_result import ActionResult

from .vwposition_names import VWPositionNames
from .vworientation import VWOrientation
from ..model.environment.vwlocation import VWLocation
from ..model.actions.vwactions import VWAction
from ..model.actions.vwidle_action import VWIdleAction


class VWObservation(Perception):
    '''
    This class specifies the `VWObservation` API.

    An `VWObservation` is a wrapper for a 3x2 (or 2x3, or 2x2, or 2x1, or 1x2, or 1x1, depending on the boundaries) slice of a `VWEnvironment` grid, and a `List` of `ActionResult` elements, each related to an attempted `VWAction` by a certain `VWActor` in the last environmental cycle.
    '''
    def __init__(self, action_type: Type[VWAction], action_result: ActionResult, locations_dict: Dict[VWPositionNames, VWLocation]={}) -> None:
        super(VWObservation, self).__init__()

        assert locations_dict is not None

        for position_name in locations_dict:
            assert position_name in VWPositionNames

        self.__locations: Dict[VWPositionNames, VWLocation] = locations_dict
        self.__action_results: List[Tuple[Type[VWAction], ActionResult]] = [(action_type, action_result)]

    def get_latest_actions_results(self) -> List[Tuple[Type[VWAction], ActionResult]]:
        '''
        Returns a `List` of the results of each `VWAction` that was attempted by the `VWActor` during the last cycle.

        Each result is represented by a `Tuple[Type[VWAction], ActionResult]`, so to keep both the order of attempt, and the mapping between the kind of `VWAction` and its `ActionResult`.
        '''
        return self.__action_results

    def get_latest_actions_outcomes_as_dict(self) -> Dict[Type[VWAction], Union[ActionOutcome, List[ActionOutcome]]]:
        '''
        Returns a `Dict` mapping each kind of `VWAction` that was attempted by the `VWActor` during the last cycle to its `ActionOutcome`, or `List[ActionOutcome]`.

        The attempt order is not preserved in general, because the returned `Dict` exhibits no particular ordering for the keys.
        '''
        to_return: Dict[Type[VWAction], Union[ActionOutcome, List[ActionOutcome]]] = {}

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

    def merge_action_result_with_previous_observations(self, observations: Iterable[VWObservation]) -> None:
        '''
        WARNING: This method needs to be public, but it is not part of the public API of the `VWObservation` class.

        Merges this `VWObservation` with another `VWObservation` passed as an argument.

        There is not change to any `VWLocation` in this `VWObservation`.

        Each `ActionResult` in the `VWObservation` passed as an argument is prepended to the list of `ActionResult` in this `VWObservation`, as this `VWObservation` is the most recent one.
        '''
        assert len(self.__action_results) == 1

        previous_results: List[Tuple[Type[VWAction], ActionResult]] = []

        for observation in observations:
            assert len(observation.get_latest_actions_results()) == 1

            previous_results += observation.get_latest_actions_results()

        self.__action_results = previous_results + self.__action_results

    def is_empty(self) -> bool:
        '''
        Returns whether or not this `VWObservation` is empty, i.e. whether or not it contains any `VWLocation`.
        '''
        return not self.__locations

    def get_locations(self) -> Dict[VWPositionNames, VWLocation]:
        '''
        Returns a `Dict` mapping each `VWPositionNames` to the `VWLocation` at that position.

        If there is no `VWLocation` at a given position, then the corresponding key is not present in the returned `Dict`.
        '''
        return self.__locations

    def get_location_at(self, position_name: VWPositionNames) -> Optional[VWLocation]:
        '''
        Returns the `VWLocation` at the given `VWPositionNames`, or `None` if there is no `VWLocation` at that position.
        '''
        if position_name in self.__locations:
            return self.__locations[position_name]
        else:
            return None

    def get_center(self) -> Optional[VWLocation]:
        '''
        Returns the `VWLocation` at the center of the `VWActor`'s view, or `None` if there is no `VWLocation` at that position.
        '''
        if VWPositionNames.center in self.__locations:
            return self.__locations[VWPositionNames.center]
        else:
            return None

    def get_forward(self) -> Optional[VWLocation]:
        '''
        Returns the `VWLocation` in front of the `VWActor`, or `None` if there is no `VWLocation` at that position.
        '''
        if VWPositionNames.forward in self.__locations:
            return self.__locations[VWPositionNames.forward]
        else:
            return None

    def get_left(self) -> Optional[VWLocation]:
        '''
        Returns the `VWLocation` to the left of the `VWActor`, or `None` if there is no `VWLocation` at that position.
        '''
        if VWPositionNames.left in self.__locations:
            return self.__locations[VWPositionNames.left]
        else:
            return None

    def get_right(self) -> Optional[VWLocation]:
        '''
        Returns the `VWLocation` to the right of the `VWActor`, or `None` if there is no `VWLocation` at that position.
        '''
        if VWPositionNames.right in self.__locations:
            return self.__locations[VWPositionNames.right]
        else:
            return None

    def get_forwardleft(self) -> Optional[VWLocation]:
        '''
        Returns the `VWLocation` to the front-left of the `VWActor`, or `None` if there is no `VWLocation` at that position.
        '''
        if VWPositionNames.forwardleft in self.__locations:
            return self.__locations[VWPositionNames.forwardleft]
        else:
            return None

    def get_forwardright(self) -> Optional[VWLocation]:
        '''
        Returns the `VWLocation` to the front-right of the `VWActor`, or `None` if there is no `VWLocation` at that position.
        '''
        if VWPositionNames.forwardright in self.__locations:
            return self.__locations[VWPositionNames.forwardright]
        else:
            return None

    def is_wall_immediately_ahead(self) -> bool:
        '''
        Returns whether or not there is a wall immediately in front of the `VWActor`.
        '''
        actor_orientation: VWOrientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_center().has_wall_on(orientation=actor_orientation)

    def is_wall_immediately_behind(self) -> bool:
        '''
        Returns whether or not there is a wall immediately behind the `VWActor`.
        '''
        actor_orientation: VWOrientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_center().has_wall_on(orientation=actor_orientation.get_opposite())

    def is_wall_immediately_to_the_left(self) -> bool:
        '''
        Returns whether or not there is a wall immediately to the left of the `VWActor`.
        '''
        actor_orientation: VWOrientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_center().has_wall_on(orientation=actor_orientation.get_left())

    def is_wall_immediately_to_the_right(self) -> bool:
        '''
        Returns whether or not there is a wall immediately to the right of the `VWActor`.
        '''
        actor_orientation: VWOrientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_center().has_wall_on(orientation=actor_orientation.get_right())

    def is_wall_one_step_ahead(self) -> bool:
        '''
        Returns whether or not there is a wall one step in front of the `VWActor`.

        One step in front means that the `VWLocation` in front of the `VWActor` exists, and has a wall on its `forward` side (w.r.t the `VWOrientation` of the `VWActor`).
        '''
        if self.is_wall_immediately_ahead():
            return False

        assert self.get_forward() is not None

        actor_orientation: VWOrientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_forward().has_wall_on(orientation=actor_orientation)

    def is_wall_one_step_to_the_left(self) -> bool:
        '''
        Returns whether or not there is a wall one step to the `left` of the `VWActor`.

        One step to the `left` means that the `VWLocation` to the `left` of the `VWActor` exists, and has a wall on its `left` side (w.r.t the `VWOrientation` of the `VWActor`).
        '''
        if self.is_wall_immediately_to_the_left():
            return False

        assert self.get_left() is not None

        actor_orientation: VWOrientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_left().has_wall_on(orientation=actor_orientation.get_left())

    def is_wall_one_step_to_the_right(self) -> bool:
        '''
        Returns whether or not there is a wall one step to the `right` of the `VWActor`.

        One step to the `right` means that the `VWLocation` to the `right` of the `VWActor` exists, and has a wall on its `right` side (w.r.t the `VWOrientation` of the `VWActor`).
        '''
        if self.is_wall_immediately_to_the_right():
            return False

        assert self.get_right() is not None

        actor_orientation: VWOrientation = self.get_center().get_actor_appearance().get_orientation()

        return self.get_right().has_wall_on(orientation=actor_orientation.get_right())

    def is_wall_visible_somewhere_ahead(self) -> bool:
        '''
        Returns whether or not there is a wall visible somewhere in front of the `VWActor`.

        In practice, it returns whether exactly one of `self.is_wall_immediately_ahead()` and `self.is_wall_one_step_ahead()` is `True`.
        '''
        return self.is_wall_immediately_ahead() or self.is_wall_one_step_ahead()

    def is_wall_visible_somewhere_to_the_left(self) -> bool:
        '''
        Returns whether or not there is a wall visible somewhere to the `left` of the `VWActor`.

        In practice, it returns whether exactly one of `self.is_wall_immediately_to_the_left()` and `self.is_wall_one_step_to_the_left()` is `True`.
        '''
        return self.is_wall_immediately_to_the_left() or self.is_wall_one_step_to_the_left()

    def is_wall_visible_somewhere_to_the_right(self) -> bool:
        '''
        Returns whether or not there is a wall visible somewhere to the `right` of the `VWActor`.

        In practice, it returns whether exactly one of `self.is_wall_immediately_to_the_right()` and `self.is_wall_one_step_to_the_right()` is `True`.
        '''
        return self.is_wall_immediately_to_the_right() or self.is_wall_one_step_to_the_right()

    def is_wall_visible_ahead(self, immediately_ahead: bool) -> bool:
        '''
        Depending on the value of `immediately_ahead`, returns either the result of `self.is_wall_immediately_ahead()` or `self.is_wall_one_step_ahead()`.
        '''
        if immediately_ahead:
            return self.is_wall_immediately_ahead()
        elif self.is_wall_immediately_ahead():
            return False  # If the wall is immediately ahead, it is not one step ahead.
        else:
            return self.is_wall_one_step_ahead()

    def is_wall_visible_to_the_left(self, immediately_to_the_left: bool) -> bool:
        '''
        Depending on the value of `immediately_to_the_left`, returns either the result of `self.is_wall_immediately_to_the_left()` or `self.is_wall_one_step_to_the_left()`.
        '''
        if immediately_to_the_left:
            return self.is_wall_immediately_to_the_left()
        elif self.is_wall_immediately_to_the_left():
            return False  # If the wall is immediately to the left, it is not one step to the left.
        else:
            return self.is_wall_one_step_to_the_left()

    def is_wall_visible_to_the_right(self, immediately_to_the_right: bool) -> bool:
        '''
        Depending on the value of `immediately_to_the_right`, returns either the result of `self.is_wall_immediately_to_the_right()` or `self.is_wall_one_step_to_the_right()`.
        '''
        if immediately_to_the_right:
            return self.is_wall_immediately_to_the_right()
        elif self.is_wall_immediately_to_the_right():
            return False  # If the wall is immediately to the right, it is not one step to the right.
        else:
            return self.is_wall_one_step_to_the_right()

    @staticmethod
    def create_empty_observation() -> VWObservation:
        '''
        Returns an empty `VWObservation`.
        '''
        return VWObservation(action_type=VWIdleAction, action_result=ActionResult(outcome=ActionOutcome.impossible), locations_dict={})

    def __iter__(self) -> Iterator[VWLocation]:
        for location in self.__locations.values():
            yield location

    def __str__(self) -> str:
        return "Actions outcomes: [{}]. Perceived locations: {}".format(self.__format_latest_action_results(), self.__format_perceived_locations())

    def __format_perceived_locations(self) -> List[str]:
        return ["{}: {}".format(pos.name, loc) for pos, loc in self.__locations.items()]

    def pretty_format(self) -> str:
        '''
        Returns a pretty-formatted JSON string representation of this `VWObservation`, including each perceived `VWLocation`, and the `ActionOutcome` of each `VWAction` that was attempted by the `VWActor` during the last cycle.
        '''
        observation_dict: dict = {
            # The `.name` is necessary because `ActionOutcome` is an `Enum` and `Enum` objects are not JSON serialisable.
            "Action outcomes": [{action_type.__name__: action_result.get_outcome().name} for action_type, action_result in self.__action_results],
            "Perceived locations": {pos.name: loc.pretty_format() for pos, loc in self.__locations.items()}
        }

        return dumps(observation_dict, indent=4)
