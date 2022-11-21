from __future__ import annotations
from typing import TYPE_CHECKING

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.utils.utils import ignore

from ...actions.vwturn_action import VWTurnAction
from ....common.vwcoordinates import VWCoord
from ....common.vworientation import VWOrientation

if TYPE_CHECKING:
    from ..vwenvironment import VWEnvironment


class VWTurnExecutor(ActionExecutor):
    '''
    This class is an `ActionExecutor` for `VWTurnAction`.
    '''
    def is_possible(self, env: VWEnvironment, action: VWTurnAction) -> bool:
        '''
        Returns whether or not `action` is possible in `env`.

        In any `VWEnvironment` a `VWTurnAction` is always possible. Therefore `True` is always returned.
        '''
        ignore(env)
        ignore(action)

        return True

    def attempt(self, env: VWEnvironment, action: VWTurnAction) -> ActionResult:
        '''
        Attempts to execute `action` in `env`, returning a provisional `ActionResult`.

        If an `Exception` is raised, the provisional `ActionResult` will have an `ActionOutcome` of `ActionOutcome.failure`.

        Otherwise, the provisional `ActionResult` will have an `ActionOutcome` of `ActionOutcome.success`.
        '''
        try:
            actor_id: str = action.get_actor_id()
            actor_position: VWCoord = env.get_actor_position(actor_id=actor_id)

            env.turn_actor(coord=actor_position, direction=action.get_turning_direction())

            return ActionResult(ActionOutcome.success)
        except Exception:
            return ActionResult(ActionOutcome.failure)

    def succeeded(self, env: VWEnvironment, action: VWTurnAction) -> bool:
        '''
        Returns whether or not the post-conditions of `action` are satisfied in `env`.

        The post-conditions of a `VWTurnAction` are satisfied if the `VWOrientation` of the `VWActor` that executed the `VWTurnAction` has been rotated according to the `VWDirection` in `action`.
        '''
        actor_id: str = action.get_actor_id()
        old_actor_orientation: VWOrientation = env.get_actor_previous_orientation(actor_id=actor_id)
        new_actor_orientation: VWOrientation = env.get_actor_orientation(actor_id=actor_id)

        return new_actor_orientation == old_actor_orientation.get(direction=action.get_turning_direction())
