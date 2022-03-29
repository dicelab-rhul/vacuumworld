from typing import Union, Iterable

from .vwactions import VWCommunicativeAction



class VWSpeakAction(VWCommunicativeAction):
    __EFFORT: int = 1
    
    def __init__(self, message: Union[int, float, str, list, tuple, dict], recipients: Iterable, sender_id: str) -> None:
        super(VWSpeakAction, self).__init__(message=message, recipients=recipients, sender_id=sender_id)

    @staticmethod
    def get_effort() -> int:
        return VWSpeakAction.__EFFORT
    
    @staticmethod
    def override_default_effort(new_effort: int) -> None:
        VWSpeakAction.__EFFORT = new_effort
