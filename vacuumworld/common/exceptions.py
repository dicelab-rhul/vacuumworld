from __future__ import annotations
from typing import Type, TYPE_CHECKING
from traceback import print_exc

if TYPE_CHECKING:
    from ..model.environment.vwenvironment import VWEnvironment
    from ..model.environment.vwambient import VWAmbient
    from ..model.actor.vwactormind import VWMind
    from ..model.actor.vwagent import VWCleaningAgent



class VWMalformedActionException(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super(VWMalformedActionException, self).__init__(args, kwargs)


class VWActionAttemptException(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super(VWActionAttemptException, self).__init__(args, kwargs)


class VWLoadException(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super(VWActionAttemptException, self).__init__(args, kwargs)


class VWInternalError(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super(VWActionAttemptException, self).__init__(args, kwargs)


class VWExceptionManager():
    @staticmethod
    def manage_exception(e: Exception, context: Type) -> None:
        if type(e) == AssertionError:
            raise e
        elif context in [VWMind, VWCleaningAgent, VWEnvironment, VWAmbient]:
            print_exc()
            print("####################")
            print("Error message: {}".format(e.args[0]))
            print("####################")
