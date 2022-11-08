from __future__ import annotations
from typing import Type, TYPE_CHECKING
from traceback import print_exc

if TYPE_CHECKING:
    from ..model.environment.vwenvironment import VWEnvironment
    from ..model.environment.vwambient import VWAmbient
    from ..model.actor.vwactormind import VWMind
    from ..model.actor.vwagent import VWCleaningAgent


class VWMalformedActionException(Exception):
    '''
    This class specifies the `Exception` that is raised when a malformed `VWAction` is attempted.
    '''
    def __init__(self, message) -> None:
        super(VWMalformedActionException, self).__init__(message)


class VWActionAttemptException(Exception):
    '''
    This class specifies the `Exception` that is raised when a malformed pool of `VWAction` instances is attempted.
    '''
    def __init__(self, message) -> None:
        super(VWActionAttemptException, self).__init__(message)


class VWPerceptionException(Exception):
    '''
    This class specifies the `Exception` that is raised when a `Perception` is malformed, unsupported, or does not exist when it should.
    '''
    def __init__(self, message) -> None:
        super(VWPerceptionException, self).__init__(message)


class VWLoadException(Exception):
    '''
    This class specifies the `Exception` that is raised when an error occurs while loading a `VWEnvironment` from a file.
    '''
    def __init__(self, message) -> None:
        super(VWLoadException, self).__init__(message)


class VWInternalError(Exception):
    '''
    This class specifies the `Exception` that is raised when a generic internal error occurs.
    '''
    def __init__(self, message) -> None:
        super(VWInternalError, self).__init__(message)


class VWEndOfCyclesException(Exception):
    '''
    This class specifies the `Exception` that is raised when the simulation has reached the maximum number of cycles.
    '''
    def __init__(self, message) -> None:
        super(VWEndOfCyclesException, self).__init__(message)


# TODO: this class is unused for now.
class VWExceptionManager():
    '''
    This class provides a custom `Exception` handler for VacuumWorld.
    '''
    @staticmethod
    def manage_exception(e: Exception, context: Type) -> None:
        '''
        Handles the given `Exception` by printing the traceback and the message of the `Exception` to the console.
        '''
        if type(e) == AssertionError:
            raise e
        elif context in [VWMind, VWCleaningAgent, VWEnvironment, VWAmbient]:
            print_exc()

            print("####################")
            print("Error message: {}".format(e.args[0]))
            print("####################")
