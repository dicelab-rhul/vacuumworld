from .vwactions import VWPhysicalAction


class VWIdleAction(VWPhysicalAction):
    def __init__(self) -> None:
        super(VWIdleAction, self).__init__()
