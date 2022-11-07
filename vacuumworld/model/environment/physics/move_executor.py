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
    '''
    This class is an `ActionExecutor` for `VWMoveAction`.
    '''
    def is_possible(self, env: VWEnvironment, action: VWMoveAction) -> bool:
        '''
        Returns whether or not `action` is possible in `env`.

        In any `VWEnvironment` a `VWMoveAction` is possible if:

        * The `forward` `VWLocation` w.r.t. the `VWLocation` that contains the `VWActor` whose ID matches the actor ID of `action` exists (i.e., is in bounds).

        * The `forward` `VWLocation` w.r.t. the `VWLocation` that contains the `VWActor` whose ID matches the actor ID of `action` has no `VWActor` in it.
        '''
        ignore(self)

        actor_id: str = action.get_actor_id()
        actor_position: Coord = env.get_actor_position(actor_id=actor_id)
        actor_orientation: Orientation = env.get_actor_orientation(actor_id=actor_id)
        forward_position: Coord = actor_position.forward(orientation=actor_orientation)

        # The target location must not be out of bounds and must contain no actor.
        return forward_position in env.get_ambient().get_grid() and not env.get_ambient().get_grid()[forward_position].has_actor()

    def attempt(self, env: VWEnvironment, action: VWMoveAction) -> ActionResult:
        '''
        Attempts to execute `action` in `env`, returning a provisional `ActionResult`.

        If an `Exception` is raised, the provisional `ActionResult` will have an `ActionOutcome` of `ActionOutcome.failure`.

        Otherwise, the provisional `ActionResult` will have an `ActionOutcome` of `ActionOutcome.success`.
        '''
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
        '''
        Returns whether or not the post-conditions of `action` are satisfied in `env`.

        The post-conditions of a `VWMoveAction` are satisfied if the `VWActor` that executed the `VWMoveAction` has moved forward one `VWLocation` w.r.t. its previous `VWLocation`.
        '''
        # This only checks that the agent has not vanished and has not been duplicated.
        # The check for the move success is implicit at this point if not exception has been raised by attempt().

        ignore(self)

        actor_id: str = action.get_actor_id()
        actor_orientation: Orientation = env.get_actor_orientation(actor_id=actor_id)
        actor_position_after_move: Coord = env.get_actor_position(actor_id=actor_id)
        actor_position_before_move: Coord = actor_position_after_move.backward(orientation=actor_orientation)

        if not env.get_ambient().get_grid()[actor_position_after_move].has_actor():
            return False

        if env.get_ambient().get_grid()[actor_position_after_move].get_actor_appearance().get_orientation() != actor_orientation:
            return False

        if env.get_ambient().get_grid()[actor_position_after_move].get_actor_appearance().get_id() != actor_id:
            return False

        if not env.get_ambient().get_grid()[actor_position_before_move].has_actor():
            return True

        return env.get_ambient().get_grid()[actor_position_before_move].get_actor_appearance().get_id() != actor_id
