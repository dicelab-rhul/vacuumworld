from .vwactions import VWPhysicalAction



class VWMoveAction(VWPhysicalAction):
    __EFFORT: int = 1
    
    def __init__(self) -> None:
        super(VWMoveAction, self).__init__()

    @staticmethod
    def get_effort() -> int:
        return VWMoveAction.__EFFORT
    
    @staticmethod
    def override_default_effort(new_effort: int) -> None:
        VWMoveAction.__EFFORT = new_effort
