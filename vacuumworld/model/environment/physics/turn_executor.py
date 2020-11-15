from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome

from ..vwenvironment import VWEnvironment
from ...actions.turn_action import VWTurnAction
from ....common.coordinates import Coord
from ....common.orientation import Orientation



class TurnExecutor(ActionExecutor):
    @staticmethod
    def is_possible(*_) -> bool:
        return True

    @staticmethod
    def attempt(env: VWEnvironment, action: VWTurnAction) -> ActionResult:
        try:
            actor_id: str = action.get_actor_appearance().get_id()
            actor_position: Coord = env.get_actor_position(actor_id=actor_id)
            
            env.turn_actor(coord=actor_position, direction=action.get_turning_direction())

            return ActionResult(ActionOutcome.success)
        except Exception:
            return ActionResult(ActionOutcome.failure)

    @staticmethod
    def succeeded(env: VWEnvironment, action: VWTurnAction) -> bool:
        actor_id: str = action.get_actor_appearance().get_id()
        actor_position: Coord = env.get_actor_position(actor_id=actor_id)
        old_actor_orientation: Orientation = env.get_ambient().get_grid()[actor_position].get_actor_appearance().get_previous_orientation()
        new_actor_orientation: Orientation = env.get_ambient().get_grid()[actor_position].get_actor_appearance().get_orientation()

        return new_actor_orientation == old_actor_orientation.get(direction=action.get_turning_direction())
