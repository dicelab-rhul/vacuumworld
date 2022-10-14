from .user_mind_surrogate import UserMindSurrogate
from .vwactormind import VWMind



class VWUserMind(VWMind):
    def __init__(self, surrogate: UserMindSurrogate) -> None:
        super(VWUserMind, self).__init__(surrogate=surrogate)

    def get_surrogate(self) -> UserMindSurrogate:
        return VWMind.get_surrogate(self)

    def _clone_surrogate(self, surrogate: UserMindSurrogate) -> UserMindSurrogate:
        return UserMindSurrogate(difficulty_level=surrogate.get_difficulty_level())
