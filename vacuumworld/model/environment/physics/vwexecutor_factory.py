from typing import Type, Optional

from pystarworldsturbo.environment.physics.executor_factory import ExecutorFactory
from pystarworldsturbo.environment.physics.action_executor import ActionExecutor

from .move_executor import MoveExecutor
from .turn_executor import TurnExecutor
from .clean_executor import CleanExecutor
from .drop_executor import DropExecutor
from .idle_executor import IdleExecutor
from .speak_executor import SpeakExecutor
from .broadcast_executor import BroadcastExecutor
from ...actions.vwactions import VWAction
from ...actions.move_action import VWMoveAction
from ...actions.turn_action import VWTurnAction
from ...actions.clean_action import VWCleanAction
from ...actions.drop_action import VWDropAction
from ...actions.idle_action import VWIdleAction
from ...actions.speak_action import VWSpeakAction
from ...actions.broadcast_action import VWBroadcastAction


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
            return MoveExecutor()
        elif action_type == VWTurnAction:
            return TurnExecutor()
        elif action_type == VWCleanAction:
            return CleanExecutor()
        elif action_type == VWDropAction:
            return DropExecutor()
        elif action_type == VWIdleAction:
            return IdleExecutor()
        elif action_type == VWSpeakAction:
            return SpeakExecutor()
        elif action_type == VWBroadcastAction:
            return BroadcastExecutor()
        else:
            return None
