#!/usr/bin/env python3

from unittest import main, TestCase
from typing import List, Callable, Any
from random import randint
from pyoptional.pyoptional import PyOptional

from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.common.content_type import MessageContentType

from vacuumworld import VacuumWorld
from vacuumworld.common.vwcoordinates import VWCoord
from vacuumworld.common.vwcolour import VWColour
from vacuumworld.common.vwdirection import VWDirection
from vacuumworld.common.vwobservation import VWObservation
from vacuumworld.common.vworientation import VWOrientation
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vwspeak_action import VWSpeakAction
from vacuumworld.model.actions.vwturn_action import VWTurnAction
from vacuumworld.model.actions.vwclean_action import VWCleanAction
from vacuumworld.model.actions.vwdrop_action import VWDropAction
from vacuumworld.model.actions.vwmove_action import VWMoveAction
from vacuumworld.model.actions.vwbroadcast_action import VWBroadcastAction
from vacuumworld.model.actions.vwactions import VWCommunicativeAction
from vacuumworld.model.actor.vwactor import VWActor
from vacuumworld.model.actor.appendices.vwsensors import VWObservationSensor
from vacuumworld.model.actor.vwuser import VWUser
from vacuumworld.model.environment.physics.vwbroadcast_executor import VWBroadcastExecutor
from vacuumworld.model.environment.physics.vwclean_executor import VWCleanExecutor
from vacuumworld.model.environment.physics.vwdrop_executor import VWDropExecutor
from vacuumworld.model.environment.physics.vwidle_executor import VWIdleExecutor
from vacuumworld.model.environment.physics.vwmove_executor import VWMoveExecutor
from vacuumworld.model.environment.physics.vwspeak_executor import VWSpeakExecutor
from vacuumworld.model.environment.physics.vwturn_executor import VWTurnExecutor
from vacuumworld.model.dirt.vwdirt_appearance import VWDirtAppearance
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.model.environment.vwenvironment import VWEnvironment
from vacuumworld.vwconfig_manager import VWConfigManager

import os
import random as random_module


class TestExecutors(TestCase):
    '''
    This class tests the executors for each non-abstract subclass of `VWAction`:
    * `VWIdleExecutor` for `VWIdleAction`.
    * `VWSpeakExecutor` for `VWSpeakAction`.
    * `VWTurnExecutor` for `VWTurnAction`.
    * `VWCleanExecutor` for `VWCleanAction`.
    * `VWDropExecutor` for `VWDropAction`.
    * `VWMoveExecutor` for `VWMoveAction`.
    * `VWBroadcastExecutor` for `VWBroadcastAction`.
    '''
    def __init__(self, args: Any) -> None:
        super(TestExecutors, self).__init__(args)

        self.__config: dict[str, Any] = VWConfigManager.load_config_from_file(config_file_path=VacuumWorld.CONFIG_FILE_PATH, load_additional_config=False)
        self.__randbytes: Callable[[int], bytes] = random_module.randbytes if hasattr(random_module, "randbytes") else os.urandom
        self.__message_content_list: List[MessageContentType] = [
            "Hello World!",
            ["Hello", "World", "!"],
            {
                "Hello": 5,
                "World": 5,
                "!": 1
            },
            bytes("foobar", "utf-8"),
            1337,
            0.1337,
            False
        ]

        VWCommunicativeAction.SENDER_ID_SPOOFING_ALLOWED = self.__config["sender_id_spoofing_allowed"]

    def test_idle_action(self) -> None:
        '''
        Tests the execution of a `VWIdleAction` by a `VWIdleExecutor`.
        '''
        action: VWIdleAction = VWIdleAction()
        idle_executor: VWIdleExecutor = VWIdleExecutor()
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

        for actor_id in env.get_actors():
            action.set_actor_id(actor_id=actor_id)

            self.assertTrue(idle_executor.is_possible(env=env, action=action))

            result: ActionResult = idle_executor.execute(env=env, action=action)

            self.assertTrue(result.get_outcome() == ActionOutcome.success)
            self.assertTrue(idle_executor.succeeded(env=env, action=action))

    def test_speak_action(self) -> None:
        '''
        Tests the execution of a `VWSpeakAction` by a `VWSpeakExecutor` without `sender_id` spoofing.

        Both the cases of an empty (i.e., equivalent to `VWBroadcastAction`) and a non-empty list of recipients are tested.
        '''
        self.__test_speak_action()

    def test_speak_action_with_sender_id_spoofing(self) -> None:
        '''
        Tests the execution of a `VWSpeakAction` by a `VWSpeakExecutor` with `sender_id` spoofing (i.e., with a custom randon sender ID).

        Both the cases of an empty (i.e., equivalent to `VWBroadcastAction`) and a non-empty list of recipients are tested.
        '''
        custom_sender_id: str = self.__randbytes(randint(1, 16)).hex()
        self.__test_speak_action(custom_sender_id=PyOptional.of(custom_sender_id))

    def __test_speak_action(self, custom_sender_id: PyOptional[str]=PyOptional.empty()) -> None:
        speak_executor: VWSpeakExecutor = VWSpeakExecutor()
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

        self.__test_messages_delivery(messages=self.__message_content_list, speak_executor=speak_executor, env=env, custom_sender_id=custom_sender_id, recipients=[a_id for a_id in env.get_actors()])
        self.__test_messages_delivery(messages=self.__message_content_list, speak_executor=speak_executor, env=env, custom_sender_id=custom_sender_id, recipients=[])

    def __test_messages_delivery(self, messages: List[Any], speak_executor: VWSpeakExecutor, env: VWEnvironment, custom_sender_id: PyOptional[str], recipients: List[str]) -> None:
        for message in messages:
            for real_sender_id in env.get_actors():
                self.__test_message_delivery(speak_executor=speak_executor, env=env, message=message, real_sender_id=real_sender_id, custom_sender_id=custom_sender_id, recipients=[r_id for r_id in recipients if r_id != real_sender_id])

    def __test_message_delivery(self, speak_executor: VWSpeakExecutor, env: VWEnvironment, message: MessageContentType, real_sender_id: str, custom_sender_id: PyOptional[str]=PyOptional.empty(), recipients: List[str]=[]) -> None:
        sender_id: str = custom_sender_id.or_else(real_sender_id)
        action: VWSpeakAction = VWSpeakAction(message=message, sender_id=sender_id, recipients=recipients)
        action.set_actor_id(actor_id=real_sender_id)

        self.assertTrue(speak_executor.is_possible(env=env, action=action))

        result: ActionResult = speak_executor.execute(env=env, action=action)

        if sender_id == real_sender_id or VWCommunicativeAction.SENDER_ID_SPOOFING_ALLOWED:
            self.assertTrue(speak_executor.succeeded(env=env, action=action))
            self.assertTrue(result.get_outcome() == ActionOutcome.success)

            self.__test_message_received(env=env, message=message, recipients=recipients, sender_id=sender_id)
        else:
            self.assertTrue(result.get_outcome() == ActionOutcome.failure)

    def __test_message_received(self, env: VWEnvironment, message: MessageContentType, sender_id: str, recipients: List[str]) -> None:
        for recipient_id in recipients:
            fake_observation: VWObservation = VWObservation(action_type=VWIdleAction, action_result=ActionResult(outcome=ActionOutcome.impossible), locations_dict={})
            recipient_actor: VWActor = env.get_actor(actor_id=recipient_id).or_else_raise()

            # We just want the physical sensor.
            sensor: PyOptional[VWObservationSensor] = recipient_actor.get_observation_sensor()

            self.assertTrue(sensor.is_present())

            sensor.or_else_raise().sink(perception=fake_observation)

            _, messages = recipient_actor.test_get_percepts()

            self.assertTrue(sender_id in [m.get_sender_id() for m in messages])

            received: bool = False

            for m in messages:
                if m.get_sender_id() == sender_id and m.get_content() == message:
                    received = True

            self.assertTrue(received)

    def test_broadcast_action(self) -> None:
        '''
        Tests the execution of a `VWBroadcastAction` by a `VWBroadcastExecutor` without `sender_id` spoofing.
        '''
        self.__test_broadcast_action()

    def test_broadcast_action_with_sender_id_spoofing(self) -> None:
        '''
        Tests the execution of a `VWBroadcastAction` by a `VWBroadcastExecutor` with `sender_id` spoofing (i.e., with a custom randon sender ID).
        '''
        custom_sender_id: str = self.__randbytes(randint(1, 16)).hex()
        self.__test_broadcast_action(custom_sender_id=PyOptional.of(custom_sender_id))

    def __test_broadcast_action(self, custom_sender_id: PyOptional[str]=PyOptional.empty()) -> None:
        broadcast_executor: VWBroadcastExecutor = VWBroadcastExecutor()
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

        for message in self.__message_content_list:
            for real_sender_id in env.get_actors():
                self.__test_broadcast_delivery(broadcast_executor=broadcast_executor, env=env, message=message, real_sender_id=real_sender_id, custom_sender_id=custom_sender_id)

    def __test_broadcast_delivery(self, broadcast_executor: VWBroadcastExecutor, env: VWEnvironment, message: Any, real_sender_id: str, custom_sender_id: PyOptional[str]) -> None:
        sender_id: str = custom_sender_id.or_else(real_sender_id)
        action: VWBroadcastAction = VWBroadcastAction(message=message, sender_id=sender_id)
        action.set_actor_id(actor_id=real_sender_id)

        self.assertTrue(broadcast_executor.is_possible(env=env, action=action))

        result: ActionResult = broadcast_executor.execute(env=env, action=action)

        if sender_id == real_sender_id or VWCommunicativeAction.SENDER_ID_SPOOFING_ALLOWED:
            self.assertTrue(broadcast_executor.succeeded(env=env, action=action))
            self.assertTrue(result.get_outcome() == ActionOutcome.success)

            self.__test_message_received(env=env, message=message, recipients=[a_id for a_id in env.get_actors() if a_id != real_sender_id], sender_id=sender_id)
        else:
            self.assertTrue(result.get_outcome() == ActionOutcome.failure)

    def test_move_action(self) -> None:
        '''
        Tests the execution of a `VWMoveAction` by a `VWMoveExecutor`.
        '''
        action: VWMoveAction = VWMoveAction()
        move_executor: VWMoveExecutor = VWMoveExecutor()
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

        for actor_id in env.get_actors():
            action.set_actor_id(actor_id=actor_id)

            actor_position: VWCoord = env.get_actor_position(actor_id=actor_id)
            orientation: VWOrientation = env.get_actor_location(actor_id=actor_id).get_actor_appearance().or_else_raise().get_orientation()
            forward_position: VWCoord = actor_position.forward(orientation=orientation)
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

    def __actor_on_location(self, location: VWLocation, actor_id: str, orientation: VWOrientation) -> bool:
        if not location.has_actor():
            return False

        if location.get_actor_appearance().or_else_raise().get_id() != actor_id:
            return False

        return location.get_actor_appearance().or_else_raise().get_orientation() == orientation

    def test_turn_action(self) -> None:
        '''
        Tests the execution of a `VWTurnAction` by a `VWTurnExecutor`.

        Both the cases of a turn to `VWDirection.left` and to `VWDirection.right` are tested.
        '''
        left_turn_action: VWTurnAction = VWTurnAction(VWDirection.left)
        right_turn_action: VWTurnAction = VWTurnAction(VWDirection.right)
        turn_executor: VWTurnExecutor = VWTurnExecutor()
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

        for actor_id in env.get_actors():
            left_turn_action.set_actor_id(actor_id=actor_id)

            old_orientation: VWOrientation = env.get_actor_location(actor_id=actor_id).get_actor_appearance().or_else_raise().get_orientation()

            self.assertTrue(turn_executor.is_possible(env=env, action=left_turn_action))

            result: ActionResult = turn_executor.execute(env=env, action=left_turn_action)

            self.assertTrue(result.get_outcome() == ActionOutcome.success)
            self.assertTrue(turn_executor.succeeded(env=env, action=left_turn_action))
            self.assertEqual(env.get_actor_location(actor_id=actor_id).get_actor_appearance().or_else_raise().get_orientation(), old_orientation.get_left())
            self.assertEqual(env.get_actor_location(actor_id=actor_id).get_actor_appearance().or_else_raise().get_previous_orientation(), old_orientation)

        for actor_id in env.get_actors():
            right_turn_action.set_actor_id(actor_id=actor_id)

            old_orientation: VWOrientation = env.get_actor_location(actor_id=actor_id).get_actor_appearance().or_else_raise().get_orientation()

            self.assertTrue(turn_executor.is_possible(env=env, action=right_turn_action))

            result: ActionResult = turn_executor.execute(env=env, action=right_turn_action)

            self.assertTrue(result.get_outcome() == ActionOutcome.success)
            self.assertTrue(turn_executor.succeeded(env=env, action=right_turn_action))
            self.assertEqual(env.get_actor_location(actor_id=actor_id).get_actor_appearance().or_else_raise().get_orientation(), old_orientation.get_right())
            self.assertEqual(env.get_actor_location(actor_id=actor_id).get_actor_appearance().or_else_raise().get_previous_orientation(), old_orientation)

    def test_clean_action(self) -> None:
        '''
        Tests the execution of a `VWCleanAction` by a `VWCleanExecutor`.

        The tests also checks that the `VWActor` is a `VWCleaningAgent`, and that the `VWColour` of the `VWActor` is compatible with the `VWColour` of the `VWDirt`.
        '''
        action: VWCleanAction = VWCleanAction()
        clean_executor: VWCleanExecutor = VWCleanExecutor()
        env, _ = VWEnvironment.generate_random_env_for_testing(custom_grid_size=True, config=self.__config)

        for actor_id in env.get_actors():
            action.set_actor_id(actor_id=actor_id)

            dirt_appearance: PyOptional[VWDirtAppearance] = env.get_actor_location(actor_id=actor_id).get_dirt_appearance()
            actor_colour: VWColour = env.get_actor_location(actor_id=actor_id).get_actor_appearance().or_else_raise().get_colour()

            if dirt_appearance.is_present() and (actor_colour == dirt_appearance.or_else_raise().get_colour() or actor_colour == VWColour.white):
                self.assertTrue(clean_executor.is_possible(env=env, action=action))

                result: ActionResult = clean_executor.execute(env=env, action=action)

                self.assertTrue(result.get_outcome() == ActionOutcome.success)
                self.assertTrue(clean_executor.succeeded(env=env, action=action))
            else:
                self.assertFalse(clean_executor.is_possible(env=env, action=action))

    def test_drop_action(self) -> None:
        '''
        Tests the execution of a `VWDropAction` by a `VWDropExecutor`.

        Both the cases of the drop of a `VWColour.green` and the drop of a `VWColour.orange` are tested.

        The tests also checks that the `VWActor` is a `VWUser`.
        '''
        drop_green_dirt_action: VWDropAction = VWDropAction(dirt_colour=VWColour.green)
        drop_orange_dirt_action: VWDropAction = VWDropAction(dirt_colour=VWColour.orange)
        drop_executor: VWDropExecutor = VWDropExecutor()
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
