from enum import Enum



class UserDifficulty(Enum):
    easy = 0
    hard = 1

    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return str(self)

    def toggle(self) -> "UserDifficulty":
        if self == UserDifficulty.easy:
            return UserDifficulty.hard
        else:
            return UserDifficulty.easy
