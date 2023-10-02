from __future__ import annotations
from typing import Dict, Iterable, List, Type, Tuple, Iterator, Any
from json import dumps
from pyoptional.pyoptional import PyOptional

from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.common.perception import Perception
from pystarworldsturbo.common.action_result import ActionResult

from .vwposition_names import VWPositionNames
from .vworientation import VWOrientation
from ..model.environment.vwlocation import VWLocation
from ..model.actions.vwactions import VWAction


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
            assert locations_dict[position_name] is not None

        self.__locations: Dict[VWPositionNames, VWLocation] = locations_dict
        self.__action_results: List[Tuple[Type[VWAction], ActionResult]] = [(action_type, action_result)]

    def get_observer_id(self) -> PyOptional[str]:
        '''
        Returns the `str` ID of the `VWActor` that presumably observed this `VWObservation`, or `None` if no observer can be identified.

        The observer is assumed to be the `VWActor` whose `VWActorAppearance` is contained by the `VWLocation` at the `VWPositionNames.center` position in this `VWObservation`.
        '''
        if VWPositionNames.center not in self.__locations or not self.__locations[VWPositionNames.center] or not self.__locations[VWPositionNames.center].has_actor():
            return PyOptional[str].empty()
        else:
            return PyOptional.of(self.__locations[VWPositionNames.center].get_actor_appearance().or_else_raise().get_id())

    def get_latest_actions_results(self) -> List[Tuple[Type[VWAction], ActionResult]]:
        '''
        Returns a `List` of the results of each `VWAction` that was attempted by the `VWActor` during the last cycle.

        Each result is represented by a `Tuple[Type[VWAction], ActionResult]`, so to preserve both the order of attempt, and the mapping between the kind of `VWAction` and its `ActionResult`.
        '''
        return self.__action_results

    def get_latest_actions_outcomes_as_dict(self) -> Dict[Type[VWAction], List[ActionOutcome]]:
        '''
        Returns a `Dict` mapping each kind of `VWAction` that was attempted by the `VWActor` during the last cycle to its `List[ActionOutcome]`.

        The attempt order is not preserved in general, because the returned `Dict` exhibits no particular ordering for the keys.
        '''
        to_return: Dict[Type[VWAction], List[ActionOutcome]] = {}

        for elm in self.__action_results:
            action_type: Type[VWAction] = elm[0]
            action_result: ActionResult = elm[1]

            if action_type not in to_return:
                to_return[action_type] = [action_result.get_outcome()]
            else:
                assert isinstance(to_return[action_type], list)

                to_return[action_type].append(action_result.get_outcome())

        return to_return

    def __format_latest_action_results(self) -> str:
        return ", ".join([f"{action_type.__name__}: {action_result.get_outcome()}" for action_type, action_result in self.__action_results])

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
        assert self.__locations is not None

        return len(self.__locations) == 0

    def get_locations(self) -> Dict[VWPositionNames, VWLocation]:
        '''
        Returns a `Dict` mapping each `VWPositionNames` to the `VWLocation` at that position.

        If there is no `VWLocation` at a given position, then the corresponding key is not present in the returned `Dict`.
        '''
        return self.__locations

    def get_location_at(self, position_name: VWPositionNames) -> PyOptional[VWLocation]:
        '''
        Returns a `PyOptional` wrapping the `VWLocation` at the given `VWPositionNames`, or an empty `PyOptional` if there is no `VWLocation` at that position.
        '''
        return PyOptional.of(self.__locations[position_name]) if position_name in self.__locations else PyOptional[VWLocation].empty()

    def get_locations_in_order(self) -> List[PyOptional[VWLocation]]:
        '''
        Returns a `List` of the `VWLocation` objects in this `VWObservation`, in the following order:
        * `VWPositionNames.center`
        * `VWPositionNames.forward`
        * `VWPositionNames.left`
        * `VWPositionNames.right`
        * `VWPositionNames.forwardleft`
        * `VWPositionNames.forwardright`
        '''
        return [PyOptional.of(self.__locations[position]) if position in self.__locations else PyOptional.empty() for position in VWPositionNames.elements_in_order()]

    def get_center(self) -> PyOptional[VWLocation]:
        '''
        Returns a `PyOptional` wrapping the `VWLocation` at the center of the `VWActor`'s view, or an empty `PyOptional` if there is no `VWLocation` at that position.
        '''
        return PyOptional.of(self.__locations[VWPositionNames.center]) if VWPositionNames.center in self.__locations else PyOptional[VWLocation].empty()

    def get_forward(self) -> PyOptional[VWLocation]:
        '''
        Returns a `PyOptional` wrapping the `VWLocation` in front of the `VWActor`, or an empty `PyOptional` if there is no `VWLocation` at that position.
        '''
        return PyOptional.of(self.__locations[VWPositionNames.forward]) if VWPositionNames.forward in self.__locations else PyOptional[VWLocation].empty()

    def get_left(self) -> PyOptional[VWLocation]:
        '''
        Returns a `PyOptional` wrapping the `VWLocation` to the left of the `VWActor`, or an empty `PyOptional` if there is no `VWLocation` at that position.
        '''
        return PyOptional.of(self.__locations[VWPositionNames.left]) if VWPositionNames.left in self.__locations else PyOptional[VWLocation].empty()

    def get_right(self) -> PyOptional[VWLocation]:
        '''
        Returns a `PyOptional` wrapping the `VWLocation` to the right of the `VWActor`, or an empty `PyOptional` if there is no `VWLocation` at that position.
        '''
        return PyOptional.of(self.__locations[VWPositionNames.right]) if VWPositionNames.right in self.__locations else PyOptional[VWLocation].empty()

    def get_forwardleft(self) -> PyOptional[VWLocation]:
        '''
        Returns a `PyOptional` wrapping the `VWLocation` to the front-left of the `VWActor`, or an empty `PyOptional` if there is no `VWLocation` at that position.
        '''
        return PyOptional.of(self.__locations[VWPositionNames.forwardleft]) if VWPositionNames.forwardleft in self.__locations else PyOptional[VWLocation].empty()

    def get_forwardright(self) -> PyOptional[VWLocation]:
        '''
        Returns a `PyOptional` wrapping the `VWLocation` to the front-right of the `VWActor`, or an empty `PyOptional` if there is no `VWLocation` at that position.
        '''
        return PyOptional.of(self.__locations[VWPositionNames.forwardright]) if VWPositionNames.forwardright in self.__locations else PyOptional[VWLocation].empty()

    def is_wall_immediately_ahead(self) -> bool:
        '''
        Returns whether or not there is a wall immediately in front of the `VWActor`.
        '''
        actor_orientation: VWOrientation = self.get_center().or_else_raise().get_actor_appearance().or_else_raise().get_orientation()

        return self.get_center().or_else_raise().has_wall_on(orientation=actor_orientation)

    def is_wall_immediately_behind(self) -> bool:
        '''
        Returns whether or not there is a wall immediately behind the `VWActor`.
        '''
        actor_orientation: VWOrientation = self.get_center().or_else_raise().get_actor_appearance().or_else_raise().get_orientation()

        return self.get_center().or_else_raise().has_wall_on(orientation=actor_orientation.get_opposite())

    def is_wall_immediately_to_the_left(self) -> bool:
        '''
        Returns whether or not there is a wall immediately to the left of the `VWActor`.
        '''
        actor_orientation: VWOrientation = self.get_center().or_else_raise().get_actor_appearance().or_else_raise().get_orientation()

        return self.get_center().or_else_raise().has_wall_on(orientation=actor_orientation.get_left())

    def is_wall_immediately_to_the_right(self) -> bool:
        '''
        Returns whether or not there is a wall immediately to the right of the `VWActor`.
        '''
        actor_orientation: VWOrientation = self.get_center().or_else_raise().get_actor_appearance().or_else_raise().get_orientation()

        return self.get_center().or_else_raise().has_wall_on(orientation=actor_orientation.get_right())

    def is_wall_one_step_ahead(self) -> bool:
        '''
        Returns whether or not there is a wall one step in front of the `VWActor`.

        One step in front means that the `VWLocation` in front of the `VWActor` exists, and has a wall on its `forward` side (w.r.t the `VWOrientation` of the `VWActor`).
        '''
        if self.is_wall_immediately_ahead():
            return False

        assert self.get_forward().is_present()

        actor_orientation: VWOrientation = self.get_center().or_else_raise().get_actor_appearance().or_else_raise().get_orientation()

        return self.get_forward().or_else_raise().has_wall_on(orientation=actor_orientation)

    def is_wall_one_step_to_the_left(self) -> bool:
        '''
        Returns whether or not there is a wall one step to the `left` of the `VWActor`.

        One step to the `left` means that the `VWLocation` to the `left` of the `VWActor` exists, and has a wall on its `left` side (w.r.t the `VWOrientation` of the `VWActor`).
        '''
        if self.is_wall_immediately_to_the_left():
            return False

        assert self.get_left().is_present()

        actor_orientation: VWOrientation = self.get_center().or_else_raise().get_actor_appearance().or_else_raise().get_orientation()

        return self.get_left().or_else_raise().has_wall_on(orientation=actor_orientation.get_left())

    def is_wall_one_step_to_the_right(self) -> bool:
        '''
        Returns whether or not there is a wall one step to the `right` of the `VWActor`.

        One step to the `right` means that the `VWLocation` to the `right` of the `VWActor` exists, and has a wall on its `right` side (w.r.t the `VWOrientation` of the `VWActor`).
        '''
        if self.is_wall_immediately_to_the_right():
            return False

        assert self.get_right().is_present()

        actor_orientation: VWOrientation = self.get_center().or_else_raise().get_actor_appearance().or_else_raise().get_orientation()

        return self.get_right().or_else_raise().has_wall_on(orientation=actor_orientation.get_right())

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

    def __iter__(self) -> Iterator[VWLocation]:
        for location in self.__locations.values():
            yield location

    def __str__(self) -> str:
        return f"Actions outcomes: [{self.__format_latest_action_results()}]. Perceived locations: {self.__format_perceived_locations()}"

    def __format_perceived_locations(self) -> List[str]:
        return [f"{pos.name}: {loc}" for pos, loc in self.__locations.items()]

    def pretty_format(self) -> str:
        '''
        Returns a pretty-formatted JSON string representation of this `VWObservation`, including each perceived `VWLocation`, and the `ActionOutcome` of each `VWAction` that was attempted by the `VWActor` during the last cycle.
        '''
        observation_dict: dict[str, Any] = {
            # The `.name` is necessary because `ActionOutcome` is an `Enum` and `Enum` objects are not JSON serialisable.
            "Action outcomes": [{action_type.__name__: action_result.get_outcome().name} for action_type, action_result in self.__action_results],
            "Perceived locations": {pos.name: loc.pretty_format() for pos, loc in self.__locations.items() if loc}
        }

        return dumps(observation_dict, indent=4)
