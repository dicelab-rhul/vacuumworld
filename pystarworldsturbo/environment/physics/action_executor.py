from __future__ import annotations
from typing import TYPE_CHECKING

from ...common.action_outcome import ActionOutcome
from ...common.action_result import ActionResult
from ...common.action import Action
from ...utils.utils import ignore

if TYPE_CHECKING:
    from ...environment.environment import Environment



class ActionExecutor():
    def execute(self, env: Environment, action: Action) -> ActionResult:
        assert isinstance(action, Action)

        # Checking the pre-conditions.
        if not self.is_possible(env=env, action=action):
            return ActionResult(ActionOutcome.impossible)
        else:
            # Attempting the action.
            result: ActionResult = self.attempt(env=env, action=action)

            assert result.get_outcome() in [ActionOutcome.success, ActionOutcome.failure]

            # Checking the post-conditions.
            if result.get_outcome() == ActionOutcome.success and not self.succeeded(env=env, action=action):
                result.amend_outcome(new_outcome=ActionOutcome.failure)

            return result

    def is_possible(self, env: Environment, action: Action) -> bool:
        # Abstract.
        ignore(self)
        ignore(env)
        ignore(action)


    def attempt(self, env: Environment, action: Action) -> ActionResult:
        # Abstract.
        ignore(self)
        ignore(env)
        ignore(action)

        return ActionResult(ActionOutcome.impossible)

    def succeeded(self, env: Environment, action: Action) -> bool:
        # Abstract.
        ignore(env)
        ignore(self)
        ignore(action)
