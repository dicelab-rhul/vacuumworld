from __future__ import annotations
from enum import Enum
from random import choice


class VWUserDifficulty(Enum):
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

    def opposite(self) -> VWUserDifficulty:
        '''
        Returns the opposite of this `VWUserDifficulty`:

        * If this is `VWUserDifficulty.easy`, it returns `VWUserDifficulty.hard`.

        * If this is `VWUserDifficulty.hard`, it returns `VWUserDifficulty.easy`.
        '''
        if self == VWUserDifficulty.easy:
            return VWUserDifficulty.hard
        else:
            return VWUserDifficulty.easy

    @staticmethod
    def random() -> VWUserDifficulty:
        '''
        Returns a random `VWUserDifficulty` value.
        '''
        return choice(list(VWUserDifficulty))
