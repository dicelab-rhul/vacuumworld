#!/usr/bin/env python3

from unittest import main, TestCase
from typing import List, Tuple, Union
from random import randint

from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome

from vacuumworld.common.coordinates import Coord
from vacuumworld.common.colour import Colour
from vacuumworld.common.direction import Direction
from vacuumworld.common.orientation import Orientation
from vacuumworld.model.actor.user_difficulty import UserDifficulty
from vacuumworld.model.actor.actor_factories import VWCleaningAgentsFactory, VWUsersFactory
from vacuumworld.model.actions.idle_action import VWIdleAction
from vacuumworld.model.actions.speak_action import VWSpeakAction
from vacuumworld.model.actions.turn_action import VWTurnAction
from vacuumworld.model.actions.clean_action import VWCleanAction
from vacuumworld.model.actions.drop_action import VWDropAction
from vacuumworld.model.actions.move_action import VWMoveAction
from vacuumworld.model.actions.broadcast_action import VWBroadcastAction
from vacuumworld.model.actor.vwuser import VWUser
from vacuumworld.model.environment.physics.broadcast_executor import BroadcastExecutor
from vacuumworld.model.environment.physics.clean_executor import CleanExecutor
from vacuumworld.model.environment.physics.drop_executor import DropExecutor
from vacuumworld.model.environment.physics.idle_executor import IdleExecutor
from vacuumworld.model.environment.physics.move_executor import MoveExecutor
from vacuumworld.model.environment.physics.speak_executor import SpeakExecutor
from vacuumworld.model.environment.physics.turn_executor import TurnExecutor
from vacuumworld.model.actor.hystereticmindsurrogate import VWHystereticMindSurrogate
from vacuumworld.model.actor.actor_factories import VWCleaningAgentsFactory, VWUsersFactory
from vacuumworld.model.dirt.dirt_appearance import VWDirtAppearance
from vacuumworld.model.dirt.dirt import Dirt
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.config_manager import ConfigManager

import os


class TestExecutors(TestCase):
    def __init__(self, args) -> None:
        super(TestExecutors, self).__init__(args)

        self.__config_file_name: str = "config.json"
        self.__vw_dir_name: str = "vacuumworld"
        self.__config_file_path: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), self.__vw_dir_name, self.__config_file_name)
        self.__config_manager: ConfigManager = ConfigManager(config_file_path=self.__config_file_path)
        self.__config: dict = self.__config_manager.load_config()
        self.__default_grid_size: int = self.__config["initial_environment_dim"]
        self.__min_grid_size: int = self.__config["min_environment_dim"]
        self.__max_grid_size: int = self.__config["max_environment_dim"]

    def test_idle_action(self) -> None:
        action: VWIdleAction = VWIdleAction()
        idle_executor: IdleExecutor = IdleExecutor()
        env, _ = self.__generate_random_environment(custom_grid_size=True)

        for actor_id in env.get_actors():
            action.set_actor_id(actor_id=actor_id)

            self.assertTrue(idle_executor.is_possible(env=env, action=action))

            result: ActionResult = idle_executor.execute(env=env, action=action)

            self.assertTrue(result.get_outcome() == ActionOutcome.success)
            self.assertTrue(idle_executor.succeeded(env=env, action=action))

    def test_speak_action(self) -> None:
        speak_executor: SpeakExecutor = SpeakExecutor()
        env, _ = self.__generate_random_environment(custom_grid_size=True)

        messages: List[Union[int, float, str, list, tuple, dict]] = [
            "Hello World!",
            ["Hello", "World", "!"],
            {
                "Hello": 5,
                "World": 5,
                "!": 1
            },
            1337,
            0.1337,
            ("Hello", "World", "!")
        ]

        for message in messages:
            for actor_id in env.get_actors():
                action: VWSpeakAction = VWSpeakAction(message=message, sender_id=actor_id, recipients=[a_id for a_id in env.get_actors() if a_id != actor_id])
                action.set_actor_id(actor_id=actor_id)

                self.assertTrue(speak_executor.is_possible(env=env, action=action))

                result: ActionResult = speak_executor.execute(env=env, action=action)

                self.assertTrue(result.get_outcome() == ActionOutcome.success)
                self.assertTrue(speak_executor.succeeded(env=env, action=action))

            for actor_id in env.get_actors():
                action: VWSpeakAction = VWSpeakAction(message=message, sender_id=actor_id, recipients=[])
                action.set_actor_id(actor_id=actor_id)

                self.assertTrue(speak_executor.is_possible(env=env, action=action))

                result: ActionResult = speak_executor.execute(env=env, action=action)

                self.assertTrue(result.get_outcome() == ActionOutcome.success)
                self.assertTrue(speak_executor.succeeded(env=env, action=action))

    def test_broadcast_action(self) -> None:
        broadcast_executor: BroadcastExecutor = BroadcastExecutor()
        env, _ = self.__generate_random_environment(custom_grid_size=True)

        messages: List[Union[int, float, str, list, tuple, dict]] = [
            "Hello World!",
            ["Hello", "World", "!"],
            {
                "Hello": 5,
                "World": 5,
                "!": 1
            },
            1337,
            0.1337,
            ("Hello", "World", "!")
        ]

        for message in messages:
            for actor_id in env.get_actors():
                action: VWBroadcastAction = VWBroadcastAction(message=message, sender_id=actor_id)
                action.set_actor_id(actor_id=actor_id)

                self.assertTrue(broadcast_executor.is_possible(env=env, action=action))

                result: ActionResult = broadcast_executor.execute(env=env, action=action)

                self.assertTrue(result.get_outcome() == ActionOutcome.success)
                self.assertTrue(broadcast_executor.succeeded(env=env, action=action))

    def test_move_action(self) -> None:
        action: VWMoveAction = VWMoveAction()
        move_executor: MoveExecutor = MoveExecutor()
        env, _ = self.__generate_random_environment(custom_grid_size=True)

        for actor_id in env.get_actors():
            action.set_actor_id(actor_id=actor_id)

            actor_position: Coord = env.get_actor_position(actor_id=actor_id)
            orientation: Orientation = env.get_actor_location(actor_id=actor_id).get_actor_appearance().get_orientation()
            forward_position: Coord = actor_position.forward(orientation=orientation)
            actor_location: VWLocation = env.get_actor_location(actor_id=actor_id)

            if forward_position in env.get_ambient().get_grid() and not env.get_ambient().get_grid()[forward_position].has_actor():
                self.assertTrue(move_executor.is_possible(env=env, action=action))

                result: ActionResult = move_executor.execute(env=env, action=action)
                new_location: VWLocation = env.get_actor_location(actor_id=actor_id)

                if new_location.get_coord() == forward_position and self.__actor_on_location(location=new_location, actor_id=actor_id, orientation=orientation) and not self.__actor_on_location(location=actor_location, actor_id=actor_id, orientation=orientation):
                    self.assertTrue(result.get_outcome() == ActionOutcome.success)
                    self.assertTrue(move_executor.succeeded(env=env, action=action))
                else:
                    self.assertTrue(result.get_outcome() == ActionOutcome.failure)
                    self.assertFalse(move_executor.succeeded(env=env, action=action))
            else:
                self.assertFalse(move_executor.is_possible(env=env, action=action))

    def __actor_on_location(self, location: VWLocation, actor_id: str, orientation: Orientation) -> bool:
        if not location.has_actor():
            return False

        if location.get_actor_appearance().get_id() != actor_id:
            return False

        return location.get_actor_appearance().get_orientation() == orientation

    def test_turn_action(self) -> None:
        left_turn_action: VWTurnAction = VWTurnAction(Direction.left)
        right_turn_action: VWTurnAction = VWTurnAction(Direction.right)
        turn_executor: TurnExecutor = TurnExecutor()
        env, _ = self.__generate_random_environment(custom_grid_size=True)

        for actor_id, actor in env.get_actors().items():
            left_turn_action.set_actor_id(actor_id=actor_id)

            old_orientation: Orientation = env.get_actor_location(actor_id=actor_id).get_actor_appearance().get_orientation()

            self.assertTrue(turn_executor.is_possible(env=env, action=left_turn_action))

            result: ActionResult = turn_executor.execute(env=env, action=left_turn_action)

            self.assertTrue(result.get_outcome() == ActionOutcome.success)
            self.assertTrue(turn_executor.succeeded(env=env, action=left_turn_action))
            self.assertEqual(env.get_actor_location(actor_id=actor_id).get_actor_appearance().get_orientation(), old_orientation.get_left())
            self.assertEqual(env.get_actor_location(actor_id=actor_id).get_actor_appearance().get_previous_orientation(), old_orientation)

        for actor_id in env.get_actors():
            right_turn_action.set_actor_id(actor_id=actor_id)

            old_orientation: Orientation = env.get_actor_location(actor_id=actor_id).get_actor_appearance().get_orientation()

            self.assertTrue(turn_executor.is_possible(env=env, action=right_turn_action))

            result: ActionResult = turn_executor.execute(env=env, action=right_turn_action)

            self.assertTrue(result.get_outcome() == ActionOutcome.success)
            self.assertTrue(turn_executor.succeeded(env=env, action=right_turn_action))
            self.assertEqual(env.get_actor_location(actor_id=actor_id).get_actor_appearance().get_orientation(), old_orientation.get_right())
            self.assertEqual(env.get_actor_location(actor_id=actor_id).get_actor_appearance().get_previous_orientation(), old_orientation)

    def test_clean_action(self) -> None:
        action: VWCleanAction = VWCleanAction()
        clean_executor: CleanExecutor = CleanExecutor()
        env, _ = self.__generate_random_environment(custom_grid_size=True)

        for actor_id in env.get_actors():
            action.set_actor_id(actor_id=actor_id)

            dirt_appearance: VWDirtAppearance = env.get_actor_location(actor_id=actor_id).get_dirt_appearance()
            actor_colour: Colour = env.get_actor_location(actor_id=actor_id).get_actor_appearance().get_colour()

            if dirt_appearance and (actor_colour == dirt_appearance.get_colour() or actor_colour == Colour.white):
                self.assertTrue(clean_executor.is_possible(env=env, action=action))

                result: ActionResult = clean_executor.execute(env=env, action=action)

                self.assertTrue(result.get_outcome() == ActionOutcome.success)
                self.assertTrue(clean_executor.succeeded(env=env, action=action))
            else:
                self.assertFalse(clean_executor.is_possible(env=env, action=action))

    def test_drop_action(self) -> None:
        drop_green_dirt_action: VWDropAction = VWDropAction(dirt_colour=Colour.green)
        drop_orange_dirt_action: VWDropAction = VWDropAction(dirt_colour=Colour.orange)
        drop_executor: DropExecutor = DropExecutor()
        env, _ = self.__generate_random_environment(custom_grid_size=True)

        for actor_id, actor in env.get_actors().items():
            drop_green_dirt_action.set_actor_id(actor_id=actor_id)

            if isinstance(actor, VWUser) and not env.get_actor_location(actor_id=actor_id).has_dirt():
                self.assertTrue(drop_executor.is_possible(env=env, action=drop_green_dirt_action))

                result: ActionResult = drop_executor.execute(env=env, action=drop_green_dirt_action)

                self.assertTrue(result.get_outcome() == ActionOutcome.success)
                self.assertTrue(drop_executor.succeeded(env=env, action=drop_green_dirt_action))
            else:
                self.assertFalse(drop_executor.is_possible(env=env, action=drop_green_dirt_action))

        env, _ = self.__generate_random_environment(custom_grid_size=True)

        for actor_id, actor in env.get_actors().items():
            drop_orange_dirt_action.set_actor_id(actor_id=actor_id)

            if isinstance(actor, VWUser) and not env.get_actor_location(actor_id=actor_id).has_dirt():
                self.assertTrue(drop_executor.is_possible(env=env, action=drop_orange_dirt_action))

                result: ActionResult = drop_executor.execute(env=env, action=drop_orange_dirt_action)

                self.assertTrue(result.get_outcome() == ActionOutcome.success)
                self.assertTrue(drop_executor.succeeded(env=env, action=drop_orange_dirt_action))
            else:
                self.assertFalse(drop_executor.is_possible(env=env, action=drop_orange_dirt_action))

    def __generate_random_environment(self, custom_grid_size: bool) -> Tuple[VWEnvironment, int]:
        green_agent_orientation: Orientation = Orientation.random()
        orange_agent_orientation: Orientation = Orientation.random()
        white_agent_orientation: Orientation = Orientation.random()
        user_orientation: Orientation = Orientation.random()
        difficutly_level: UserDifficulty = UserDifficulty.random()

        green_agent, green_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=Colour.green, orientation=green_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        orange_agent, orange_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=Colour.orange, orientation=orange_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        white_agent, white_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=Colour.white, orientation=white_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        user, user_appearance = VWUsersFactory.create_user(difficulty_level=difficutly_level, orientation=user_orientation)

        green_dirt: Dirt = Dirt(colour=Colour.green)
        green_dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=green_dirt.get_id(), progressive_id=green_dirt.get_progressive_id(), colour=Colour.green)

        orange_dirt: Dirt = Dirt(colour=Colour.orange)
        orange_dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=orange_dirt.get_id(), progressive_id=orange_dirt.get_progressive_id(), colour=Colour.orange)

        env, grid_size = self.__generate_empty_env(custom_grid_size=custom_grid_size)

        env.add_actor(actor=green_agent)
        env.add_actor(actor=orange_agent)
        env.add_actor(actor=white_agent)
        env.add_actor(actor=user)
        env.add_passive_body(passive_body=green_dirt)
        env.add_passive_body(passive_body=orange_dirt)

        green_agent_coord, orange_agent_coord, white_agent_coord, user_coord = self.__generate_mutually_exclusive_coordinates(amount=4, grid_size=grid_size)
        green_dirt_coord, orange_dirt_coord = self.__generate_mutually_exclusive_coordinates(amount=2, grid_size=grid_size)

        env.get_ambient().get_grid()[green_agent_coord] = VWLocation(coord=green_agent_coord, actor_appearance=green_agent_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=green_agent_coord, grid_size=grid_size))
        env.get_ambient().get_grid()[orange_agent_coord] = VWLocation(coord=orange_agent_coord, actor_appearance=orange_agent_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=orange_agent_coord, grid_size=grid_size))
        env.get_ambient().get_grid()[white_agent_coord] = VWLocation(coord=white_agent_coord, actor_appearance=white_agent_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=white_agent_coord, grid_size=grid_size))
        env.get_ambient().get_grid()[user_coord] = VWLocation(coord=user_coord, actor_appearance=user_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=user_coord, grid_size=grid_size))

        if green_dirt_coord in env.get_ambient().get_grid():
            env.get_ambient().get_grid()[green_dirt_coord].add_dirt(dirt_appearance=green_dirt_appearance)
        else:
            env.get_ambient().get_grid()[green_dirt_coord] = VWLocation(coord=green_dirt_coord, dirt_appearance=green_dirt_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=green_dirt_coord, grid_size=grid_size))

        if orange_dirt_coord in env.get_ambient().get_grid():
            env.get_ambient().get_grid()[orange_dirt_coord].add_dirt(dirt_appearance=orange_dirt_appearance)
        else:
            env.get_ambient().get_grid()[orange_dirt_coord] = VWLocation(coord=orange_dirt_coord, dirt_appearance=orange_dirt_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=orange_dirt_coord, grid_size=grid_size))

        return env, grid_size

    def __generate_empty_env(self, custom_grid_size: bool) -> Tuple[VWEnvironment, int]:
        if custom_grid_size:
            grid_size: int = randint(self.__min_grid_size, self.__max_grid_size)
            return VWEnvironment.generate_empty_env(config=self.__config, forced_line_dim=grid_size), grid_size
        else:
            grid_size: int = self.__default_grid_size
            return VWEnvironment.generate_empty_env(config=self.__config), grid_size

    def __generate_mutually_exclusive_coordinates(self, amount: int, grid_size: int) -> List[Coord]:
        assert amount > 1

        coords: List[Coord] = [Coord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1))]

        for _ in range(amount - 1):
            tmp: Coord = Coord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1))

            while tmp in coords:
                tmp = Coord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1))

            coords.append(tmp)

        return coords

if __name__ == '__main__':
    main()
