from .action_executor import ActionExecutor
from ...common.action import Action



class ExecutorFactory():
    @staticmethod
    def get_executor_for(action: Action) -> ActionExecutor:
        # Abstract.
        pass
