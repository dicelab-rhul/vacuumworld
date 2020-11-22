from __future__ import annotations
from typing import TYPE_CHECKING

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.utils.utils import ignore

from ...actions.move_action import VWMoveAction
from ....common.coordinates import Coord
from ....common.orientation import Orientation

if TYPE_CHECKING:
    from ..vwenvironment import VWEnvironment



class MoveExecutor(ActionExecutor):
    def is_possible(self, env: VWEnvironment, action: VWMoveAction) -> bool:
        ignore(self)
        
        actor_id: str = action.get_actor_id()
        actor_position: Coord = env.get_actor_position(actor_id=actor_id)
        actor_orientation: Orientation = env.get_actor_orientation(actor_id=actor_id)
        forward_position: Coord = actor_position.forward(orientation=actor_orientation)

        # The target location must not be out of bounds and must contain no actor.
        return forward_position in env.get_ambient().get_grid() and not env.get_ambient().get_grid()[forward_position].has_actor()

    def attempt(self, env: VWEnvironment, action: VWMoveAction) -> ActionResult:
        ignore(self)
        
        try:
            actor_id: str = action.get_actor_id()
            actor_position: Coord = env.get_actor_position(actor_id=actor_id)
            actor_orientation: Orientation = env.get_actor_orientation(actor_id=actor_id)
            forward_position: Coord = actor_position.forward(orientation=actor_orientation)

            assert forward_position in env.get_ambient().get_grid() and not env.get_ambient().get_grid()[forward_position].has_actor()

            env.move_actor(from_coord=actor_position, to_coord=forward_position)

            return ActionResult(ActionOutcome.success)
        except Exception:
            return ActionResult(ActionOutcome.failure)

    def succeeded(self, env: VWEnvironment, action: VWMoveAction) -> bool:
        # This only checks that the agent has not vanished and has not been duplicated.
        # The check for the move success is implicit at this point if not exception has been raised by attempt().

        ignore(self)

        actor_id: str = action.get_actor_id()
        actor_orientation: Orientation = env.get_actor_orientation(actor_id=actor_id)
        actor_position_after_move: Coord = env.get_actor_position(actor_id=actor_id)
        actor_position_before_move: Coord = actor_position_after_move.backward(orientation=actor_orientation)

        if not env.get_ambient().get_grid()[actor_position_after_move].has_actor():
            return False
        
        if not env.get_ambient().get_grid()[actor_position_after_move].get_actor_appearance().get_id() == actor_id:
            return False

        if not env.get_ambient().get_grid()[actor_position_before_move].has_actor():
            return True

        return env.get_ambient().get_grid()[actor_position_before_move].get_actor_appearance().get_id() != actor_id
