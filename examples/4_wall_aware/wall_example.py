#!/usr/bin/env python3

from typing import Iterable, Type, cast
from random import randint

from vacuumworld import run
from vacuumworld.model.actions.vwactions import VWAction, VWPhysicalAction
from vacuumworld.model.actions.vwbroadcast_action import VWBroadcastAction
from vacuumworld.model.actions.vwmove_action import VWMoveAction
from vacuumworld.model.actions.vwturn_action import VWTurnAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.model.actions.vweffort import VWActionEffort
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.common.vwdirection import VWDirection


class WallMind(VWActorMindSurrogate):
    def __init__(self) -> None:
        super(WallMind, self).__init__()

        # Add here all the attributes you need/want.

    def revise(self) -> None:
        # No need to revise anything.
        pass

    def decide(self) -> Iterable[VWAction]:
        return [cast(VWAction, self.__random_physical_action())] + [cast(VWAction, self.__broadcast_possible_physical_actions())]

    def __broadcast_possible_physical_actions(self) -> VWBroadcastAction:
        '''
        This method broadcasts the possible physical actions that the sender `VWCleaningAgent` can perform.
        '''
        actions: list[Type[VWPhysicalAction]] = [VWIdleAction, VWTurnAction]

        if self.__can_move():
            actions.append(VWMoveAction)

        return VWBroadcastAction(message=f"Possible physical actions for me: {[action.__name__ for action in actions]}", sender_id=self.get_own_id())

    def __random_physical_action(self) -> VWPhysicalAction:
        pool: list[Type[VWPhysicalAction]] = [VWTurnAction, VWTurnAction]

        if self.__can_move():
            pool.append(VWMoveAction)

        roll: int = randint(0, len(pool) - 1)

        assert 0 <= roll < len(pool)

        if roll == 0 and isinstance(pool[0], Type) and issubclass(pool[0], VWTurnAction):
            return pool[0](direction=VWDirection.left)
        elif roll == 1 and isinstance(pool[1], Type) and issubclass(pool[1], VWTurnAction):
            return pool[1](direction=VWDirection.right)
        else:
            assert VWMoveAction in pool

            return VWMoveAction()

    def __can_move(self) -> bool:
        '''
        This method uses the Wall API to check if the `VWCleaningAgent` can move forward.

        It is a much safer alternative than to check whether a `VWLocation` exists or not.
        '''

        # Here the second condition will not raise an exception because we know that the forward location is not None because of the first condition.
        return not self.get_latest_observation().get_center().or_else_raise().has_wall_on(orientation=self.get_own_orientation()) and not self.get_latest_observation().get_forward().or_else_raise().has_actor()


if __name__ == "__main__":
    run(default_mind=WallMind(), efforts=VWActionEffort.REASONABLE_EFFORTS)
