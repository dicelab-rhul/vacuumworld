from typing import override
from abc import abstractmethod

from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate


class DanceMind(VWActorMindSurrogate):
    def __init__(self) -> None:
        super(DanceMind, self).__init__()

        self.__tick: int = 0

    def get_tick(self) -> int:
        return self.__tick

    @override
    def revise(self) -> None:
        '''
        This is the base revise function for updating the agent state.

        It calls a sub_revise function which can be overridden by child minds. This way they
        can add their own behaviours without overwriting the base behaviours from this mind.
        '''
        self.__tick += 1

        self.sub_revise()

    @abstractmethod
    def sub_revise(self) -> None:
        ...
