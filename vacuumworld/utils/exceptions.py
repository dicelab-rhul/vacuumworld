class VWMalformedActionException(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super(VWMalformedActionException, self).__init__(args=args, kwargs=kwargs)


class VWActionAttemptException(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super(VWActionAttemptException, self).__init__(args=args, kwargs=kwargs)
