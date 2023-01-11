from vacuumworld.model.actor.mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate


class DanceMind(VWActorMindSurrogate):
    def __init__(self):
        super(DanceMind, self).__init__()

        self.__tick: int = 0

    def get_tick(self) -> int:
        return self.__tick

    def revise(self) -> None:
        '''
        This is the base revise function for updating the agent state.

        It calls a sub_revise function which can be overridden by child minds. This way they
        can add their own behaviours without overwriting the base behaviours from this mind.
        '''
        self.__tick += 1

        self.sub_revise()

    def sub_revise(self):
        raise NotImplementedError()
