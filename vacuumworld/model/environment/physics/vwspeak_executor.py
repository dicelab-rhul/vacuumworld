from __future__ import annotations
from typing import TYPE_CHECKING

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.common.exceptions import IdentityException
from pystarworldsturbo.utils.utils import ignore

from ...actions.vwspeak_action import VWSpeakAction

if TYPE_CHECKING:
    from ..vwenvironment import VWEnvironment


class VWSpeakExecutor(ActionExecutor):
    '''
    This class is an `ActionExecutor` for `VWSpeakAction`.
    '''
    def is_possible(self, env: VWEnvironment, action: VWSpeakAction) -> bool:
        '''
        Returns whether or not `action` is possible in `env`.

        In any `VWEnvironment` a `VWSpeakAction` is always possible. Therefore `True` is always returned.
        '''
        ignore(env)
        ignore(action)

        return True

    def attempt(self, env: VWEnvironment, action: VWSpeakAction) -> ActionResult:
        '''
        Attempts to execute `action` in `env`, returning a provisional `ActionResult`.

        If an `Exception` is raised, the provisional `ActionResult` will have an `ActionOutcome` of `ActionOutcome.failure`.

        Otherwise, the provisional `ActionResult` will have an `ActionOutcome` of `ActionOutcome.success`.
        '''
        try:
            if not VWSpeakAction.SENDER_ID_SPOOFING_ALLOWED and action.get_message().get_sender_id() != action.get_actor_id():
                raise IdentityException(f"Sender ID spoofing detected: it should be {action.get_actor_id()}, not {action.get_message().get_sender_id()}.")
            else:
                env.send_message_to_recipients(message=action.get_message(), check_sender_identity=not VWSpeakAction.SENDER_ID_SPOOFING_ALLOWED)

                return ActionResult(ActionOutcome.success)
        except Exception:
            return ActionResult(ActionOutcome.failure)

    def succeeded(self, env: VWEnvironment, action: VWSpeakAction) -> bool:
        '''
        Returns whether or not the post-conditions of `action` are satisfied in `env`.

        There are no post-conditions for `VWSpeakAction` to check in `VWEnvironment`, so `True` is always returned.
        '''
        ignore(env)
        ignore(action)

        return True
