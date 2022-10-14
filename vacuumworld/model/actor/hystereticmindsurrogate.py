from typing import Iterable, Tuple, Union

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from vacuumworld.common.observation import Observation
from vacuumworld.model.actor.actor_mind_surrogate import ActorMindSurrogate
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.idle_action import VWIdleAction


class VWHystereticMindSurrogate(ActorMindSurrogate):
    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        ignore(self)
        ignore(observation)

        for m in messages:
            ignore(m)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        ignore(self)

        return VWIdleAction()
