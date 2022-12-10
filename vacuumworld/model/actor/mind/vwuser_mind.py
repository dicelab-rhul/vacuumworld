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
        return VWMind.get_surrogate(self)

    def _clone_surrogate(self, surrogate: VWUserMindSurrogate) -> VWUserMindSurrogate:
        return VWUserMindSurrogate(difficulty_level=surrogate.get_difficulty_level())
