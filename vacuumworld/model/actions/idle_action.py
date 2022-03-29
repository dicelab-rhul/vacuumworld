from .vwactions import VWPhysicalAction



class VWIdleAction(VWPhysicalAction):
    __EFFORT: int = 1
    
    def __init__(self) -> None:
        super(VWIdleAction, self).__init__()

    @staticmethod
    def get_effort() -> int:
        return VWIdleAction.__EFFORT
    
    @staticmethod
    def override_default_effort(new_effort: int) -> None:
        VWIdleAction.__EFFORT = new_effort
