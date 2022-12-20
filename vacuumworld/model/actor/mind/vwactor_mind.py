from typing import Iterable, List

from pystarworldsturbo.elements.mind import Mind
from pystarworldsturbo.common.message import BccMessage

from .surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from ...actions.vwactions import VWAction
from ....common.vwobservation import VWObservation
from ....common.vwexceptions import VWActionAttemptException


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

        # `surrogate` has already been validated by the `VWRunner` constructor.

        # This is to prevent that, when the simulation is stopped and the grid is cleared, the surrogates retain the values of their attributes.
        self.__surrogate: VWActorMindSurrogate = self._clone_surrogate(surrogate=surrogate)
        del surrogate

        self.__next_actions: List[VWAction] = []

    def get_surrogate(self) -> VWActorMindSurrogate:
        '''
        Returns the `VWActorMindSurrogate` of this `VWMind`.
        '''
        return self.__surrogate

    # This method needs to be overridden by sub-classes.
    def _clone_surrogate(self, surrogate: VWActorMindSurrogate) -> VWActorMindSurrogate:
        return type(surrogate)()

    def reset_surrogate(self) -> None:
        '''
        Resets the `VWActorMindSurrogate` of this `VWMind`.
        '''
        self.__surrogate = self._clone_surrogate(surrogate=self.__surrogate)

    def perceive(self, observation: VWObservation, messages: Iterable[BccMessage]) -> None:
        '''
        Calls the `perceive()` method of the `VWActorMindSurrogate`, passing the `observation` and `messages` arguments.

        This method assumes (via assertions) that the `VWActorMindSurrogate` has a callable `perceive()` method which accepts the intended arguments.
        '''
        assert hasattr(self.__surrogate, VWMind.PERCEIVE_METHOD_NAME)
        assert callable(getattr(self.__surrogate, VWMind.PERCEIVE_METHOD_NAME))
        assert observation is not None
        assert isinstance(observation, VWObservation)
        assert messages is not None
        assert isinstance(messages, Iterable)

        self.__surrogate.perceive(observation=observation, messages=messages)

    def revise(self) -> None:
        '''
        Calls the `revise()` method of the `VWActorMindSurrogate`.

        This method assumes (via assertions) that the `VWActorMindSurrogate` has a callable `revise()` method.
        '''
        assert hasattr(self.__surrogate, VWMind.REVISE_METHOD_NAME)
        assert callable(getattr(self.__surrogate, VWMind.REVISE_METHOD_NAME))

        self.__surrogate.revise()

    def decide(self) -> None:
        '''
        Calls the `decide()` method of the `VWActorMindSurrogate`, and propagates (returns) its return value.

        This method assumes (via assertions) that the `VWActorMindSurrogate` has a callable `decide()` method which returns an appropriate value.
        '''
        assert hasattr(self.__surrogate, VWMind.DECIDE_METHOD_NAME)
        assert callable(getattr(self.__surrogate, VWMind.DECIDE_METHOD_NAME))

        actions: Iterable[VWAction] = self.__surrogate.decide()

        if actions is None:
            raise VWActionAttemptException("The `decide()` method of the surrogate mind must not return `None`.")
        elif isinstance(actions, Iterable):
            self.__store_actions_for_next_cycle(actions=actions)
        else:
            raise VWActionAttemptException("The `decide()` method of the surrogate mind must return an `Iterable[VWAction]`.")

    def __store_actions_for_next_cycle(self, actions: Iterable[VWAction]) -> None:
        sanitised_actions: List[VWAction] = []

        for action in actions:
            if action is None:
                raise VWActionAttemptException("The `decide()` method of the surrogate mind must not return an `Iterable` with `None` elements.")
            elif not isinstance(action, VWAction):
                raise VWActionAttemptException("The `decide()` method of the surrogate mind must return an `Iterable[VWAction]`.")
            else:
                sanitised_actions.append(action)

        self.__next_actions = sanitised_actions

    def execute(self) -> List[VWAction]:
        '''
        Returns a `List[VWAction]` consisting of each `VWAction` to be attempted.

        This method assumes (via assertion) that at least one `VWAction` is returned.
        '''
        assert len(self.__next_actions) > 0

        return self.__next_actions
