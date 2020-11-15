from ...common.action_outcome import ActionOutcome
from ...common.action_result import ActionResult
from ...common.action import Action
from ...environment.environment import Environment
from ...elements.actor_appearance import ActorAppearance



class ActionExecutor():
    @staticmethod
    def execute(env: Environment, action: Action) -> ActionResult:
        assert isinstance(action, Action)
        assert isinstance(action.get_actor_appearance(), ActorAppearance)

        # Checking the pre-conditions.
        if not ActionExecutor.is_possible(env=env, action=action):
            return ActionResult(ActionOutcome.impossible)
        else:
            # Attempting the action.
            result: ActionResult = ActionExecutor.attempt(env=env, action=action)

            assert result.get_outcome() in [ActionOutcome.success, ActionOutcome.failure]

            # Checking the post-conditions.
            if result.get_outcome() == ActionOutcome.success and not ActionExecutor.succeeded(env=env, action=action):
                result.amend_outcome(new_outcome=ActionOutcome.failure)

            return result

    @staticmethod
    def is_possible(*_) -> bool:
        raise NotImplementedError()

    @staticmethod
    def attempt(*_) -> ActionResult:
        raise NotImplementedError()

    @staticmethod
    def succeeded(*_) -> bool:
        raise NotImplementedError()
