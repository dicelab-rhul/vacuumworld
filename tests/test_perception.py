#!/usr/bin/env python3

from unittest import main, TestCase
from typing import Type, Callable, Any, cast
from random import choice, randint, random as randfloat
from uuid import uuid4
from sys import maxsize, float_info
from pyoptional.pyoptional import PyOptional

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.content_type import MessageContentType, MessageContentSimpleType

from vacuumworld import VacuumWorld
from vacuumworld.common.vwposition_names import VWPositionNames
from vacuumworld.common.vwvalidator import VWValidator
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwbroadcast_action import VWBroadcastAction
from vacuumworld.model.actions.vwclean_action import VWCleanAction
from vacuumworld.model.actions.vwdrop_action import VWDropAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vwmove_action import VWMoveAction
from vacuumworld.model.actions.vwspeak_action import VWSpeakAction
from vacuumworld.model.actions.vwturn_action import VWTurnAction
from vacuumworld.model.dirt.vwdirt_appearance import VWDirtAppearance
from vacuumworld.common.vworientation import VWOrientation
from vacuumworld.common.vwcolour import VWColour
from vacuumworld.model.actor.appearance.vwactor_appearance import VWActorAppearance
from vacuumworld.common.vwcoordinates import VWCoord
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.common.vwobservation import VWObservation
from vacuumworld.vwconfig_manager import VWConfigManager

import os
import random as random_module


class TestPerception(TestCase):
    '''
    This class tests `VWObservation` and `BccMessage`.
    '''
    def __init__(self, args: Any) -> None:
        super(TestPerception, self).__init__(args)

        self.__config: dict[str, Any] = VWConfigManager.load_config_from_file(config_file_path=VacuumWorld.CONFIG_FILE_PATH, load_additional_config=False)
        self.__min_grid_size: int = self.__config["min_environment_dim"]
        self.__max_grid_size: int = self.__config["max_environment_dim"]
        self.__number_of_locations: int = len(VWPositionNames)
        self.__progressive_id: int = 0
        self.__number_of_runs: int = 100
        self.__collection_size: int = 100
        self.__randbytes: Callable[[int], bytes] = random_module.randbytes if hasattr(random_module, "randbytes") else os.urandom

    def test_observation_coming_from_physical_action(self) -> None:
        '''
        Tests a `VWObservation` coming from a `VWPhysicalAction`.
        '''
        test_function: Callable[..., None] = self.__test_observation_coming_from_physical_action

        for _ in range(self.__number_of_runs):
            self.__test_observation(test_function=test_function)

    def test_observation_coming_from_communicative_action(self) -> None:
        '''
        Tests a `VWObservation` coming from a `VWCommunicativeAction`.
        '''
        test_function: Callable[..., None] = self.__test_observation_coming_from_communicative_action

        for _ in range(self.__number_of_runs):
            self.__test_observation(test_function=test_function)

    def test_observation_coming_from_multiple_actions(self) -> None:
        '''
        Tests a `VWObservation` coming from a combination of a `VWPhysicalAction` and a `VWCommunicativeAction`.
        '''
        test_function: Callable[..., None] = self.__test_observation_coming_from_multiple_actions

        for _ in range(self.__number_of_runs):
            self.__test_observation(test_function=test_function)

    def __test_observation(self, test_function: Callable[..., None]) -> None:
        grid_size: int = randint(self.__min_grid_size, self.__max_grid_size)
        coords: list[VWCoord] = self.__generate_random_coords(grid_size=grid_size)
        actors: list[PyOptional[VWActorAppearance]] = self.__generate_random_actor_appearances()
        dirts: list[PyOptional[VWDirtAppearance]] = self.__generate_random_dirt_appearances()
        perceived_locations: dict[VWPositionNames, VWLocation] = self.__generate_locations_dict(grid_size=grid_size, coords=coords, actors=actors, dirts=dirts)

        test_function(perceived_locations=perceived_locations, coords=coords, actors=actors, dirts=dirts)

        self.__progressive_id = 0

    def __test_observation_coming_from_physical_action(self, perceived_locations: dict[VWPositionNames, VWLocation], coords: list[VWCoord], actors: list[PyOptional[VWActorAppearance]], dirts: list[PyOptional[VWDirtAppearance]]) -> None:
        for action_type in [VWCleanAction, VWDropAction, VWIdleAction, VWMoveAction, VWTurnAction]:
            for action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                self.__test_observation_coming_from_single_action(perceived_locations=perceived_locations, coords=coords, actors=actors, dirts=dirts, action_type=action_type, action_outcome=action_outcome)

    def __test_observation_coming_from_communicative_action(self, perceived_locations: dict[VWPositionNames, VWLocation], coords: list[VWCoord], actors: list[PyOptional[VWActorAppearance]], dirts: list[PyOptional[VWDirtAppearance]]) -> None:
        for action_type in [VWSpeakAction, VWBroadcastAction]:
            for action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                self.__test_observation_coming_from_single_action(perceived_locations=perceived_locations, coords=coords, actors=actors, dirts=dirts, action_type=action_type, action_outcome=action_outcome)

    def __test_observation_coming_from_multiple_actions(self, perceived_locations: dict[VWPositionNames, VWLocation], coords: list[VWCoord], actors: list[PyOptional[VWActorAppearance]], dirts: list[PyOptional[VWDirtAppearance]]) -> None:
        for physical_action_type in [VWCleanAction, VWDropAction, VWIdleAction, VWMoveAction, VWTurnAction]:
            for communicative_action_type in [VWSpeakAction, VWBroadcastAction]:
                for physical_action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                    for communicative_action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                        physical_result: ActionResult = ActionResult(outcome=physical_action_outcome)
                        communicative_result: ActionResult = ActionResult(outcome=communicative_action_outcome)
                        physical_observation: VWObservation = VWObservation(action_type=physical_action_type, action_result=physical_result, locations_dict=perceived_locations)
                        communicative_observation: VWObservation = VWObservation(action_type=communicative_action_type, action_result=communicative_result, locations_dict=perceived_locations)
                        communicative_observation.merge_action_result_with_previous_observations(observations=[physical_observation])

                        self.__check_locations(o=communicative_observation, positions=VWPositionNames.elements(), coords=coords, actors=actors, dirts=dirts)

                        actions_outcomes: dict[Type[VWAction], list[ActionOutcome]] = communicative_observation.get_latest_actions_outcomes_as_dict()

                        self.assertTrue(len(actions_outcomes) == 2)
                        self.assertTrue(physical_action_type in actions_outcomes)
                        self.assertTrue(communicative_action_type in actions_outcomes)
                        self.assertTrue(VWValidator.does_type_match(t=list, obj=actions_outcomes[physical_action_type]))
                        self.assertTrue(all([VWValidator.does_type_match(t=ActionOutcome, obj=action_outcome) for action_outcome in actions_outcomes[physical_action_type]]))
                        self.assertTrue(VWValidator.does_type_match(t=list, obj=actions_outcomes[communicative_action_type]))
                        self.assertTrue(all([VWValidator.does_type_match(t=ActionOutcome, obj=action_outcome) for action_outcome in actions_outcomes[communicative_action_type]]))
                        self.assertIn(physical_action_outcome, actions_outcomes[physical_action_type])
                        self.assertIn(communicative_action_outcome, actions_outcomes[communicative_action_type])

    def __test_observation_coming_from_single_action(self, perceived_locations: dict[VWPositionNames, VWLocation], coords: list[VWCoord], actors: list[PyOptional[VWActorAppearance]], dirts: list[PyOptional[VWDirtAppearance]], action_type: Type[VWAction], action_outcome: ActionOutcome) -> None:
        result: ActionResult = ActionResult(outcome=action_outcome)
        o: VWObservation = VWObservation(action_type=action_type, action_result=result, locations_dict=perceived_locations)

        self.__check_locations(o=o, positions=VWPositionNames.elements(), coords=coords, actors=actors, dirts=dirts)

        actions_outcomes: dict[Type[VWAction], list[ActionOutcome]] = o.get_latest_actions_outcomes_as_dict()

        self.assertTrue(len(actions_outcomes) == 1)
        self.assertTrue(action_type in actions_outcomes)

        action_outcomes: list[ActionOutcome] = actions_outcomes[action_type]

        self.assertTrue(VWValidator.does_type_match(t=list, obj=action_outcomes))
        self.assertTrue(all([VWValidator.does_type_match(t=ActionOutcome, obj=action_outcome) for action_outcome in action_outcomes]))
        self.assertIn(action_outcome, action_outcomes)

    def __check_locations(self, o: VWObservation, positions: list[VWPositionNames], coords: list[VWCoord], actors: list[PyOptional[VWActorAppearance]], dirts: list[PyOptional[VWDirtAppearance]]) -> None:
        for i in range(len(positions)):
            self.__check_location(o=o, position=positions[i], coord=coords[i], actor_appearance=actors[i], dirt_appearance=dirts[i])

    def __check_location(self, o: VWObservation, position: VWPositionNames, coord: VWCoord, actor_appearance: PyOptional[VWActorAppearance], dirt_appearance: PyOptional[VWDirtAppearance]) -> None:
        self.__check_observer_id(observation=o, position=position, actor_appearance=actor_appearance)

        if o.get_location_at(position_name=position):
            self.__check_appearances(observation=o, position=position, actor_appearance=actor_appearance, dirt_appearance=dirt_appearance)

    def __check_observer_id(self, observation: VWObservation, position: VWPositionNames, actor_appearance: PyOptional[VWActorAppearance]) -> None:
        if position == VWPositionNames.center:
            self.assertTrue(observation.get_location_at(position_name=position).is_present())
            self.assertTrue(actor_appearance.is_present())
            self.assertEqual(actor_appearance.or_else_raise().get_id(), observation.get_observer_id().or_else_raise())

    def __check_appearances(self, observation: VWObservation, position: VWPositionNames, actor_appearance: PyOptional[VWActorAppearance], dirt_appearance: PyOptional[VWDirtAppearance]) -> None:
        if observation.get_location_at(position_name=position).is_present():
            location: PyOptional[VWLocation] = observation.get_location_at(position_name=position)

            if actor_appearance.is_present():
                self.assertEqual(location.or_else_raise().get_actor_appearance().or_else_raise(), actor_appearance.or_else_raise())
            else:
                self.assertTrue(location.or_else_raise().get_actor_appearance().is_empty())

            if dirt_appearance.is_present():
                self.assertEqual(location.or_else_raise().get_dirt_appearance().or_else_raise(), dirt_appearance.or_else_raise())
            else:
                self.assertTrue(location.or_else_raise().get_dirt_appearance().is_empty())

    def __generate_random_coords(self, grid_size: int) -> list[VWCoord]:
        return [VWCoord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1)) for _ in range(self.__number_of_locations)]

    def __generate_random_actor_appearances(self) -> list[PyOptional[VWActorAppearance]]:
        # The `VWLocation` at `PositionNames.center` must always have a `VWActorAppearance` (i.e., the observer) in it.
        # In particular, the first element of this list must be a `VWActorAppearance`.
        return [PyOptional.empty() if randfloat() < 0.5 and i > 0 else PyOptional.of(self.__generate_random_actor_appearance()) for i in range(self.__number_of_locations)]

    def __generate_random_actor_appearance(self) -> VWActorAppearance:
        actor_id: str = str(uuid4())
        colour: VWColour = choice(list(VWColour))
        orientation: VWOrientation = choice(list(VWOrientation))
        self.__progressive_id += 1

        return VWActorAppearance(actor_id=actor_id, progressive_id=str(self.__progressive_id), colour=colour, orientation=orientation)

    def __generate_random_dirt_appearances(self) -> list[PyOptional[VWDirtAppearance]]:
        return [PyOptional.empty() if randfloat() < 0.5 else PyOptional.of(self.__generate_random_dirt_appearance()) for _ in range(self.__number_of_locations)]

    def __generate_random_dirt_appearance(self) -> VWDirtAppearance:
        dirt_id: str = str(uuid4())
        colour: VWColour = choice(list(VWColour))
        self.__progressive_id += 1

        return VWDirtAppearance(dirt_id=dirt_id, progressive_id=str(self.__progressive_id), colour=colour)

    def __generate_locations_dict(self, grid_size: int, coords: list[VWCoord], actors: list[PyOptional[VWActorAppearance]], dirts: list[PyOptional[VWDirtAppearance]]) -> dict[VWPositionNames, VWLocation]:
        locations_dict: dict[VWPositionNames, PyOptional[VWLocation]] = {}

        for i in range(len(coords)):
            coord: VWCoord = coords[i]
            position = VWPositionNames.elements()[i]
            locations_dict[position] = PyOptional.of(VWLocation(coord=coord, actor_appearance=actors[i], dirt_appearance=dirts[i], wall=VWEnvironment.generate_wall_from_coordinates(coord=coord, grid_size=grid_size))) if coord.in_bounds(min_x=0, max_x=grid_size-1, min_y=0, max_y=grid_size-1) else PyOptional[VWLocation].empty()

        return {k: v.or_else_raise() for k, v in locations_dict.items() if v.is_present()}

    def test_message_with_int_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is an `int`.
        '''
        contents: list[int] = [randint(-maxsize + 1, maxsize) for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_float_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is a `float`.
        '''
        contents: list[float] = [randfloat() * float_info.max for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_str_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is a `str`.
        '''
        contents: list[str] = [self.__randbytes(randint(0, 2**16 - 1)).hex() for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_bytes_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is a `bytes` value.
        '''
        contents: list[bytes] = [self.__randbytes(randint(0, 2**16 - 1)) for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_list_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is a `list`.
        '''
        contents: list[list[MessageContentType]] = [self.__generate_random_list() for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_dict_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is a `dict`.
        '''
        contents: list[dict[MessageContentSimpleType, MessageContentType]] = [self.__generate_random_dict() for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_messages_with_recursion(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content contains recursive data structures.
        '''
        for content in (1, 1.32343, "foo", bytes("foobar", "utf-8"), ["foo", 1, 1.234, bytes("foobar", "utf-8"), {"foo": "bar"}], True, {1: ["", False], 1.2343: [3, 4.5]}):
            for sender_id in ("Sephiroth", "Jenova", "Hojo", "Rufus"):
                for recipient_id in ("Cloud", "Barret", "Red XIII", "Cid", "Vincent", "Tifa", "Yuffie", "Cait Sith", "Aerith"):
                    self.__test_message(content=cast(MessageContentType, content), sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_none_top_content(self) -> None:
        self.assertRaises(AssertionError, BccMessage, content=None, sender_id="Sephiroth", recipient_id="Cloud")

    def __test_message(self, content: MessageContentType, sender_id: str, recipient_id: str) -> None:
        message: BccMessage = BccMessage(content=content, sender_id=sender_id, recipient_id=recipient_id)

        self.assertEqual(content, message.get_content())
        self.assertEqual(sender_id, message.get_sender_id())
        self.assertEqual(len(message.get_recipients_ids()), 1)
        self.assertIn(recipient_id, message.get_recipients_ids())

    def __generate_random_list(self) -> list[MessageContentType]:
        return [self.__generate_random_element() for _ in range(randint(0, self.__collection_size))]

    def __generate_random_dict(self) -> dict[MessageContentSimpleType, MessageContentType]:
        return {self.__generate_random_key(): self.__generate_random_element() for _ in range(randint(0, self.__collection_size))}

    def __generate_random_element(self) -> MessageContentType:
        roll: float = randfloat() * 7

        if roll < 1:
            return randint(-maxsize + 1, maxsize)
        elif roll < 2:
            return randfloat() * float_info.max
        elif roll < 3:
            return self.__randbytes(randint(0, 2**16 - 1)).hex()
        elif roll < 4:
            return self.__randbytes(randint(0, 2**16 - 1))
        elif roll < 5:
            return choice([True, False])
        elif roll < 6:
            return []  # We want to avoid infinite recursion.
        elif roll < 7:
            return {}  # We want to avoid infinite recursion.
        else:
            raise ValueError("Invalid roll")

    def __generate_random_key(self) -> MessageContentSimpleType:
        roll: float = randfloat() * 3

        if roll < 1:
            return randint(-maxsize + 1, maxsize)
        elif roll < 2:
            return randfloat() * float_info.max
        elif roll < 3:
            return self.__randbytes(randint(0, 2**16 - 1)).hex()
        else:
            raise ValueError("Invalid roll")


if __name__ == "__main__":
    main()
