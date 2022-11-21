from __future__ import annotations
from typing import TYPE_CHECKING

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.utils.utils import ignore

from ...actions.vwidle_action import VWIdleAction

if TYPE_CHECKING:
    from ..vwenvironment import VWEnvironment


class VWIdleExecutor(ActionExecutor):
    '''
    This class is an `ActionExecutor` for `VWIdleAction`.
    '''
    def is_possible(self, env: VWEnvironment, action: VWIdleAction) -> bool:
        '''
        Returns whether or not `action` is possible in `env`.

        In any `VWEnvironment` a `VWIdleAction` is always possible. Therefore `True` is always returned.
        '''
        ignore(self)
        ignore(env)
        ignore(action)

        return True

    def attempt(self, env: VWEnvironment, action: VWIdleAction) -> ActionResult:
        '''
        Attempts to execute `action` in `env`, returning a provisional `ActionResult`.

        For every `VWIdleAction` in any `VWEnvironment` the provisional `ActionResult` will always have an `ActionOutcome` of `ActionOutcome.success`.
        '''
        ignore(self)
        ignore(env)
        ignore(action)

        return ActionResult(ActionOutcome.success)

    def succeeded(self, env: VWEnvironment, action: VWIdleAction) -> bool:
        '''
        Returns whether or not the post-conditions of `action` are satisfied in `env`.

        There are no post-conditions for `VWIdleAction` to check in `VWEnvironment`, so `True` is always returned.
        '''
        ignore(env)
        ignore(self)
        ignore(action)

        return True
