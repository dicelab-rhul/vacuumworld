from __future__ import annotations
from typing import TYPE_CHECKING

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.utils.utils import ignore

from ...actions.turn_action import VWTurnAction
from ....common.coordinates import Coord
from ....common.orientation import Orientation

if TYPE_CHECKING:
    from ..vwenvironment import VWEnvironment


class TurnExecutor(ActionExecutor):
    def is_possible(self, env: VWEnvironment, action: VWTurnAction) -> bool:
        ignore(self)
        ignore(env)
        ignore(action)

        return True

    def attempt(self, env: VWEnvironment, action: VWTurnAction) -> ActionResult:
        ignore(self)

        try:
            actor_id: str = action.get_actor_id()
            actor_position: Coord = env.get_actor_position(actor_id=actor_id)

            env.turn_actor(coord=actor_position, direction=action.get_turning_direction())

            return ActionResult(ActionOutcome.success)
        except Exception:
            return ActionResult(ActionOutcome.failure)

    def succeeded(self, env: VWEnvironment, action: VWTurnAction) -> bool:
        ignore(self)

        actor_id: str = action.get_actor_id()
        old_actor_orientation: Orientation = env.get_actor_previous_orientation(actor_id=actor_id)
        new_actor_orientation: Orientation = env.get_actor_orientation(actor_id=actor_id)

        return new_actor_orientation == old_actor_orientation.get(direction=action.get_turning_direction())
