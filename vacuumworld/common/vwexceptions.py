class VWMalformedActionException(Exception):
    '''
    This class specifies the `Exception` that is raised when a malformed `VWAction` is attempted.
    '''
    def __init__(self, message: str) -> None:
        super(VWMalformedActionException, self).__init__(message)


class VWActionAttemptException(Exception):
    '''
    This class specifies the `Exception` that is raised when a malformed pool of `VWAction` instances is attempted.
    '''
    def __init__(self, message: str) -> None:
        super(VWActionAttemptException, self).__init__(message)


class VWPerceptionException(Exception):
    '''
    This class specifies the `Exception` that is raised when a `Perception` is malformed, unsupported, or does not exist when it should.
    '''
    def __init__(self, message: str) -> None:
        super(VWPerceptionException, self).__init__(message)


class VWLoadException(Exception):
    '''
    This class specifies the `Exception` that is raised when an error occurs while loading a `VWEnvironment` from a file.
    '''
    def __init__(self, message: str) -> None:
        super(VWLoadException, self).__init__(message)


class VWInternalError(Exception):
    '''
    This class specifies the `Exception` that is raised when a generic internal error occurs.
    '''
    def __init__(self, message: str) -> None:
        super(VWInternalError, self).__init__(message)


class VWEndOfCyclesException(Exception):
    '''
    This class specifies the `Exception` that is raised when the simulation has reached the maximum number of cycles.
    '''
    def __init__(self, message: str) -> None:
        super(VWEndOfCyclesException, self).__init__(message)


class VWRunnerException(Exception):
    '''
    This class specifies the `Exception` that is raised when a `VWRunner` cannot be instantiated.
    '''
    def __init__(self, message: str) -> None:
        super(VWRunnerException, self).__init__(message)
