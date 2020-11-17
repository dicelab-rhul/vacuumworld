from __future__ import annotations
from typing import TYPE_CHECKING

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome

from ...actions.idle_action import VWIdleAction
from ....utils.vwutils import ignore

if TYPE_CHECKING:
    from ..vwenvironment import VWEnvironment



class IdleExecutor(ActionExecutor):
    def is_possible(self, env: VWEnvironment, action: VWIdleAction) -> bool:
        ignore(self)
        ignore(env)
        ignore(action)

        return True

    def attempt(self, env: VWEnvironment, action: VWIdleAction) -> ActionResult:
        ignore(self)
        ignore(env)
        ignore(action)

        return ActionResult(ActionOutcome.success)

    def succeeded(self, env: VWEnvironment, action: VWIdleAction) -> bool:
        ignore(env)
        ignore(self)
        ignore(action)

        return True
