from .vwactions import VWPhysicalAction



class VWCleanAction(VWPhysicalAction):
    __EFFORT: int = 1
    
    def __init__(self) -> None:
        super(VWCleanAction, self).__init__()
        
    @staticmethod
    def get_effort() -> int:
        return VWCleanAction.__EFFORT
    
    @staticmethod
    def override_default_effort(new_effort: int) -> None:
        VWCleanAction.__EFFORT = new_effort
