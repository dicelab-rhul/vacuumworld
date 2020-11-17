from __future__ import annotations

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome

#from ..vwenvironment import VWEnvironment
from ...actions.broadcast_action import VWBroadcastAction
from ....utils.vwutils import ignore



class BroadcastExecutor(ActionExecutor):
    def is_possible(self, env: VWenvironment, action: VWBroadcastAction) -> bool:
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

    def succeeded(self, env: VWenvironment, action: VWBroadcastAction) -> bool:
        ignore(self)
        ignore(env)
        ignore(action)
        
        return True
