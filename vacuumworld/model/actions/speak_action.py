from typing import Union, Iterable

from .vwactions import VWCommunicativeAction
from ..actor.vwactor_appearance import VWActorAppearance



class VWSpeakAction(VWCommunicativeAction):
    def __init__(self, message: Union[int, float, str, list, tuple, dict], recipients: Iterable, actor_appearance: VWActorAppearance) -> None:
        super(VWSpeakAction, self).__init__(message=message, recipients=recipients, actor_appearance=actor_appearance)
