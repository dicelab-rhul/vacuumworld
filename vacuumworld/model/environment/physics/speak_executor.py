from __future__ import annotations
from typing import TYPE_CHECKING

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.utils.utils import ignore

from ...actions.speak_action import VWSpeakAction

if TYPE_CHECKING:
    from ..vwenvironment import VWEnvironment


class SpeakExecutor(ActionExecutor):
    def is_possible(self, env: VWEnvironment, action: VWSpeakAction) -> bool:
        ignore(self)
        ignore(env)
        ignore(action)

        return True

    def attempt(self, env: VWEnvironment, action: VWSpeakAction) -> ActionResult:
        ignore(self)
        ignore(env)
        ignore(action)

        try:
            env.send_message_to_actors(message=action.get_message())

            return ActionResult(ActionOutcome.success)
        except Exception:
            return ActionResult(ActionOutcome.failure)

    def succeeded(self, env: VWEnvironment, action: VWSpeakAction) -> bool:
        ignore(env)
        ignore(self)
        ignore(action)

        return True
