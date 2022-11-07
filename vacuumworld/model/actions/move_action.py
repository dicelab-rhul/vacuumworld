from .vwactions import VWPhysicalAction


class VWMoveAction(VWPhysicalAction):
    '''
    This class is a `VWPhysicalAction` that moves the `VWActor` in the direction it is facing.
    '''
    def __init__(self) -> None:
        super(VWMoveAction, self).__init__()
