from __future__ import annotations
from typing import TYPE_CHECKING

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.utils.utils import ignore

from ...actions.broadcast_action import VWBroadcastAction

if TYPE_CHECKING:
    from ..vwenvironment import VWEnvironment



class BroadcastExecutor(ActionExecutor):
    def is_possible(self, env: VWEnvironment, action: VWBroadcastAction) -> bool:
        ignore(self)
        ignore(env)
        ignore(action)

        return True

    def attempt(self, env: VWEnvironment, action: VWBroadcastAction) -> ActionResult:
        ignore(self)
        
        try:
            env.send_message_to_actors(message=action.get_message())

            return ActionResult(ActionOutcome.success)
        except Exception:
            return ActionResult(ActionOutcome.failure)

    def succeeded(self, env: VWEnvironment, action: VWBroadcastAction) -> bool:
        ignore(env)
        ignore(self)
        ignore(action)
        
        return True
