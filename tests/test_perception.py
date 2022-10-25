#!/usr/bin/env python3

from unittest import main, TestCase
from typing import Dict, Optional, List, Union, Type, Callable, Tuple
from random import choice, randint, random as randfloat
from uuid import uuid4
from sys import maxsize, float_info

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.common.action_result import ActionResult

from vacuumworld.common.position_names import PositionNames
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.broadcast_action import VWBroadcastAction
from vacuumworld.model.actions.clean_action import VWCleanAction
from vacuumworld.model.actions.drop_action import VWDropAction
from vacuumworld.model.actions.idle_action import VWIdleAction
from vacuumworld.model.actions.move_action import VWMoveAction
from vacuumworld.model.actions.speak_action import VWSpeakAction
from vacuumworld.model.actions.turn_action import VWTurnAction
from vacuumworld.model.dirt.dirt_appearance import VWDirtAppearance
from vacuumworld.common.orientation import Orientation
from vacuumworld.common.colour import Colour
from vacuumworld.model.actor.vwactor_appearance import VWActorAppearance
from vacuumworld.common.coordinates import Coord
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.common.observation import Observation
from vacuumworld.config_manager import ConfigManager

import os
import sys


if sys.version_info.major == 3 and sys.version_info.minor > 8:
    from random import randbytes
elif sys.version_info.major == 3 and sys.version_info.minor == 8:
    randbytes = os.urandom
else:
    raise RuntimeError("Python version not supported (too old): {}.{}.{}.".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))


class TestPerception(TestCase):
    def __init__(self, args) -> None:
        super(TestPerception, self).__init__(args)

        self.__config_file_path: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vacuumworld", "config.json")
        self.__config: dict = ConfigManager(config_file_path=self.__config_file_path).load_config()
        self.__min_grid_size: int = self.__config["min_environment_dim"]
        self.__max_grid_size: int = self.__config["max_environment_dim"]
        self.__number_of_locations: int = len(PositionNames)
        self.__progressive_id: int = 0
        self.__number_of_runs: int = 100
        self.__collection_size: int = 100

    def test_observation_coming_from_physical_action(self) -> None:
        test_function: Callable = self.__test_observation_coming_from_physical_action

        for _ in range(self.__number_of_runs):
            self.__test_observation(test_function=test_function)

    def test_observation_coming_from_communicative_action(self) -> None:
        test_function: Callable = self.__test_observation_coming_from_communicative_action

        for _ in range(self.__number_of_runs):
            self.__test_observation(test_function=test_function)

    def test_observation_coming_from_multiple_actions(self) -> None:
        test_function: Callable = self.__test_observation_coming_from_multiple_actions

        for _ in range(self.__number_of_runs):
            self.__test_observation(test_function=test_function)

    def __test_observation(self, test_function: Callable) -> None:
        grid_size: int = randint(self.__min_grid_size, self.__max_grid_size)
        coords: List[Coord] = self.__generate_random_coords(grid_size=grid_size)
        actors: List[Optional[VWActorAppearance]] = self.__generate_random_actor_appearances()
        dirts: List[Optional[VWDirtAppearance]] = self.__generate_random_dirt_appearances()
        perceived_locations: Dict[PositionNames, VWLocation] = self.__generate_locations_dict(grid_size=grid_size, coords=coords, actors=actors, dirts=dirts)

        test_function(perceived_locations=perceived_locations, coords=coords, actors=actors, dirts=dirts)

        self.__progressive_id = 0

    def __test_observation_coming_from_physical_action(self, perceived_locations: Dict[PositionNames, VWLocation], coords: List[Coord], actors: List[Optional[VWActorAppearance]], dirts: List[Optional[VWDirtAppearance]]) -> None:
        for action_type in [VWCleanAction, VWDropAction, VWIdleAction, VWMoveAction, VWTurnAction]:
            for action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                self.__test_observation_coming_from_single_action(perceived_locations=perceived_locations, coords=coords, actors=actors, dirts=dirts, action_type=action_type, action_outcome=action_outcome)

    def __test_observation_coming_from_communicative_action(self, perceived_locations: Dict[PositionNames, VWLocation], coords: List[Coord], actors: List[Optional[VWActorAppearance]], dirts: List[Optional[VWDirtAppearance]]) -> None:
        for action_type in [VWSpeakAction, VWBroadcastAction]:
            for action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                self.__test_observation_coming_from_single_action(perceived_locations=perceived_locations, coords=coords, actors=actors, dirts=dirts, action_type=action_type, action_outcome=action_outcome)

    def __test_observation_coming_from_multiple_actions(self, perceived_locations: Dict[PositionNames, VWLocation], coords: List[Coord], actors: List[Optional[VWActorAppearance]], dirts: List[Optional[VWDirtAppearance]]) -> None:
        for physical_action_type in [VWCleanAction, VWDropAction, VWIdleAction, VWMoveAction, VWTurnAction]:
            for communicative_action_type in [VWSpeakAction, VWBroadcastAction]:
                for physical_action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                    for communicative_action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                        physical_result: ActionResult = ActionResult(outcome=physical_action_outcome)
                        communicative_result: ActionResult = ActionResult(outcome=communicative_action_outcome)
                        physical_observation: Observation = Observation(action_type=physical_action_type, action_result=physical_result, locations_dict=perceived_locations)
                        communicative_observation: Observation = Observation(action_type=communicative_action_type, action_result=communicative_result, locations_dict=perceived_locations)
                        communicative_observation.merge_action_result_with_previous_observations(observations=[physical_observation])

                        self.__check_locations(o=communicative_observation, positions=PositionNames.values(), coords=coords, actors=actors, dirts=dirts)

                        actions_outcomes: Dict[Type[VWAction], Union[ActionOutcome, List[ActionOutcome]]] = communicative_observation.get_latest_actions_outcomes_as_dict()

                        self.assertTrue(len(actions_outcomes) == 2)
                        self.assertTrue(physical_action_type.__name__ in actions_outcomes)
                        self.assertTrue(communicative_action_type.__name__ in actions_outcomes)
                        self.assertTrue(isinstance(actions_outcomes[physical_action_type.__name__], ActionOutcome))
                        self.assertTrue(isinstance(actions_outcomes[communicative_action_type.__name__], ActionOutcome))
                        self.assertEqual(physical_action_outcome, actions_outcomes[physical_action_type.__name__])
                        self.assertEqual(communicative_action_outcome, actions_outcomes[communicative_action_type.__name__])

    def __test_observation_coming_from_single_action(self, perceived_locations: Dict[PositionNames, VWLocation], coords: List[Coord], actors: List[Optional[VWActorAppearance]], dirts: List[Optional[VWDirtAppearance]], action_type: Type[VWAction], action_outcome: ActionOutcome) -> None:
        result: ActionResult = ActionResult(outcome=action_outcome)
        o: Observation = Observation(action_type=action_type, action_result=result, locations_dict=perceived_locations)

        self.__check_locations(o=o, positions=PositionNames.values(), coords=coords, actors=actors, dirts=dirts)

        actions_outcomes: Dict[Type[VWAction], Union[ActionOutcome, List[ActionOutcome]]] = o.get_latest_actions_outcomes_as_dict()

        self.assertTrue(len(actions_outcomes) == 1)
        self.assertTrue(action_type.__name__ in actions_outcomes)

        action_outcomes: Union[ActionOutcome, List[ActionOutcome]] = actions_outcomes[action_type.__name__]

        self.assertTrue(isinstance(action_outcomes, ActionOutcome))
        self.assertEqual(action_outcome, action_outcomes)

    def __check_locations(self, o: Observation, positions: List[PositionNames], coords: List[Coord], actors: List[Optional[VWActorAppearance]], dirts: List[Optional[VWDirtAppearance]]) -> None:
        for i in range(len(positions)):
            self.__check_location(o=o, position=positions[i], coord=coords[i], actor_appearance=actors[i], dirt_appearance=dirts[i])

    def __check_location(self, o: Observation, position: PositionNames, coord: Coord, actor_appearance: Optional[VWActorAppearance], dirt_appearance: Optional[VWDirtAppearance]) -> None:
        if o.get_location_at(position_name=position) is not None:
            location: VWLocation = o.get_location_at(position_name=position)

            self.assertEqual(location.get_coord(), coord)

            if actor_appearance is not None:
                self.assertEqual(location.get_actor_appearance(), actor_appearance)
            else:
                self.assertIsNone(location.get_actor_appearance())

            if dirt_appearance is not None:
                self.assertEqual(location.get_dirt_appearance(), dirt_appearance)
            else:
                self.assertIsNone(location.get_dirt_appearance())

    def __generate_random_coords(self, grid_size: int) -> List[Coord]:
        return [Coord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1)) for _ in range(self.__number_of_locations)]

    def __generate_random_actor_appearances(self) -> List[Optional[VWActorAppearance]]:
        return [None if randfloat() < 0.5 else self.__generate_random_actor_appearance() for _ in range(self.__number_of_locations)]

    def __generate_random_actor_appearance(self) -> VWActorAppearance:
        actor_id: str = str(uuid4())
        colour: Colour = choice(list(Colour))
        orientation: Orientation = choice(list(Orientation))
        self.__progressive_id += 1

        return VWActorAppearance(actor_id=actor_id, progressive_id=self.__progressive_id, colour=colour, orientation=orientation)

    def __generate_random_dirt_appearances(self) -> List[Optional[VWDirtAppearance]]:
        return [None if randfloat() < 0.5 else self.__generate_random_dirt_appearance() for _ in range(self.__number_of_locations)]

    def __generate_random_dirt_appearance(self) -> VWDirtAppearance:
        dirt_id: str = str(uuid4())
        colour: Colour = choice(list(Colour))
        self.__progressive_id += 1

        return VWDirtAppearance(dirt_id=dirt_id, progressive_id=self.__progressive_id, colour=colour)

    def __generate_locations_dict(self, grid_size: int, coords: List[Coord], actors: List[Optional[VWActorAppearance]], dirts: List[Optional[VWDirtAppearance]]) -> Dict[PositionNames, VWLocation]:
        locations_dict: Dict[PositionNames, VWLocation] = {}

        for i in range(len(coords)):
            coord: Coord = coords[i]
            locations_dict[PositionNames.values()[i]] = VWLocation(coord=coord, actor_appearance=actors[i], dirt_appearance=dirts[i], wall=VWEnvironment.generate_wall_from_coordinates(coord=coord, grid_size=grid_size)) if coord.in_bounds(min_x=0, max_x=grid_size-1, min_y=0, max_y=grid_size-1) else None

        return locations_dict

    def test_message_with_int_content(self) -> None:
        contents: List[int] = [randint(-maxsize + 1, maxsize) for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_float_content(self) -> None:
        contents: List[float] = [randfloat() * float_info.max for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_str_content(self) -> None:
        contents: List[str] = [randbytes(randint(0, 2**16 - 1)).hex() for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_list_content(self) -> None:
        contents: List[List[Union[int, float, str, list, tuple, dict]]] = [self.__generate_random_list() for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_tuple_content(self) -> None:
        contents: List[Tuple[Union[int, float, str, list, tuple, dict]]] = [self.__generate_random_tuple() for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_message_with_dict_content(self) -> None:
        contents: List[Dict[Union[int, float, str], Union[int, float, str, list, tuple, dict]]] = [self.__generate_random_dict() for _ in range(self.__number_of_runs)]

        for content in contents:
            sender_id: str = str(uuid4())
            recipient_id: str = str(uuid4())

            self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def test_messages_with_recursion(self) -> None:
        for content in (1, 1.32343, "foo", ["foo", 1, 1.234, [], (), {"foo": "bar"}], ("foo", 1, 1.234, [], (), {}), {1: ["", None], 1.2343: (3, 4.5, {})}):
            for sender_id in ("Sephiroth", "Jenova", "Hojo", "Rufus"):
                for recipient_id in ("Cloud", "Barret", "Red XIII", "Cid", "Vincent", "Tifa", "Yuffie", "Cait Sith", "Aerith"):
                    self.__test_message(content=content, sender_id=sender_id, recipient_id=recipient_id)

    def __test_message(self, content: Union[int, float, str, list, tuple, dict], sender_id: str, recipient_id: str) -> None:
        message: BccMessage = BccMessage(content=content, sender_id=sender_id, recipient_id=recipient_id)

        self.assertEqual(content, message.get_content())
        self.assertEqual(sender_id, message.get_sender_id())
        self.assertEqual(len(message.get_recipients_ids()), 1)
        self.assertIn(recipient_id, message.get_recipients_ids())

    def __generate_random_list(self) -> List[Union[int, float, str, list, tuple, dict]]:
        return [self.__generate_random_element() for _ in range(randint(0, self.__collection_size))]

    def __generate_random_tuple(self) -> Tuple[Union[int, float, str, list, tuple, dict]]:
        return tuple(self.__generate_random_element() for _ in range(randint(0, self.__collection_size)))

    def __generate_random_dict(self) -> Dict[Union[int, float, str], Union[int, float, str, list, tuple, dict]]:
        return {self.__generate_random_key(): self.__generate_random_element() for _ in range(randint(0, self.__collection_size))}

    def __generate_random_element(self) -> Union[int, float, str, list, tuple, dict]:
        roll: float = randfloat() * 6

        if roll < 1:
            return randint(-maxsize + 1, maxsize)
        elif roll < 2:
            return randfloat() * float_info.max
        elif roll < 3:
            return randbytes(randint(0, 2**16 - 1)).hex()
        elif roll < 4:
            return []  # We want to avoid infinite recursion.
        elif roll < 5:
            return tuple()  # We want to avoid infinite recursion.
        elif roll < 6:
            return {}  # We want to avoid infinite recursion.
        else:
            raise ValueError("Invalid roll")

    def __generate_random_key(self) -> Union[int, float, str]:
        roll: float = randfloat() * 3

        if roll < 1:
            return randint(-maxsize + 1, maxsize)
        elif roll < 2:
            return randfloat() * float_info.max
        elif roll < 3:
            return randbytes(randint(0, 2**16 - 1)).hex()
        else:
            raise ValueError("Invalid roll")


if __name__ == "__main__":
    main()
