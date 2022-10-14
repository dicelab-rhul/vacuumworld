from typing import Union, Iterable

from .vwactions import VWCommunicativeAction


class VWSpeakAction(VWCommunicativeAction):
    def __init__(self, message: Union[int, float, str, list, tuple, dict], recipients: Iterable, sender_id: str) -> None:
        super(VWSpeakAction, self).__init__(message=message, recipients=recipients, sender_id=sender_id)
