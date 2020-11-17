from typing import Iterable, Tuple, Union

from pystarworldsturbo.common.message import BccMessage

from ..actions.vwactions import VWAction
from ..actions.idle_action import VWIdleAction
from ...common.observation import Observation



class ActorMindSurrogate():
    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        # Abstract.
        pass

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        # Abstract.

        return VWIdleAction()
