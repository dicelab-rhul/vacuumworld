from typing import Union

from .vwactions import VWCommunicativeAction


class VWBroadcastAction(VWCommunicativeAction):
    '''
    This class is a `VWCommunicativeAction` that broadcasts a message to each `VWActor` in the `VWEnvironment`.
    '''
    def __init__(self, message: Union[int, float, str, bytes, list, tuple, dict], sender_id: str) -> None:
        super(VWBroadcastAction, self).__init__(message=message, recipients=[], sender_id=sender_id)
