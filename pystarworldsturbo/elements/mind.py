from typing import Tuple

from ..common.action import Action



class Mind():
    def perceive(*_) -> None:
        # Abstract.
        pass

    def revise(*_) -> None:
        # Abstract.
        pass

    def decide(*_) -> None:
        # Abstract.
        pass

    def execute(*_) -> Tuple[Action]:
        # Abstract.
        pass
