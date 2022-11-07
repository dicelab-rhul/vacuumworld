from typing import Iterable, Tuple, Union

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

from vacuumworld.common.observation import Observation
from vacuumworld.model.actor.actor_mind_surrogate import ActorMindSurrogate
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.idle_action import VWIdleAction


class VWHystereticMindSurrogate(ActorMindSurrogate):
    '''
    This class specifies the hysteretic mind surrogate. It is a subclass of `ActorMindSurrogate`.

    The `VWHystereticMindSurrogate` does nothing in `revise()` and always returns `VWIdleAction` in `decide()`.
    '''
    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        '''
        Does nothing, and ignores both `observation` and `messages`.
        '''
        ignore(self)
        ignore(observation)

        for m in messages:
            ignore(m)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        '''
        Always returns `VWIdleAction`.
        '''
        ignore(self)

        return VWIdleAction()
