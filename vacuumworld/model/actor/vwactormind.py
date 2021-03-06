from typing import Iterable, List, Tuple, Union

from pystarworldsturbo.elements.mind import Mind
from pystarworldsturbo.common.message import BccMessage

from .actor_mind_surrogate import ActorMindSurrogate
from ..actions.vwactions import VWAction
from ..actions.idle_action import VWIdleAction
from ...common.observation import Observation



class VWMind(Mind):
    def __init__(self, surrogate: ActorMindSurrogate) -> None:
        super(VWMind, self).__init__()

        VWMind.__validate_surrogate(surrogate=surrogate)

        self.__surrogate: ActorMindSurrogate = surrogate
        self.__next_actions: Tuple[VWAction] = None

    def get_surrogate(self) -> ActorMindSurrogate:
        return self.__surrogate

    @staticmethod
    def __validate_surrogate(surrogate: ActorMindSurrogate) -> None:
        if not isinstance(surrogate, ActorMindSurrogate):
            raise ValueError("Invalid surrogate mind.")

        if not hasattr(surrogate, "revise") or not callable(getattr(surrogate, "revise")):
            raise ValueError("Invalid surrogate mind: no revise() method found.")

        if not hasattr(surrogate, "decide") or not callable(getattr(surrogate, "decide")):
            raise ValueError("Invalid surrogate mind: no decide() method found.")

    def perceive(*_) -> None:
        return

    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        assert hasattr(self.__surrogate, "revise")
        assert callable(getattr(self.__surrogate, "revise"))
        
        if not observation:
            observation = Observation.create_empty_observation()

        if not messages:
            messages = []

        self.__surrogate.revise(observation=observation, messages=messages)

    def decide(self) -> None:
        assert hasattr(self.__surrogate, "decide")
        assert callable(getattr(self.__surrogate, "decide"))

        actions: Union[VWAction, Tuple[VWAction]] = self.__surrogate.decide()

        if actions is None:
            self.__next_actions = (VWIdleAction(),) # For safety and back compatibility with 4.1.8.
        elif type(actions) == tuple:
            self.__store_actions_for_next_cycle(actions=actions)
        else:
            assert isinstance(actions, VWAction)
            self.__next_actions = (actions,)

    def __store_actions_for_next_cycle(self, actions: Tuple[VWAction]) -> None:
        sanitised_actions: List[VWAction] = []

        for action in actions:
            if action is None:
                sanitised_actions.append(VWIdleAction()) # For safety and back compatibility with 4.1.8.
            else:
                assert isinstance(action, VWAction)
                sanitised_actions.append(action)

        self.__next_actions = tuple(sanitised_actions)

    def execute(self) -> Tuple[VWAction]:
        assert len(self.__next_actions) > 0
        

        return self.__next_actions
