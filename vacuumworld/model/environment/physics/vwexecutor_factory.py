from typing import Type, Optional

from pystarworldsturbo.environment.physics.executor_factory import ExecutorFactory
from pystarworldsturbo.environment.physics.action_executor import ActionExecutor

from .vwmove_executor import VWMoveExecutor
from .vwturn_executor import VWTurnExecutor
from .vwclean_executor import VWCleanExecutor
from .vwdrop_executor import VWDropExecutor
from .vwidle_executor import VWIdleExecutor
from .vwspeak_executor import VWSpeakExecutor
from .vwbroadcast_executor import VWBroadcastExecutor
from ...actions.vwactions import VWAction
from ...actions.vwmove_action import VWMoveAction
from ...actions.vwturn_action import VWTurnAction
from ...actions.vwclean_action import VWCleanAction
from ...actions.vwdrop_action import VWDropAction
from ...actions.vwidle_action import VWIdleAction
from ...actions.vwspeak_action import VWSpeakAction
from ...actions.vwbroadcast_action import VWBroadcastAction


class VWExecutorFactory(ExecutorFactory):
    '''
    This class is a factory for creating `ActionExecutor` objects.
    '''
    @staticmethod
    def get_executor_for(action: VWAction) -> Optional[ActionExecutor]:
        '''
        Returns an `ActionExecutor` object for the given `VWAction`, or `None` if `action` is incompatible with `VWEnvironment`.
        '''
        assert isinstance(action, VWAction)

        action_type: Type = type(action)

        if action_type == VWMoveAction:
            return VWMoveExecutor()
        elif action_type == VWTurnAction:
            return VWTurnExecutor()
        elif action_type == VWCleanAction:
            return VWCleanExecutor()
        elif action_type == VWDropAction:
            return VWDropExecutor()
        elif action_type == VWIdleAction:
            return VWIdleExecutor()
        elif action_type == VWSpeakAction:
            return VWSpeakExecutor()
        elif action_type == VWBroadcastAction:
            return VWBroadcastExecutor()
        else:
            return None
