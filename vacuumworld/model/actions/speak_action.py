from typing import Union, Iterable

from .vwactions import VWCommunicativeAction
from .broadcast_action import VWBroadcastAction
from .effort import ActionEffort


class VWSpeakAction(VWCommunicativeAction):
    def __init__(self, message: Union[int, float, str, bytes, list, tuple, dict], recipients: Iterable[str], sender_id: str) -> None:
        super(VWSpeakAction, self).__init__(message=message, recipients=recipients, sender_id=sender_id)

    def get_effort(self) -> ActionEffort:
        if type(self).__name__ in ActionEffort.EFFORTS:
            if not self.get_recipients():
                return ActionEffort.EFFORTS[VWBroadcastAction.__name__]
            else:
                return ActionEffort.EFFORTS[type(self).__name__]
        else:
            return ActionEffort.DEFAULT_EFFORT_FOR_OTHER_ACTIONS
