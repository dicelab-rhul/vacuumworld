from typing import Union

from .vwactions import VWCommunicativeAction


class VWBroadcastAction(VWCommunicativeAction):
    __EFFORT: int = 1
    
    def __init__(self, message: Union[int, float, str, list, tuple, dict], sender_id: str) -> None:
        super(VWBroadcastAction, self).__init__(message=message, recipients=[], sender_id=sender_id)
        
    @staticmethod
    def get_effort() -> int:
        return VWBroadcastAction.__EFFORT
    
    @staticmethod
    def override_default_effort(new_effort: int) -> None:
        VWBroadcastAction.__EFFORT = new_effort
