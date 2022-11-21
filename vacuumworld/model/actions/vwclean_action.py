from .vwactions import VWPhysicalAction


class VWCleanAction(VWPhysicalAction):
    '''
    This class is a `VWPhysicalAction` that removes a `VWDirt` from the `VWCleaningAgent`'s current location.
    '''
    def __init__(self) -> None:
        super(VWCleanAction, self).__init__()
