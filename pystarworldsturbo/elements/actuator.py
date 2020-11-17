from typing import List, Type, Union, Iterable
from queue import Queue

from ..common.action import Action



class Actuator():
    def __init__(self, subscribed_events: List[Type]=[]) -> None:
        self.__subscribed_events: List[Type] = subscribed_events
        self.__action_buffer: Queue[Action] = Queue()

    def subscribe_to_event_type(self, event_type: Type) -> None:
        if not isinstance(event_type, Type) or not issubclass(event_type, Action):
            raise ValueError("Cannot subscribe to something which is not a type of Action.")
        elif event_type in self.__subscribed_events:
            # We do not need to re-subscribe.
            pass
        else:
            self.__subscribed_events.append(event_type)

    def unsubscribe_from_event_type(self, event_type: Type) -> None:
        if not isinstance(event_type, Type) or not issubclass(event_type, Action):
            raise ValueError("Cannot unsubscribe from something which is not a type of Action.")
        elif event_type not in self.__subscribed_events:
            # We do not need to unsubscribe.
            pass
        else:
            self.__subscribed_events.remove(event_type)

    def is_subscribed_to(self, event_type: Type) -> bool:
        return event_type in self.__subscribed_events

    def sink(self, action: Action) -> None:
        assert self.is_subscribed_to(event_type=type(action))

        self.__action_buffer.put(action)

    def has_pending_actions(self) -> bool:
        return not self.__action_buffer.empty()

    def source(self) -> Union[Action, Iterable[Action]]:
        if not self.__action_buffer.empty():
            return self.__action_buffer.get()
        else:
            return None
