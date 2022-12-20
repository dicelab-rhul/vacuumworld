from typing import List, Iterable
from random import random
from itertools import accumulate

from .vwactor_mind_surrogate import VWActorMindSurrogate
from .....common.vwuser_difficulty import VWUserDifficulty
from ....actions.vwactions import VWPhysicalAction
from ....actions.vwmove_action import VWMoveAction
from ....actions.vwturn_action import VWTurnAction
from ....actions.vwdrop_action import VWDropAction
from ....actions.vwidle_action import VWIdleAction
from .....common.vwcolour import VWColour
from .....common.vwdirection import VWDirection


class VWUserMindSurrogate(VWActorMindSurrogate):
    '''
    This class specifies the surrogate of a `VWUserMind` of a `VWUser`.

    It is used to simulate the behaviour of a `VWUser` in the `VWEnvironment`.
    '''
    def __init__(self, difficulty_level: VWUserDifficulty=VWUserDifficulty.easy) -> None:
        super(VWUserMindSurrogate, self).__init__()

        assert type(difficulty_level) == VWUserDifficulty

        self.__difficulty_level: VWUserDifficulty = difficulty_level

    def get_difficulty_level(self) -> VWUserDifficulty:
        '''
        Returns the `VWUserDifficulty` of this `VWUserMindSurrogate`.
        '''
        return self.__difficulty_level

    def set_difficulty_level(self, difficulty_level: VWUserDifficulty) -> None:
        '''
        Sets the `VWUserDifficulty` of this `VWUserMindSurrogate`.
        '''
        self.__difficulty_level = difficulty_level

    def __is_on_dirt(self) -> bool:
        return self.get_latest_observation().get_center().filter(lambda center: center.has_dirt()).is_present()

    def __is_actor_ahead(self) -> bool:
        return not self.get_latest_observation().is_wall_immediately_ahead() and self.get_latest_observation().get_forward().filter(lambda forward: forward.has_actor()).is_present()

    def __is_actor_on_the_left(self) -> bool:
        return not self.get_latest_observation().is_wall_immediately_to_the_left() and self.get_latest_observation().get_left().filter(lambda left: left.has_actor()).is_present()

    def __is_actor_on_the_right(self) -> bool:
        return not self.get_latest_observation().is_wall_immediately_to_the_right() and self.get_latest_observation().get_right().filter(lambda right: right.has_actor()).is_present()

    def revise(self) -> None:
        '''
        The `VWUser` does not need to revise anything.
        '''
        pass

    def decide(self) -> Iterable[VWPhysicalAction]:
        '''
        Decides the next `VWPhysicalAction` to be attempted by the `VWUser` associated with this `VWUserMindSurrogate`.

        * If no `VWObservation` has been received yet, returns `VWIdleAction`.

        * If the `VWUserDifficulty` of this `VWUserMindSurrogate` is `VWUserDifficulty.easy`, then the `VWUser` will not try to avoid any other `VWActor`.

        * If the `VWUserDifficulty` of this `VWUserMindSurrogate` is `VWUserDifficulty.hard`, then the `VWUser` will try to avoid each `VWActor` that comes too close.
        '''
        if not self.get_latest_observation():
            return [VWIdleAction()]
        elif self.__difficulty_level == VWUserDifficulty.easy:
            return [self.__be_kind()]
        elif self.__difficulty_level == VWUserDifficulty.hard:
            return [self.__be_inconsiderate()]
        else:
            raise ValueError("Unrecognised user difficulty level: {}.".format(self.__difficulty_level))

    def __be_kind(self) -> VWPhysicalAction:
        if self.get_latest_observation().is_wall_immediately_ahead():
            return self.__decide_if_wall_ahead_and_kind()
        elif self.__is_on_dirt():
            # If there is already a dirt on this location, move or turn.
            return self.__decide_if_on_dirt_and_kind()
        else:
            # Otherwise, do a random action (including dropping dirt).
            return VWUserMindSurrogate.__act_randomly(weights=[0.2, 0.2, 0.45, 0.075, 0.075])

    def __decide_if_wall_ahead_and_kind(self) -> VWPhysicalAction:
        if self.get_latest_observation().is_wall_immediately_to_the_left():
            return VWTurnAction(direction=VWDirection.right)
        elif self.get_latest_observation().is_wall_immediately_to_the_right():
            return VWTurnAction(direction=VWDirection.left)
        else:
            return VWUserMindSurrogate.__turn_randomly()

    def __decide_if_on_dirt_and_kind(self) -> VWPhysicalAction:
        if self.get_latest_observation().is_wall_immediately_to_the_left():
            return VWUserMindSurrogate.__move_randomly(weights=[0.6, 0.0, 0.4])
        elif self.get_latest_observation().is_wall_immediately_to_the_right():
            return VWUserMindSurrogate.__move_randomly(weights=[0.6, 0.4, 0.0])
        else:
            return VWUserMindSurrogate.__move_randomly(weights=[0.5, 0.25, 0.25])

    @staticmethod
    def __turn_randomly() -> VWPhysicalAction:
        if random() < 0.5:
            return VWTurnAction(direction=VWDirection.left)
        else:
            return VWTurnAction(direction=VWDirection.right)

    @staticmethod
    def __drop_random_dirt() -> VWPhysicalAction:
        if random() < 0.5:
            return VWDropAction(dirt_colour=VWColour.green)
        else:
            return VWDropAction(dirt_colour=VWColour.orange)

    @staticmethod
    def __move_randomly(weights: List[float]=[1/3, 1/3, 1/3]) -> VWPhysicalAction:
        assert type(weights) == list and len(weights) == 3 and sum(weights) == 1.0

        return VWUserMindSurrogate.__act_randomly(weights=[0.0, 0.0, weights[0], weights[1], weights[2]])

    @staticmethod
    def __move_or_drop_randomly(weights: List[float]=[1/3, 1/3, 1/3]) -> VWPhysicalAction:
        assert type(weights) == list and len(weights) == 3 and sum(weights) == 1.0

        return VWUserMindSurrogate.__act_randomly(weights=[weights[0], weights[1], weights[2], 0.0, 0.0])

    @staticmethod
    def __act_randomly(weights: List[float]=[0.2, 0.2, 0.2, 0.2, 0.2]) -> VWPhysicalAction:
        assert type(weights) == list and len(weights) == 5 and sum(weights) == 1.0

        rng_thresholds: List[float] = list(accumulate(weights))

        random_number: float = random()

        if random_number < rng_thresholds[0]:
            return VWDropAction(dirt_colour=VWColour.green)
        elif random_number < rng_thresholds[1]:
            return VWDropAction(dirt_colour=VWColour.orange)
        elif random_number < rng_thresholds[2]:
            return VWMoveAction()
        elif random_number < rng_thresholds[3]:
            return VWTurnAction(direction=VWDirection.left)
        else:
            return VWTurnAction(direction=VWDirection.right)

    def __be_inconsiderate(self) -> VWPhysicalAction:
        # Wall ahead.
        if self.get_latest_observation().is_wall_immediately_ahead():
            return self.__decide_if_wall_ahead_and_inconsiderate()
        # Actor ahead.
        elif self.__is_actor_ahead():
            return self.__decide_if_agent_ahead_and_inconsiderate()
        # Both right and left occupied by actors.
        elif self.__is_actor_on_the_left() and self.__is_actor_on_the_right():
            return VWUserMindSurrogate.__move_or_drop_randomly(weights=[0.1, 0.1, 0.8])
        # Actor on the left and no wall on the right.
        elif self.__is_actor_on_the_left() and not self.get_latest_observation().is_wall_immediately_to_the_right():
            return VWUserMindSurrogate.__move_randomly(weights=[0.5, 0.0, 0.5])
        # Actor on the right and no wall on the left.
        elif self.__is_actor_on_the_right() and not self.get_latest_observation().is_wall_immediately_to_the_left():
            return VWUserMindSurrogate.__move_randomly(weights=[0.5, 0.5, 0.0])
        # Wall on the left.
        elif self.get_latest_observation().is_wall_immediately_to_the_left():
            return self.__decide_if_wall_on_the_left_and_inconsiderate()
        # Wall on the right.
        elif self.get_latest_observation().is_wall_immediately_to_the_right():
            return self.__decide_if_wall_on_the_right_and_inconsiderate()
        # Any other possibility.
        else:
            return self.__act_randomly(weights=[0.15, 0.15, 0.6, 0.05, 0.05])

        # Always wall ahead
    def __decide_if_wall_ahead_and_inconsiderate(self) -> VWPhysicalAction:
        if self.get_latest_observation().is_wall_immediately_to_the_left():  # Wall on the left.
            return VWTurnAction(direction=VWDirection.right)
        elif self.get_latest_observation().is_wall_immediately_to_the_right():  # Wall on the right.
            return VWTurnAction(direction=VWDirection.left)
        elif self.__is_actor_on_the_left() and self.__is_actor_on_the_right():  # Both left and right are occupied by actors.
            return VWUserMindSurrogate.__turn_randomly()
        elif self.__is_actor_on_the_left():  # Actor on the left.
            return VWTurnAction(direction=VWDirection.right)
        elif self.__is_actor_on_the_right():  # Actor on the right.
            return VWTurnAction(direction=VWDirection.left)
        elif self.__is_on_dirt():  # Both left and right are free.
            return VWUserMindSurrogate.__turn_randomly()
        else:  # Wall ahead, left and right free, no dirt on center.
            return self.__act_randomly(weights=[0.075, 0.075, 0.6, 0.0, 0.25])

    # Always actor ahead.
    def __decide_if_agent_ahead_and_inconsiderate(self) -> VWPhysicalAction:
        if self.get_latest_observation().is_wall_immediately_to_the_left():  # Wall on the left.
            return VWTurnAction(direction=VWDirection.right)
        elif not self.get_latest_observation().is_wall_immediately_to_the_right():  # Wall on the right.
            return VWTurnAction(direction=VWDirection.left)
        elif self.__is_actor_on_the_left() and self.__is_actor_on_the_right():  # Both left and right are occupied by actors.
            return self.__drop_random_dirt()  # Dropping a dirt in front of the actor, if possible.
        elif self.__is_actor_on_the_left():  # Actor on the left.
            return VWTurnAction(direction=VWDirection.right)
        elif self.__is_actor_on_the_right():  # Actor on the right.
            return VWTurnAction(direction=VWDirection.left)
        elif self.__is_on_dirt():  # Both left and right are free.
            return VWUserMindSurrogate.__turn_randomly()
        else:
            return VWUserMindSurrogate.__act_randomly(weights=[0.25, 0.25, 0.0, 0.25, 0.25])

    # Always wall on the left.
    def __decide_if_wall_on_the_left_and_inconsiderate(self) -> VWPhysicalAction:
        if self.__is_on_dirt():
            return VWUserMindSurrogate.__move_randomly(weights=[0.9, 0.0, 0.1])
        else:
            return VWUserMindSurrogate.__act_randomly(weights=[0.075, 0.075, 0.6, 0.0, 0.25])

    # Always wall on the right.
    def __decide_if_wall_on_the_right_and_inconsiderate(self) -> VWPhysicalAction:
        if self.__is_on_dirt():
            return VWUserMindSurrogate.__move_randomly(weights=[0.9, 0.1, 0.0])
        else:
            return VWUserMindSurrogate.__act_randomly(weights=[0.075, 0.075, 0.6, 0.25, 0.0])
