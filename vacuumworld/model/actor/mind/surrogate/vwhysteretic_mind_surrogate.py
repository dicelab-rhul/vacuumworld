from typing import Iterable

# These imports must be absolute, otherwise the tests that require to load the class from file will fail.
from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from vacuumworld.model.actions.vwactions import VWAction
from vacuumworld.model.actions.vwidle_action import VWIdleAction


class VWHystereticMindSurrogate(VWActorMindSurrogate):
    '''
    This class specifies the hysteretic mind surrogate. It is a subclass of `VWActorMindSurrogate`.

    The `VWHystereticMindSurrogate` does nothing in `revise()` and always returns a single `VWIdleAction` in `decide()`.
    '''
    def revise(self) -> None:
        '''
        Does nothing.
        '''
        pass

    def decide(self) -> Iterable[VWAction]:
        '''
        Always returns a single `VWIdleAction`.
        '''
        return [VWIdleAction()]
