#!/usr/bin/env python3

from unittest import main, TestCase
from typing import Dict, Optional, List, Union, Type
from random import randint

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


class TestPerception(TestCase):
    def __init__(self, args) -> None:
        super(TestPerception, self).__init__(args)

        self.__config_file_path: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vacuumworld", "config.json")
        self.__config: dict = ConfigManager(config_file_path=self.__config_file_path).load_config()
        self.__min_grid_size: int = self.__config["min_environment_dim"]
        self.__max_grid_size: int = self.__config["max_environment_dim"]

    def test_observation(self) -> None:
        for _ in range(100):
            self.__test_observation()

    def __test_observation(self) -> None:
        grid_size: int = randint(self.__min_grid_size, self.__max_grid_size)

        a1: VWActorAppearance = VWActorAppearance(actor_id="foo", progressive_id="1", colour=Colour.green, orientation=Orientation.east)
        a2: VWActorAppearance = VWActorAppearance(actor_id="bar", progressive_id="2", colour=Colour.orange, orientation=Orientation.north)
        u1: VWActorAppearance = VWActorAppearance(actor_id="foobar", progressive_id="3", colour=Colour.user, orientation=Orientation.west)
        u2: VWActorAppearance = VWActorAppearance(actor_id="barfoo", progressive_id="4", colour=Colour.user, orientation=Orientation.south)
        d1: VWDirtAppearance = VWDirtAppearance(dirt_id="running", progressive_id="5", colour=Colour.green)
        d2: VWDirtAppearance = VWDirtAppearance(dirt_id="out_of", progressive_id="6", colour=Colour.orange)
        d3: VWDirtAppearance = VWDirtAppearance(dirt_id="ideas", progressive_id="7", colour=Colour.orange)

        c: Coord = Coord(x=randint(0, self.__max_grid_size-1), y=randint(0, self.__max_grid_size-1))
        l: Coord = c.left(orientation=a1.get_orientation())
        r: Coord = c.right(orientation=a1.get_orientation())
        f: Coord = c.forward(orientation=a1.get_orientation())
        fl: Coord = c.forwardleft(orientation=a1.get_orientation())
        fr: Coord = c.forwardright(orientation=a1.get_orientation())

        center: VWLocation = VWLocation(coord=c, actor_appearance=a1, dirt_appearance=None, wall=VWEnvironment.generate_wall_from_coordinates(coord=c, grid_size=grid_size))
        left: VWLocation = VWLocation(coord=l, actor_appearance=None, dirt_appearance=None, wall=VWEnvironment.generate_wall_from_coordinates(coord=l, grid_size=grid_size))
        right: VWLocation = VWLocation(coord=r, actor_appearance=a2, dirt_appearance=d1, wall=VWEnvironment.generate_wall_from_coordinates(coord=r, grid_size=grid_size))
        forward: VWLocation = VWLocation(coord=f, actor_appearance=None, dirt_appearance=d2, wall=VWEnvironment.generate_wall_from_coordinates(coord=f, grid_size=grid_size))
        forwardleft: VWLocation = VWLocation(coord=fl, actor_appearance=u1, dirt_appearance=None, wall=VWEnvironment.generate_wall_from_coordinates(coord=fl, grid_size=grid_size))
        forwardright: VWLocation = VWLocation(coord=fr, actor_appearance=u2, dirt_appearance=d3, wall=VWEnvironment.generate_wall_from_coordinates(coord=fr, grid_size=grid_size))

        perceived_locations: Dict[PositionNames, VWLocation] = {
            PositionNames.center: center.deep_copy() if c.in_bounds(min_x=0, max_x=grid_size-1, min_y=0, max_y=grid_size-1) else None,
            PositionNames.left: left.deep_copy() if l.in_bounds(min_x=0, max_x=grid_size-1, min_y=0, max_y=grid_size-1) else None,
            PositionNames.right: right.deep_copy() if r.in_bounds(min_x=0, max_x=grid_size-1, min_y=0, max_y=grid_size-1) else None,
            PositionNames.forward: forward.deep_copy() if f.in_bounds(min_x=0, max_x=grid_size-1, min_y=0, max_y=grid_size-1) else None,
            PositionNames.forwardleft: forwardleft.deep_copy() if fl.in_bounds(min_x=0, max_x=grid_size-1, min_y=0, max_y=grid_size-1) else None,
            PositionNames.forwardright: forwardright.deep_copy() if fr.in_bounds(min_x=0, max_x=grid_size-1, min_y=0, max_y=grid_size-1) else None
        }

        self.__test_observation_coming_from_physical_action(perceived_locations=perceived_locations, coords=[c, l, r, f, fl, fr], actors=[a1, None, a2, None, u1, u2], dirts=[None, None, d1, d2, None, d3])
        self.__test_observation_coming_from_communicative_action(perceived_locations=perceived_locations, coords=[c, l, r, f, fl, fr], actors=[a1, None, a2, None, u1, u2], dirts=[None, None, d1, d2, None, d3])
        self.__test_observation_coming_from_multiple_actions(perceived_locations=perceived_locations, coords=[c, l, r, f, fl, fr], actors=[a1, None, a2, None, u1, u2], dirts=[None, None, d1, d2, None, d3])

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

    def test_messages(self) -> None:
        for content in (1, 1.32343, "foo", ["foo", 1, 1.234, [], (), {}], ("foo", 1, 1.234, [], (), {}), {1: ["", None], 1.2343: (3, 4.5)}):
            for sender in ("U", "N", "OWEN"):
                for recipient in ("Cloud", "Barret", "Red XIII", "Cid", "Vincent", "Tifa", "Yuffie", "Cait Sith", "Aerith"):
                    message: BccMessage = BccMessage(content=content, sender_id=sender, recipient_id=recipient)

                    self.assertEqual(content, message.get_content())
                    self.assertEqual(sender, message.get_sender_id())
                    self.assertEqual(len(message.get_recipients_ids()), 1)
                    self.assertIn(recipient, message.get_recipients_ids())


if __name__ == "__main__":
    main()
