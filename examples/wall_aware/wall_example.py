#!/usr/bin/env python3

from typing import Iterable, Tuple, Union, List
from random import randint

from pystarworldsturbo.common.message import BccMessage

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction, VWPhysicalAction
from vacuumworld.model.actions.broadcast_action import VWBroadcastAction
from vacuumworld.model.actions.move_action import VWMoveAction
from vacuumworld.model.actions.turn_action import VWTurnAction
from vacuumworld.model.actions.idle_action import VWIdleAction
from vacuumworld.model.actions.effort import ActionEffort
from vacuumworld.model.actor.actor_mind_surrogate import ActorMindSurrogate
from vacuumworld.common.observation import Observation
from vacuumworld.common.orientation import Orientation
from vacuumworld.common.direction import Direction
from vacuumworld.model.environment.vwlocation import VWLocation


class WallMind(ActorMindSurrogate):
    def __init__(self) -> None:
        super(WallMind, self).__init__()

        # Add here all the attributes you need/want.

    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        self.__observation: Observation = observation

        assert self.__observation.get_center() and self.__observation.get_center().has_actor()

        self.__current_location: VWLocation = self.__observation.get_center()
        self.__orientation: Orientation = self.__current_location.get_actor_appearance().get_orientation()
        self.__id: str = self.__current_location.get_actor_appearance().get_id()

        for message in messages:
            print(message)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        return self.__random_physical_action(), self.__broadcast_possible_physical_actions()

    def __broadcast_possible_physical_actions(self) -> VWBroadcastAction:
        """
        This method broadcasts the possible physical actions that the sender `VWCleaningAgent` can perform.
        """

        actions: List[VWPhysicalAction] = [VWIdleAction, VWTurnAction]

        if self.__can_move():
            actions.append(VWMoveAction)

        return VWBroadcastAction(message="Possible physical actions for me: {}".format([action.__name__ for action in actions]), sender_id=self.__id)

    def __random_physical_action(self) -> VWAction:
        pool: List[VWPhysicalAction] = [VWTurnAction, VWTurnAction]

        if self.__can_move():
            pool.append(VWMoveAction)

        roll: int = randint(0, len(pool) - 1)

        assert 0 <= roll < len(pool)

        if roll == 0:
            return pool[0](direction=Direction.left)
        elif roll == 1:
            return pool[1](direction=Direction.right)
        else:
            assert VWMoveAction in pool

            return VWMoveAction()

    def __can_move(self) -> bool:
        """
        This method uses the Wall API to check if the `VWCleaningAgent` can move forward.

        It is a much safer alternative than to check whether a `VWLocation` exists or not.
        """

        # Here the second condition will not raise an exception because we know that the forward location is not None because of the first condition.
        return not self.__observation.get_center().has_wall_on(orientation=self.__orientation) and not self.__observation.get_forward().has_actor()


if __name__ == "__main__":
    run(default_mind=WallMind(), efforts=ActionEffort.REASONABLE_EFFORTS)
