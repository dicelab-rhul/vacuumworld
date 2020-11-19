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
