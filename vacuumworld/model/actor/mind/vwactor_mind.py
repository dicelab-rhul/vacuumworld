from typing import Iterable, List, Tuple, Union

from pystarworldsturbo.elements.mind import Mind
from pystarworldsturbo.common.message import BccMessage

from .surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from ...actions.vwactions import VWAction
from ...actions.vwidle_action import VWIdleAction
from ....common.vwobservation import VWObservation


class VWMind(Mind):
    '''
    This class specifies the mind of a `VWActor`.

    The mind has a surrogate, which is an instance of a class that extends `VWActorMindSurrogate`. The surrogate is used to store the state of the mind, and to implement `revise()`, and `decide()`.

    The mind implements the `perceive()` and `execute()` methods that are called by the body together with `revise()` and `decide()` during the `VWActor` cycle.
    '''
    PERCEIVE_METHOD_NAME: str = "perceive"
    REVISE_METHOD_NAME: str = "revise"
    DECIDE_METHOD_NAME: str = "decide"
    EXECUTE_METHOD_NAME: str = "execute"

    def __init__(self, surrogate: VWActorMindSurrogate) -> None:
        super(VWMind, self).__init__()

        VWMind.__validate_surrogate(surrogate=surrogate)

        # This is to prevent that, when the simulation is stopped and the grid is cleared, the surrogates retain the values of their attributes.
        self.__surrogate: VWActorMindSurrogate = self._clone_surrogate(surrogate=surrogate)
        del surrogate

        self.__next_actions: Tuple[VWAction] = None

    def get_surrogate(self) -> VWActorMindSurrogate:
        '''
        Returns the `VWActorMindSurrogate` of this `VWMind`.
        '''
        return self.__surrogate

    # This method needs to be overridden by sub-classes.
    def _clone_surrogate(self, surrogate: VWActorMindSurrogate) -> VWActorMindSurrogate:
        return type(surrogate)()

    @staticmethod
    def __validate_surrogate(surrogate: VWActorMindSurrogate) -> None:
        if not isinstance(surrogate, VWActorMindSurrogate):
            raise ValueError("Invalid surrogate mind.")

        if not hasattr(surrogate, VWMind.REVISE_METHOD_NAME) or not callable(getattr(surrogate, VWMind.REVISE_METHOD_NAME)):
            raise ValueError("Invalid surrogate mind: no callable {}() method found.".format(VWMind.REVISE_METHOD_NAME))

        if not hasattr(surrogate, VWMind.DECIDE_METHOD_NAME) or not callable(getattr(surrogate, VWMind.DECIDE_METHOD_NAME)):
            raise ValueError("Invalid surrogate mind: no callable {}() method found.".format(VWMind.DECIDE_METHOD_NAME))

    def reset_surrogate(self) -> None:
        '''
        Resets the `VWActorMindSurrogate` of this `VWMind`.
        '''
        self.__surrogate = self._clone_surrogate(surrogate=self.__surrogate)

    def perceive(*_) -> None:
        '''
        Not implemented, as the perception is initiated by the body.
        '''

    def revise(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None:
        '''
        Calls the `revise()` method of the `VWActorMindSurrogate`, passing the `observation` and `messages` arguments.

        This method assumes (via assertions) that the `VWActorMindSurrogate` has a callable `revise()` method which accepts the intended arguments.
        '''
        assert hasattr(self.__surrogate, VWMind.REVISE_METHOD_NAME)
        assert callable(getattr(self.__surrogate, VWMind.REVISE_METHOD_NAME))

        if not observation:
            observation = VWObservation.create_empty_observation()

        if not messages:
            messages = []

        self.__surrogate.revise(observation=observation, messages=messages)

    def decide(self) -> None:
        '''
        Calls the `decide()` method of the `VWActorMindSurrogate`, and propagates (returns) its return value.

        This method assumes (via assertions) that the `VWActorMindSurrogate` has a callable `decide()` method which returns an appropriate value.
        '''
        assert hasattr(self.__surrogate, VWMind.DECIDE_METHOD_NAME)
        assert callable(getattr(self.__surrogate, VWMind.DECIDE_METHOD_NAME))

        actions: Union[VWAction, Tuple[VWAction]] = self.__surrogate.decide()

        if actions is None:
            self.__next_actions = (VWIdleAction(),)  # For safety and back compatibility with 4.1.8.
        elif type(actions) == tuple:
            self.__store_actions_for_next_cycle(actions=actions)
        else:
            assert isinstance(actions, VWAction)
            self.__next_actions = (actions,)

    def __store_actions_for_next_cycle(self, actions: Tuple[VWAction]) -> None:
        sanitised_actions: List[VWAction] = []

        for action in actions:
            if action is None:
                sanitised_actions.append(VWIdleAction())  # For safety and back compatibility with 4.1.8.
            else:
                assert isinstance(action, VWAction)
                sanitised_actions.append(action)

        self.__next_actions = tuple(sanitised_actions)

    def execute(self) -> Tuple[VWAction]:
        '''
        Returns a Tuple[VWAction] consisting of each `VWAction` to be attempted.

        This method assumes (via assertion) that at least one `VWAction` is returned.
        '''
        assert len(self.__next_actions) > 0

        return self.__next_actions
