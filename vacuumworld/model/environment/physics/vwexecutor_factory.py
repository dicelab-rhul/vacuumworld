from typing import Type, cast
from pyoptional.pyoptional import PyOptional

from pystarworldsturbo.environment.physics.executor_factory import ExecutorFactory
from pystarworldsturbo.environment.physics.action_executor import ActionExecutor

from .vwmove_executor import VWMoveExecutor
from .vwturn_executor import VWTurnExecutor
from .vwclean_executor import VWCleanExecutor
from .vwdrop_executor import VWDropExecutor
from .vwidle_executor import VWIdleExecutor
from .vwspeak_executor import VWSpeakExecutor
from .vwbroadcast_executor import VWBroadcastExecutor
from ....common.vwvalidator import VWValidator
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
    def get_executor_for(action: VWAction) -> PyOptional[ActionExecutor]:
        '''
        Returns an `ActionExecutor` object for the given `VWAction`, or `None` if `action` is incompatible with `VWEnvironment`.
        '''
        assert isinstance(action, VWAction)

        action_type: Type[VWAction] = type(action)

        if action_type == VWMoveAction:
            return PyOptional.of(VWMoveExecutor()).filter(lambda e: VWValidator.does_type_match(t=ActionExecutor, obj=e)).map(lambda e: cast(ActionExecutor, e))
        elif action_type == VWTurnAction:
            return PyOptional.of(VWTurnExecutor()).filter(lambda e: VWValidator.does_type_match(t=ActionExecutor, obj=e)).map(lambda e: cast(ActionExecutor, e))
        elif action_type == VWCleanAction:
            return PyOptional.of(VWCleanExecutor()).filter(lambda e: VWValidator.does_type_match(t=ActionExecutor, obj=e)).map(lambda e: cast(ActionExecutor, e))
        elif action_type == VWDropAction:
            return PyOptional.of(VWDropExecutor()).filter(lambda e: VWValidator.does_type_match(t=ActionExecutor, obj=e)).map(lambda e: cast(ActionExecutor, e))
        elif action_type == VWIdleAction:
            return PyOptional.of(VWIdleExecutor()).filter(lambda e: VWValidator.does_type_match(t=ActionExecutor, obj=e)).map(lambda e: cast(ActionExecutor, e))
        elif action_type == VWSpeakAction:
            return PyOptional.of(VWSpeakExecutor()).filter(lambda e: VWValidator.does_type_match(t=ActionExecutor, obj=e)).map(lambda e: cast(ActionExecutor, e))
        elif action_type == VWBroadcastAction:
            return PyOptional.of(VWBroadcastExecutor()).filter(lambda e: VWValidator.does_type_match(t=ActionExecutor, obj=e)).map(lambda e: cast(ActionExecutor, e))
        else:
            return PyOptional[ActionExecutor].empty()
