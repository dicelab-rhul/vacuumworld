from typing import Iterable, Tuple, Union

from pystarworldsturbo.common.message import BccMessage
from pystarworldsturbo.utils.utils import ignore

# These imports must be absolute, otherwise the tests that require to load the class from file will fail.
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction
from vacuumworld.common.vwobservation import VWObservation


class VWHystereticMindSurrogate(VWActorMindSurrogate):
    '''
    This class specifies the hysteretic mind surrogate. It is a subclass of `VWActorMindSurrogate`.

    The `VWHystereticMindSurrogate` does nothing in `revise()` and always returns `VWIdleAction` in `decide()`.
    '''
    def revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None:
        '''
        Does nothing, and ignores both `observation` and `messages`.
        '''
        ignore(observation)

        for m in messages:
            ignore(m)

    def decide(self) -> Union[VWAction, Tuple[VWAction]]:
        '''
        Always returns `VWIdleAction`.
        '''
        return VWIdleAction()
