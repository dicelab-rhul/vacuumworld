from typing import Union

from .vwactions import VWCommunicativeAction
from ..actor.vwactor_appearance import VWActorAppearance


class VWBroadcastAction(VWCommunicativeAction):
    def __init__(self, message: Union[int, float, str, list, tuple, dict], actor_appearance: VWActorAppearance) -> None:
        super(VWBroadcastAction, self).__init__(message=message, recipients=[], actor_appearance=actor_appearance)
