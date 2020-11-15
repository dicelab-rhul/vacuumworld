from pystarworldsturbo.elements.actor_appearance import ActorAppearance
from .event import Event



class Action(Event):
    def __init__(self, actor_appearance: ActorAppearance=None) -> None:
        super(Action, self).__init__()

        self.__actor_appearance: ActorAppearance = actor_appearance

    def get_actor_appearance(self) -> ActorAppearance:
        return self.__actor_appearance

    def set_actor_appearance(self, actor_appearance: ActorAppearance) -> None:
        self.__actor_appearance = actor_appearance
