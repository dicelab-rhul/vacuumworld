#!/usr/bin/env python3

from unittest import main, TestCase
from typing import Dict, Optional
from random import randint

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.common.action_result import ActionResult

from vacuumworld.common.position_names import PositionNames
from vacuumworld.model.actions.idle_action import VWIdleAction
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

        self.__config_file_name: str = "config.json"
        self.__vw_dir_name: str = "vacuumworld"
        self.__config_file_path: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), self.__vw_dir_name, self.__config_file_name)
        self.__config_manager: ConfigManager = ConfigManager(config_file_path=self.__config_file_path)
        self.__config: dict = self.__config_manager.load_config()
        self.__min_grid_size: int = self.__config["min_environment_dim"]
        self.__max_grid_size: int = self.__config["max_environment_dim"]

    def test_observation(self) -> None:
        for _ in range(100):
            grid_size: int = randint(self.__min_grid_size, self.__max_grid_size)

            a1: VWActorAppearance = VWActorAppearance(actor_id="foo", progressive_id="1", colour=Colour.green, orientation=Orientation.east)
            a2: VWActorAppearance = VWActorAppearance(actor_id="bar", progressive_id="2", colour=Colour.orange, orientation=Orientation.north)
            u1: VWActorAppearance = VWActorAppearance(actor_id="foobar", progressive_id="3", colour=Colour.user, orientation=Orientation.west)
            u2: VWActorAppearance = VWActorAppearance(actor_id="barfoo", progressive_id="4", colour=Colour.user, orientation=Orientation.south)
            d1: VWDirtAppearance = VWDirtAppearance(dirt_id="running", progressive_id="5", colour=Colour.green)
            d2: VWDirtAppearance = VWDirtAppearance(dirt_id="out_of", progressive_id="6", colour=Colour.orange)
            d3: VWDirtAppearance = VWDirtAppearance(dirt_id="ideas", progressive_id="7", colour=Colour.orange)

            c: Coord = Coord(x=randint(0, self.__max_grid_size-1), y=randint(0, self.__max_grid_size-1))
            f: Coord = c.forward(orientation=a1.get_orientation())
            l: Coord = c.left(orientation=a1.get_orientation())
            r: Coord = c.right(orientation=a1.get_orientation())
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

            for action_outcome in (ActionOutcome.impossible, ActionOutcome.success, ActionOutcome.failure):
                result: ActionResult = ActionResult(outcome=action_outcome)
                o: Observation = Observation(action_type=VWIdleAction, action_result=result, locations_dict=perceived_locations)

                self.__check_location(o=o, position=PositionNames.center, coord=c, actor_appearance=a1, dirt_appearance=None)
                self.__check_location(o=o, position=PositionNames.left, coord=l, actor_appearance=None, dirt_appearance=None)
                self.__check_location(o=o, position=PositionNames.right, coord=r, actor_appearance=a2, dirt_appearance=d1)
                self.__check_location(o=o, position=PositionNames.forward, coord=f, actor_appearance=None, dirt_appearance=d2)
                self.__check_location(o=o, position=PositionNames.forwardleft, coord=fl, actor_appearance=u1, dirt_appearance=None)
                self.__check_location(o=o, position=PositionNames.forwardright, coord=fr, actor_appearance=u2, dirt_appearance=d3)

    def __check_location(self, o: Observation, position: PositionNames, coord: Coord, actor_appearance: Optional[VWActorAppearance], dirt_appearance: Optional[VWDirtAppearance]) -> None:
        if o.get_location_at(position_name=position) is not None:
            location: VWLocation = o.get_location_at(position_name=position)

            self.assertEqual(location.get_coord(), coord)
            self.assertEqual(location.get_actor_appearance(), actor_appearance)
            self.assertEqual(location.get_dirt_appearance(), dirt_appearance)

    def test_message(self) -> None:
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
