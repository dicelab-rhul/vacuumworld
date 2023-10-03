class VWException(Exception):
    '''
    This class specifies a generic `Exception` for all other VW exceptions to inherit from.
    '''
    def __init__(self, message: str) -> None:
        super(VWException, self).__init__(message)


class VWRunnerException(VWException):
    '''
    This class specifies the `VWException` that is raised when at the `VWRunner` level.
    '''
    def __init__(self, message: str) -> None:
        super(VWRunnerException, self).__init__(message)


class VWSurrogateMindException(VWException):
    '''
    This class specifies the `VWException` that is raised when a provided `VWMindSurrogate` is non-compliant.
    '''
    def __init__(self, message: str) -> None:
        super(VWSurrogateMindException, self).__init__(message)


class VWActionException(VWException):
    '''
    This class specifies the `VWException` that is raised when one or more `VWAction` instances are non-compliant.
    '''
    def __init__(self, message: str) -> None:
        super(VWActionException, self).__init__(message)


class VWMalformedActionException(VWActionException):
    '''
    This class specifies the `VWActionException` that is raised when a malformed `VWAction` is attempted.
    '''
    def __init__(self, message: str) -> None:
        super(VWMalformedActionException, self).__init__(message)


class VWActionAttemptException(VWActionException):
    '''
    This class specifies the `VWActionException` that is raised when a malformed pool of `VWAction` instances is attempted.
    '''
    def __init__(self, message: str) -> None:
        super(VWActionAttemptException, self).__init__(message)


class VWPerceptionException(VWException):
    '''
    This class specifies the `VWException` that is raised when a `Perception` is malformed, unsupported, or does not exist when it should.
    '''
    def __init__(self, message: str) -> None:
        super(VWPerceptionException, self).__init__(message)


class VWLoadException(VWException):
    '''
    This class specifies the `VWException` that is raised when an error occurs while loading a `VWEnvironment` from a file.
    '''
    def __init__(self, message: str) -> None:
        super(VWLoadException, self).__init__(message)


class VWInternalError(VWException):
    '''
    This class specifies the `VWException` that is raised when a generic or unknown internal error occurs.
    '''
    def __init__(self, message: str) -> None:
        super(VWInternalError, self).__init__(message)


class VWEndOfCyclesException(VWException):
    '''
    This class specifies the `VWException` that is raised when the simulation has reached the maximum number of cycles.
    '''
    def __init__(self, message: str) -> None:
        super(VWEndOfCyclesException, self).__init__(message)
