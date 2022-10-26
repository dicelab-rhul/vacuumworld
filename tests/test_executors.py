#!/usr/bin/env python3

from unittest import main, TestCase
from typing import List, Union
from random import randint

from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome

from vacuumworld import VacuumWorld
from vacuumworld.common.coordinates import Coord
from vacuumworld.common.colour import Colour
from vacuumworld.common.direction import Direction
from vacuumworld.common.orientation import Orientation
from vacuumworld.model.actions.idle_action import VWIdleAction
from vacuumworld.model.actions.speak_action import VWSpeakAction
from vacuumworld.model.actions.turn_action import VWTurnAction
from vacuumworld.model.actions.clean_action import VWCleanAction
from vacuumworld.model.actions.drop_action import VWDropAction
from vacuumworld.model.actions.move_action import VWMoveAction
from vacuumworld.model.actions.broadcast_action import VWBroadcastAction
from vacuumworld.model.actions.vwactions import VWCommunicativeAction
from vacuumworld.model.actor.vwuser import VWUser
from vacuumworld.model.environment.physics.broadcast_executor import BroadcastExecutor
from vacuumworld.model.environment.physics.clean_executor import CleanExecutor
from vacuumworld.model.environment.physics.drop_executor import DropExecutor
from vacuumworld.model.environment.physics.idle_executor import IdleExecutor
from vacuumworld.model.environment.physics.move_executor import MoveExecutor
from vacuumworld.model.environment.physics.speak_executor import SpeakExecutor
from vacuumworld.model.environment.physics.turn_executor import TurnExecutor
from vacuumworld.model.dirt.dirt_appearance import VWDirtAppearance
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.config_manager import ConfigManager

import os
import sys


if sys.version_info.major == 3 and sys.version_info.minor > 8:
    from random import randbytes
elif sys.version_info.major == 3 and sys.version_info.minor == 8:
    randbytes = os.urandom
else:
    raise RuntimeError("Python version not supported (too old): {}.{}.{}.".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))


class TestExecutors(TestCase):
    def __init__(self, args) -> None:
        super(TestExecutors, self).__init__(args)

        self.__config: dict = ConfigManager(config_file_path=VacuumWorld.CONFIG_FILE_PATH).load_config()

        VWCommunicativeAction.SENDER_ID_SPOOFING_ALLOWED = self.__config["sender_id_spoofing_allowed"]

    def test_idle_action(self) -> None:
        action: VWIdleAction = VWIdleAction()
        idle_executor: IdleExecutor = IdleExecutor()
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

        for actor_id in env.get_actors():
            action.set_actor_id(actor_id=actor_id)

            self.assertTrue(idle_executor.is_possible(env=env, action=action))

            result: ActionResult = idle_executor.execute(env=env, action=action)

            self.assertTrue(result.get_outcome() == ActionOutcome.success)
            self.assertTrue(idle_executor.succeeded(env=env, action=action))

    def test_speak_action(self) -> None:
        self.__test_speak_action()

    def test_speak_action_with_sender_id_spoofing(self) -> None:
        custom_sender_id: str = randbytes(randint(1, 16)).hex()
        self.__test_speak_action(custom_sender_id=custom_sender_id)

    def __test_speak_action(self, custom_sender_id: str=None) -> None:
        speak_executor: SpeakExecutor = SpeakExecutor()
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

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
                self.__test_with_recipients(speak_executor=speak_executor, env=env, message=message, actor_id=actor_id, custom_sender_id=custom_sender_id, recipients=[a_id for a_id in env.get_actors() if a_id != actor_id])
                self.__test_with_recipients(speak_executor=speak_executor, env=env, message=message, actor_id=actor_id, custom_sender_id=custom_sender_id, recipients=[])

    def __test_with_recipients(self, speak_executor: SpeakExecutor, env: VWEnvironment, message: Union[int, float, str, list, tuple, dict], actor_id: str, custom_sender_id: str=None, recipients: List[str]=None) -> None:
        sender_id: str = actor_id if custom_sender_id is None else custom_sender_id
        action: VWSpeakAction = VWSpeakAction(message=message, sender_id=sender_id, recipients=recipients)
        action.set_actor_id(actor_id=actor_id)

        self.assertTrue(speak_executor.is_possible(env=env, action=action))

        result: ActionResult = speak_executor.execute(env=env, action=action)

        if sender_id == actor_id or VWCommunicativeAction.SENDER_ID_SPOOFING_ALLOWED:
            self.assertTrue(speak_executor.succeeded(env=env, action=action))
            self.assertTrue(result.get_outcome() == ActionOutcome.success)
        else:
            self.assertTrue(result.get_outcome() == ActionOutcome.failure)

    def test_broadcast_action(self) -> None:
        self.__test_broadcast_action()

    def test_broadcast_action_with_sender_id_spoofing(self) -> None:
        custom_sender_id: str = randbytes(randint(1, 16)).hex()
        self.__test_broadcast_action(custom_sender_id=custom_sender_id)

    def __test_broadcast_action(self, custom_sender_id: str=None) -> None:
        broadcast_executor: BroadcastExecutor = BroadcastExecutor()
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

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
                sender_id: str = actor_id if custom_sender_id is None else custom_sender_id
                action: VWBroadcastAction = VWBroadcastAction(message=message, sender_id=sender_id)
                action.set_actor_id(actor_id=actor_id)

                self.assertTrue(broadcast_executor.is_possible(env=env, action=action))

                result: ActionResult = broadcast_executor.execute(env=env, action=action)

                if sender_id == actor_id or VWCommunicativeAction.SENDER_ID_SPOOFING_ALLOWED:
                    self.assertTrue(broadcast_executor.succeeded(env=env, action=action))
                    self.assertTrue(result.get_outcome() == ActionOutcome.success)
                else:
                    self.assertTrue(result.get_outcome() == ActionOutcome.failure)

    def test_move_action(self) -> None:
        action: VWMoveAction = VWMoveAction()
        move_executor: MoveExecutor = MoveExecutor()
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

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
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

        for actor_id in env.get_actors():
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
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

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
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

        for actor_id, actor in env.get_actors().items():
            drop_green_dirt_action.set_actor_id(actor_id=actor_id)

            if isinstance(actor, VWUser) and not env.get_actor_location(actor_id=actor_id).has_dirt():
                self.assertTrue(drop_executor.is_possible(env=env, action=drop_green_dirt_action))

                result: ActionResult = drop_executor.execute(env=env, action=drop_green_dirt_action)

                self.assertTrue(result.get_outcome() == ActionOutcome.success)
                self.assertTrue(drop_executor.succeeded(env=env, action=drop_green_dirt_action))
            else:
                self.assertFalse(drop_executor.is_possible(env=env, action=drop_green_dirt_action))

        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

        for actor_id, actor in env.get_actors().items():
            drop_orange_dirt_action.set_actor_id(actor_id=actor_id)

            if isinstance(actor, VWUser) and not env.get_actor_location(actor_id=actor_id).has_dirt():
                self.assertTrue(drop_executor.is_possible(env=env, action=drop_orange_dirt_action))

                result: ActionResult = drop_executor.execute(env=env, action=drop_orange_dirt_action)

                self.assertTrue(result.get_outcome() == ActionOutcome.success)
                self.assertTrue(drop_executor.succeeded(env=env, action=drop_orange_dirt_action))
            else:
                self.assertFalse(drop_executor.is_possible(env=env, action=drop_orange_dirt_action))


if __name__ == '__main__':
    main()
