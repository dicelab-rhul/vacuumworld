from typing import Iterable, Tuple, Union

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from ..actions.vwactions import VWAction
from ..actions.idle_action import VWIdleAction
from ...common.observation import Observation



class ActorMindSurrogate():
    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        # Abstract.
        ignore(self)
        ignore(observation)
        ignore(messages)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        # Abstract.
        ignore(self)

        return VWIdleAction()
