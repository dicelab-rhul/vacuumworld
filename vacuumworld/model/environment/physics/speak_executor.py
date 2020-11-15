from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome

from ..vwenvironment import VWEnvironment
from ...actions.speak_action import VWSpeakAction



class SpeakExecutor(ActionExecutor):
    @staticmethod
    def is_possible(*_) -> bool:
        return True

    @staticmethod
    def attempt(env: VWEnvironment, action: VWSpeakAction) -> ActionResult:
        try:
            env.send_message_to_actors(message=action.get_message())

            return ActionResult(ActionOutcome.success)
        except Exception:
            return ActionResult(ActionOutcome.failure)

    @staticmethod
    def succeeded(*_) -> bool:
        return True
