from .vwactions import VWPhysicalAction


class VWIdleAction(VWPhysicalAction):
    '''
    This class is a `VWPhysicalAction` that does nothing.
    '''
    def __init__(self) -> None:
        super(VWIdleAction, self).__init__()
