from typing import Union, Iterable

from .vwactions import VWCommunicativeAction
from .vwbroadcast_action import VWBroadcastAction
from .vweffort import VWActionEffort


class VWSpeakAction(VWCommunicativeAction):
    '''
    This class is a `VWCommunicativeAction` that sends a message to a `VWActor` (or more) in the `VWEnvironment`.

    An empty list of recipients is interpreted as a broadcast.
    '''
    def __init__(self, message: Union[int, float, str, bytes, list, tuple, dict], recipients: Iterable[str], sender_id: str) -> None:
        super(VWSpeakAction, self).__init__(message=message, recipients=recipients, sender_id=sender_id)

    def get_effort(self) -> int:
        '''
        Adjust the effort of this `VWSpeakAction` based on the number of recipients, and then returns it as an `int`.
        '''
        if type(self).__name__ in VWActionEffort.EFFORTS:
            if not self.get_recipients():
                return VWActionEffort.EFFORTS[VWBroadcastAction.__name__]
            else:
                return VWActionEffort.EFFORTS[type(self).__name__]
        else:
            return VWActionEffort.DEFAULT_EFFORT_FOR_OTHER_ACTIONS
