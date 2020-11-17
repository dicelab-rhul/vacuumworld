from .event import Event



class Action(Event):
    def __init__(self) -> None:
        super(Action, self).__init__()

        self.__actor_id: str = None

    def get_actor_id(self) -> str:
        return self.__actor_id

    def set_actor_id(self, actor_id: str) -> None:
        self.__actor_id = actor_id
