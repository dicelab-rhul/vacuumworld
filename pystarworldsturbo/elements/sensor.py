from typing import List, Type
from queue import Queue

from ..common.perception import Perception



class Sensor():
    def __init__(self, subscribed_events: List[Type]=[]) -> None:
        self.__subscribed_events: List[Type] = subscribed_events
        self.__perception_buffer: Queue[Perception] = Queue()

    def subscribe_to_event_type(self, event_type: Type) -> None:
        if not isinstance(event_type, Type) or not issubclass(event_type, Perception):
            raise ValueError("Cannot subscribe to something which is not a type of Perception.")
        elif event_type in self.__subscribed_events:
            # We do not need to re-subscribe.
            pass
        else:
            self.__subscribed_events.append(event_type)

    def unsubscribe_from_event_type(self, event_type: Type) -> None:
        if not isinstance(event_type, Type) or not issubclass(event_type, Perception):
            raise ValueError("Cannot unsubscribe from something which is not a type of Perception.")
        elif event_type not in self.__subscribed_events:
            # We do not need to unsubscribe.
            pass
        else:
            self.__subscribed_events.remove(event_type)

    def is_subscribed_to(self, event_type: Type) -> bool:
        return event_type in self.__subscribed_events

    def sink(self, perception: Perception) -> None:
        assert self.is_subscribed_to(type(perception))

        self.__perception_buffer.put(perception)

    def has_perception(self) -> bool:
        return not self.__perception_buffer.empty()

    def source(self) -> Perception:
        if not self.__perception_buffer.empty():
            return self.__perception_buffer.get()
        else:
            return None
