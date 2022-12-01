#!/usr/bin/env python3

from unittest import main, TestCase
from typing import Dict, Optional, List, Union, Type, Callable, Tuple
from random import choice, randint, random as randfloat
from uuid import uuid4
from sys import maxsize, float_info

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.common.action_result import ActionResult

from vacuumworld import VacuumWorld
from vacuumworld.common.vwposition_names import VWPositionNames
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
    def __init__(self, args) -> None:
        super(TestPerception, self).__init__(args)

        self.__config: dict = VWConfigManager.load_config_from_file(config_file_path=VacuumWorld.CONFIG_FILE_PATH)
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
        test_function: Callable = self.__test_observation_coming_from_physical_action

        for _ in range(self.__number_of_runs):
            self.__test_observation(test_function=test_function)

    def test_observation_coming_from_communicative_action(self) -> None:
        '''
        Tests a `VWObservation` coming from a `VWCommunicativeAction`.
        '''
        test_function: Callable = self.__test_observation_coming_from_communicative_action

        for _ in range(self.__number_of_runs):
            self.__test_observation(test_function=test_function)

    def test_observation_coming_from_multiple_actions(self) -> None:
        '''
        Tests a `VWObservation` coming from a combination of a `VWPhysicalAction` and a `VWCommunicativeAction`.
        '''
        test_function: Callable = self.__test_observation_coming_from_multiple_actions

        for _ in range(self.__number_of_runs):
            self.__test_observation(test_function=test_function)

    def __test_observation(self, test_function: Callable) -> None:
        grid_size: int = randint(self.__min_grid_size, self.__max_grid_size)
        coords: List[VWCoord] = self.__generate_random_coords(grid_size=grid_size)
        actors: List[Optional[VWActorAppearance]] = self.__generate_random_actor_appearances()
        dirts: List[Optional[VWDirtAppearance]] = self.__generate_random_dirt_appearances()
        perceived_locations: Dict[VWPositionNames, VWLocation] = self.__generate_locations_dict(grid_size=grid_size, coords=coords, actors=actors, dirts=dirts)

        test_function(perceived_locations=perceived_locations, coords=coords, actors=actors, dirts=dirts)

        self.__progressive_id = 0

    def __test_observation_coming_from_physical_action(self, perceived_locations: Dict[VWPositionNames, VWLocation], coords: List[VWCoord], actors: List[Optional[VWActorAppearance]], dirts: List[Optional[VWDirtAppearance]]) -> None:
        for action_type in [VWCleanAction, VWDropAction, VWIdleAction, VWMoveAction, VWTurnAction]:
            for action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                self.__test_observation_coming_from_single_action(perceived_locations=perceived_locations, coords=coords, actors=actors, dirts=dirts, action_type=action_type, action_outcome=action_outcome)

    def __test_observation_coming_from_communicative_action(self, perceived_locations: Dict[VWPositionNames, VWLocation], coords: List[VWCoord], actors: List[Optional[VWActorAppearance]], dirts: List[Optional[VWDirtAppearance]]) -> None:
        for action_type in [VWSpeakAction, VWBroadcastAction]:
            for action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                self.__test_observation_coming_from_single_action(perceived_locations=perceived_locations, coords=coords, actors=actors, dirts=dirts, action_type=action_type, action_outcome=action_outcome)

    def __test_observation_coming_from_multiple_actions(self, perceived_locations: Dict[VWPositionNames, VWLocation], coords: List[VWCoord], actors: List[Optional[VWActorAppearance]], dirts: List[Optional[VWDirtAppearance]]) -> None:
        for physical_action_type in [VWCleanAction, VWDropAction, VWIdleAction, VWMoveAction, VWTurnAction]:
            for communicative_action_type in [VWSpeakAction, VWBroadcastAction]:
                for physical_action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                    for communicative_action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                        physical_result: ActionResult = ActionResult(outcome=physical_action_outcome)
                        communicative_result: ActionResult = ActionResult(outcome=communicative_action_outcome)
                        physical_observation: VWObservation = VWObservation(action_type=physical_action_type, action_result=physical_result, locations_dict=perceived_locations)
                        communicative_observation: VWObservation = VWObservation(action_type=communicative_action_type, action_result=communicative_result, locations_dict=perceived_locations)
                        communicative_observation.merge_action_result_with_previous_observations(observations=[physical_observation])

                        self.__check_locations(o=communicative_observation, positions=VWPositionNames.values(), coords=coords, actors=actors, dirts=dirts)

                        actions_outcomes: Dict[Type[VWAction], Union[ActionOutcome, List[ActionOutcome]]] = communicative_observation.get_latest_actions_outcomes_as_dict()

                        self.assertTrue(len(actions_outcomes) == 2)
                        self.assertTrue(physical_action_type.__name__ in actions_outcomes)
                        self.assertTrue(communicative_action_type.__name__ in actions_outcomes)
                        self.assertTrue(isinstance(actions_outcomes[physical_action_type.__name__], ActionOutcome))
                        self.assertTrue(isinstance(actions_outcomes[communicative_action_type.__name__], ActionOutcome))
                        self.assertEqual(physical_action_outcome, actions_outcomes[physical_action_type.__name__])
                        self.assertEqual(communicative_action_outcome, actions_outcomes[communicative_action_type.__name__])

    def __test_observation_coming_from_single_action(self, perceived_locations: Dict[VWPositionNames, VWLocation], coords: List[VWCoord], actors: List[Optional[VWActorAppearance]], dirts: List[Optional[VWDirtAppearance]], action_type: Type[VWAction], action_outcome: ActionOutcome) -> None:
        result: ActionResult = ActionResult(outcome=action_outcome)
        o: VWObservation = VWObservation(action_type=action_type, action_result=result, locations_dict=perceived_locations)

        self.__check_locations(o=o, positions=VWPositionNames.values(), coords=coords, actors=actors, dirts=dirts)

        actions_outcomes: Dict[Type[VWAction], Union[ActionOutcome, List[ActionOutcome]]] = o.get_latest_actions_outcomes_as_dict()

        self.assertTrue(len(actions_outcomes) == 1)
        self.assertTrue(action_type.__name__ in actions_outcomes)

        action_outcomes: Union[ActionOutcome, List[ActionOutcome]] = actions_outcomes[action_type.__name__]

        self.assertTrue(isinstance(action_outcomes, ActionOutcome))
        self.assertEqual(action_outcome, action_outcomes)

    def __check_locations(self, o: VWObservation, positions: List[VWPositionNames], coords: List[VWCoord], actors: List[Optional[VWActorAppearance]], dirts: List[Optional[VWDirtAppearance]]) -> None:
        for i in range(len(positions)):
            self.__check_location(o=o, position=positions[i], coord=coords[i], actor_appearance=actors[i], dirt_appearance=dirts[i])

    def __check_location(self, o: VWObservation, position: VWPositionNames, coord: VWCoord, actor_appearance: Optional[VWActorAppearance], dirt_appearance: Optional[VWDirtAppearance]) -> None:
        self.__check_observer_id(observation=o, position=position, actor_appearance=actor_appearance)

        if o.get_location_at(position_name=position) is not None:
            self.__check_appearances(observation=o, position=position, actor_appearance=actor_appearance, dirt_appearance=dirt_appearance)

    def __check_observer_id(self, observation: VWObservation, position: VWPositionNames, actor_appearance: Optional[VWActorAppearance]) -> None:
        if position == VWPositionNames.center:
            self.assertIsNotNone(observation.get_location_at(position_name=position))
            self.assertIsNotNone(actor_appearance)
            self.assertEqual(actor_appearance.get_id(), observation.get_observer_id())

    def __check_appearances(self, observation: VWObservation, position: VWPositionNames, actor_appearance: Optional[VWActorAppearance], dirt_appearance: Optional[VWDirtAppearance]) -> None:
        if observation.get_location_at(position_name=position) is not None:
            location: VWLocation = observation.get_location_at(position_name=position)

            if actor_appearance is not None:
                self.assertEqual(location.get_actor_appearance(), actor_appearance)
            else:
                self.assertIsNone(location.get_actor_appearance())

            if dirt_appearance is not None:
                self.assertEqual(location.get_dirt_appearance(), dirt_appearance)
            else:
                self.assertIsNone(location.get_dirt_appearance())

    def __generate_random_coords(self, grid_size: int) -> List[VWCoord]:
        return [VWCoord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1)) for _ in range(self.__number_of_locations)]

    def __generate_random_actor_appearances(self) -> List[Optional[VWActorAppearance]]:
        # The `VWLocation` at `PositionNames.center` must always have a `VWActorAppearance` (i.e., the observer) in it.
        # In particular, the first element of this list must be a `VWActorAppearance`.
        return [None if randfloat() < 0.5 and i > 0 else self.__generate_random_actor_appearance() for i in range(self.__number_of_locations)]

    def __generate_random_actor_appearance(self) -> VWActorAppearance:
        actor_id: str = str(uuid4())
        colour: VWColour = choice(list(VWColour))
        orientation: VWOrientation = choice(list(VWOrientation))
        self.__progressive_id += 1

        return VWActorAppearance(actor_id=actor_id, progressive_id=self.__progressive_id, colour=colour, orientation=orientation)

    def __generate_random_dirt_appearances(self) -> List[Optional[VWDirtAppearance]]:
        return [None if randfloat() < 0.5 else self.__generate_random_dirt_appearance() for _ in range(self.__number_of_locations)]

    def __generate_random_dirt_appearance(self) -> VWDirtAppearance:
        dirt_id: str = str(uuid4())
        colour: VWColour = choice(list(VWColour))
        self.__progressive_id += 1

        return VWDirtAppearance(dirt_id=dirt_id, progressive_id=self.__progressive_id, colour=colour)

    def __generate_locations_dict(self, grid_size: int, coords: List[VWCoord], actors: List[Optional[VWActorAppearance]], dirts: List[Optional[VWDirtAppearance]]) -> Dict[VWPositionNames, VWLocation]:
        locations_dict: Dict[VWPositionNames, VWLocation] = {}

        for i in range(len(coords)):
            coord: VWCoord = coords[i]
            locations_dict[VWPositionNames.values()[i]] = VWLocation(coord=coord, actor_appearance=actors[i], dirt_appearance=dirts[i], wall=VWEnvironment.generate_wall_from_coordinates(coord=coord, grid_size=grid_size)) if coord.in_bounds(min_x=0, max_x=grid_size-1, min_y=0, max_y=grid_size-1) else None

        return locations_dict

    def test_message_with_int_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is an `int`.
        '''
        contents: List[int] = [randint(-maxsize + 1, maxsize) for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_float_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is a `float`.
        '''
        contents: List[float] = [randfloat() * float_info.max for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_str_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is a `str`.
        '''
        contents: List[str] = [self.__randbytes(randint(0, 2**16 - 1)).hex() for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_bytes_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is a `bytes` value.
        '''
        contents: List[bytes] = [self.__randbytes(randint(0, 2**16 - 1)) for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_list_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is a `list`.
        '''
        contents: List[List[Union[int, float, str, bytes, list, tuple, dict]]] = [self.__generate_random_list() for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_tuple_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is a `tuple`.
        '''
        contents: List[Tuple[Union[int, float, str, bytes, list, tuple, dict]]] = [self.__generate_random_tuple() for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_dict_content(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content is a `dict`.
        '''
        contents: List[Dict[Union[int, float, str, bytes], Union[int, float, str, bytes, list, tuple, dict]]] = [self.__generate_random_dict() for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_messages_with_recursion(self) -> None:
        '''
        Tests various instances of `BccMessage` whose content contains recursive data structures.
        '''
        for content in (1, 1.32343, "foo", bytes("foobar", "utf-8"), ["foo", 1, 1.234, bytes("foobar", "utf-8"), [], (), {"foo": "bar"}], ("foo", 1, 1.234, [], (), {}, bytes("foobar", "utf-8")), {1: ["", None], 1.2343: (3, 4.5, {})}):
            for sender_id in ("Sephiroth", "Jenova", "Hojo", "Rufus"):
                for recipient_id in ("Cloud", "Barret", "Red XIII", "Cid", "Vincent", "Tifa", "Yuffie", "Cait Sith", "Aerith"):
                    self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_none_top_content(self) -> None:
        self.assertRaises(ValueError, BccMessage, content=None, sender_id="Sephiroth", recipient_id="Cloud")

    def __test_message(self, content: Union[int, float, str, bytes, list, tuple, dict], sender_id: str, recipient_id: str) -> None:
        message: BccMessage = BccMessage(content=content, sender_id=sender_id, recipient_id=recipient_id)

        self.assertEqual(content, message.get_content())
        self.assertEqual(sender_id, message.get_sender_id())
        self.assertEqual(len(message.get_recipients_ids()), 1)
        self.assertIn(recipient_id, message.get_recipients_ids())

    def __generate_random_list(self) -> List[Union[int, float, str, bytes, list, tuple, dict]]:
        return [self.__generate_random_element() for _ in range(randint(0, self.__collection_size))]

    def __generate_random_tuple(self) -> Tuple[Union[int, float, str, bytes, list, tuple, dict]]:
        return tuple(self.__generate_random_element() for _ in range(randint(0, self.__collection_size)))

    def __generate_random_dict(self) -> Dict[Union[int, float, str, bytes], Union[int, float, str, bytes, list, tuple, dict]]:
        return {self.__generate_random_key(): self.__generate_random_element() for _ in range(randint(0, self.__collection_size))}

    def __generate_random_element(self) -> Union[int, float, str, bytes, list, tuple, dict]:
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
            return []  # We want to avoid infinite recursion.
        elif roll < 6:
            return tuple()  # We want to avoid infinite recursion.
        elif roll < 7:
            return {}  # We want to avoid infinite recursion.
        else:
            raise ValueError("Invalid roll")

    def __generate_random_key(self) -> Union[int, float, str, bytes]:
        roll: float = randfloat() * 4

        if roll < 1:
            return randint(-maxsize + 1, maxsize)
        elif roll < 2:
            return randfloat() * float_info.max
        elif roll < 3:
            return self.__randbytes(randint(0, 2**16 - 1)).hex()
        elif roll < 4:
            return self.__randbytes(randint(0, 2**16 - 1))
        else:
            raise ValueError("Invalid roll")


if __name__ == "__main__":
    main()
