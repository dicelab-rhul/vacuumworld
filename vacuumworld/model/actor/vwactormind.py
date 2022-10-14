from typing import Iterable, List, Tuple, Union

from pystarworldsturbo.elements.mind import Mind
from pystarworldsturbo.common.message import BccMessage

from .actor_mind_surrogate import ActorMindSurrogate
from ..actions.vwactions import VWAction
from ..actions.idle_action import VWIdleAction
from ...common.observation import Observation



class VWMind(Mind):
    PERCEIVE_METHOD_NAME: str = "perceive"
    REVISE_METHOD_NAME: str = "revise"
    DECIDE_METHOD_NAME: str = "decide"
    EXECUTE_METHOD_NAME: str = "execute"
    
    def __init__(self, surrogate: ActorMindSurrogate) -> None:
        super(VWMind, self).__init__()

        VWMind.__validate_surrogate(surrogate=surrogate)

        # This is to prevent that, when the simulation is stopped and the grid is cleared, the surrogates retain the values of their attributes.
        self.__surrogate: ActorMindSurrogate = self._clone_surrogate(surrogate=surrogate)
        del surrogate
        
        self.__next_actions: Tuple[VWAction] = None

    def get_surrogate(self) -> ActorMindSurrogate:
        return self.__surrogate
    
    # This method needs to be overridden by sub-classes.
    def _clone_surrogate(self, surrogate: ActorMindSurrogate) -> ActorMindSurrogate:
        return type(surrogate)()

    @staticmethod
    def __validate_surrogate(surrogate: ActorMindSurrogate) -> None:
        if not isinstance(surrogate, ActorMindSurrogate):
            raise ValueError("Invalid surrogate mind.")

        if not hasattr(surrogate, VWMind.REVISE_METHOD_NAME) or not callable(getattr(surrogate, VWMind.REVISE_METHOD_NAME)):
            raise ValueError("Invalid surrogate mind: no callable {}() method found.".format(VWMind.REVISE_METHOD_NAME))

        if not hasattr(surrogate, VWMind.DECIDE_METHOD_NAME) or not callable(getattr(surrogate, VWMind.DECIDE_METHOD_NAME)):
            raise ValueError("Invalid surrogate mind: no callable {}() method found.".format(VWMind.DECIDE_METHOD_NAME))

    def perceive(*_) -> None:
        # Not implemented, as the perception is initiated by the body.
        return

    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        assert hasattr(self.__surrogate, VWMind.REVISE_METHOD_NAME)
        assert callable(getattr(self.__surrogate, VWMind.REVISE_METHOD_NAME))
        
        if not observation:
            observation = Observation.create_empty_observation()

        if not messages:
            messages = []

        self.__surrogate.revise(observation=observation, messages=messages)

    def decide(self) -> None:
        assert hasattr(self.__surrogate, VWMind.DECIDE_METHOD_NAME)
        assert callable(getattr(self.__surrogate, VWMind.DECIDE_METHOD_NAME))

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
