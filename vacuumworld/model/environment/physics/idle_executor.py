from __future__ import annotations

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome

from ...actions.idle_action import VWIdleAction
from ....utils.vwutils import ignore



class IdleExecutor(ActionExecutor):
    def is_possible(self, env: VWenvironment, action: VWIdleAction) -> bool:
        ignore(self)
        ignore(env)
        ignore(action)

        return True

    def attempt(self, env: VWenvironment, action: VWIdleAction) -> ActionResult:
        ignore(self)
        ignore(env)
        ignore(action)

        return ActionResult(ActionOutcome.success)

    def succeeded(self, env: VWenvironment, action: VWIdleAction) -> bool:
        ignore(self)
        ignore(env)
        ignore(action)

        return True
