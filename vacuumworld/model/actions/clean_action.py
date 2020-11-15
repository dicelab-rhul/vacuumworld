from .vwactions import VWPhysicalAction
from ..actor.vwactor_appearance import VWActorAppearance



class VWCleanAction(VWPhysicalAction):
    def __init__(self, actor_appearance: VWActorAppearance) -> None:
        super(VWCleanAction, self).__init__(actor_appearance=actor_appearance)
