from ..elements.actor_appearance import ActorAppearance
from ..common.action import Action



class Mind():
    def __init__(self, body_appearance: ActorAppearance) -> None:
        self.__body_appearance: ActorAppearance = body_appearance

    def get_body_appearance(self) -> ActorAppearance:
        return self.__body_appearance

    def get_body_id(self) -> str:
        return self.__body_appearance.get_id()

    def get_body_progressive_id(self) -> str:
        return self.__body_appearance.get_progressive_id()

    def perceive(*_) -> None:
        # Abstract.
        pass

    def revise(*_) -> None:
        # Abstract.
        pass

    def decide(*_) -> Action:
        # Abstract.
        pass

    def execute(*_) -> None:
        # Abstract.
        pass
