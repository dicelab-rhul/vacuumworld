from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome



class IdleExecutor(ActionExecutor):
    @staticmethod
    def is_possible(*_) -> bool:
        return True

    @staticmethod
    def attempt(*_) -> ActionResult:
        return ActionResult(ActionOutcome.success)

    @staticmethod
    def succeeded(*_) -> bool:
        return True
