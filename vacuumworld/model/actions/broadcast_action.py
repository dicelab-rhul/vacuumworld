from typing import Union

from .vwactions import VWCommunicativeAction


class VWBroadcastAction(VWCommunicativeAction):
    def __init__(self, message: Union[int, float, str, list, tuple, dict], sender_id: str) -> None:
        super(VWBroadcastAction, self).__init__(message=message, recipients=[], sender_id=sender_id)
