from .surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from .surrogate.vwuser_mind_surrogate import VWUserMindSurrogate
from .vwactor_mind import VWMind


class VWUserMind(VWMind):
    '''
    This class specifies the user mind. It is a subclass of `VWMind`.
    '''
    def __init__(self, surrogate: VWUserMindSurrogate) -> None:
        super(VWUserMind, self).__init__(surrogate=surrogate)

        assert isinstance(surrogate, VWUserMindSurrogate)

    def get_surrogate(self) -> VWUserMindSurrogate:
        '''
        Returns the `VWUserMindSurrogate` of this `VWUserMind`.
        '''
        surrogate: VWActorMindSurrogate = VWMind.get_surrogate(self)

        if isinstance(surrogate, VWUserMindSurrogate):
            return surrogate
        else:
            raise TypeError("The surrogate of a `VWUserMind` must be a `VWUserMindSurrogate`.")

    def _clone_surrogate(self, surrogate: VWActorMindSurrogate) -> VWUserMindSurrogate:
        if not isinstance(surrogate, VWUserMindSurrogate):
            raise TypeError("The surrogate of a `VWUserMind` must be a `VWUserMindSurrogate`.")
        else:
            return VWUserMindSurrogate(difficulty_level=surrogate.get_difficulty_level())
