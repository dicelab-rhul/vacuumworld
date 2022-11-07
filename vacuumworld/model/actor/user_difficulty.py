from __future__ import annotations
from enum import Enum
from random import choice


class UserDifficulty(Enum):
    '''
    This `Enum` specifies the behaviour of a `VWUser`.

    * `easy` means that the `VWUser` will not try to avoid any `VWCleaningAgent`.
    * `hard` means that the `VWUser` will try to avoid any `VWCleaningAgent` it sees.
    '''
    easy = 0
    hard = 1

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)

    def toggle(self) -> UserDifficulty:
        if self == UserDifficulty.easy:
            return UserDifficulty.hard
        else:
            return UserDifficulty.easy

    @staticmethod
    def random() -> UserDifficulty:
        return choice(list(UserDifficulty))
