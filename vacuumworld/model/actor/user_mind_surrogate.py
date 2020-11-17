from typing import Iterable, List
from random import random
from itertools import accumulate

from pystarworldsturbo.common.message import BccMessage

from .actor_mind_surrogate import ActorMindSurrogate
from .user_difficulty import UserDifficulty
from ..actions.vwactions import VWPhysicalAction
from ..actions.move_action import VWMoveAction
from ..actions.turn_action import VWTurnAction
from ..actions.drop_action import VWDropAction
from ..actions.idle_action import VWIdleAction
from ...common.observation import Observation
from ...common.colour import Colour
from ...common.direction import Direction
from ...utils.vwutils import ignore



class UserMindSurrogate(ActorMindSurrogate):
    def __init__(self, difficulty_level: UserDifficulty=UserDifficulty.easy) -> None:
        assert type(difficulty_level) == UserDifficulty

        self.__difficulty_level: UserDifficulty = difficulty_level
        self.__observation: Observation = None

    def get_difficulty_level(self) -> int:
        return self.__difficulty_level

    def set_difficulty_level(self, difficulty_level: UserDifficulty) -> None:
        self.__difficulty_level = difficulty_level

    def __is_wall_ahead(self) -> bool:
        return not self.__observation.get_forward()

    def __is_wall_on_the_left(self) -> bool:
        return not self.__observation.get_left()

    def __is_wall_on_the_right(self) -> bool:
        return not self.__observation.get_right()

    def __is_on_dirt(self) -> bool:
        return self.__observation.get_center().has_dirt()

    def __is_actor_ahead(self) -> bool:
        return self.__observation.get_forward() and self.__observation.get_forward().has_actor()

    def __is_actor_on_the_left(self) -> bool:
        return self.__observation.get_left() and self.__observation.get_left().has_actor()

    def __is_actor_on_the_right(self) -> bool:
        return self.__observation.get_right() and self.__observation.get_right().has_actor()

    def revise(self, observation: Observation, messages: Iterable[BccMessage]) -> None:
        self.__observation: Observation = observation

        # print("Observation: {}".format(self.__observation))

        ignore(messages)

    def decide(self) -> VWPhysicalAction:
        if not self.__observation:
            return VWIdleAction()
        elif self.__difficulty_level == UserDifficulty.easy:
            return self.__be_kind()
        elif self.__difficulty_level == UserDifficulty.hard:
            return self.__be_inconsiderate()
        else:
            raise ValueError("Unrecognised user difficulty level: {}.".format(self.__difficulty_level))

    def __be_kind(self) -> VWPhysicalAction:
        if self.__is_wall_ahead():
            return self.__decide_if_wall_ahead_and_kind()
        elif self.__is_on_dirt():
            #if there is already a dirt at this location, move or turn
            return self.__decide_if_on_dirt_and_kind()
        else:
            #otherwise do a random action (including dropping dirt)
            return UserMindSurrogate.__act_randomly(weights=[0.2, 0.2, 0.45, 0.075, 0.075])

    def __decide_if_wall_ahead_and_kind(self) -> VWPhysicalAction:
        if self.__is_wall_on_the_left():
            return VWTurnAction(direction=Direction.right)
        elif self.__is_wall_on_the_right():
            return VWTurnAction(direction=Direction.left)
        else:
            return UserMindSurrogate.__turn_randomly()

    def __decide_if_on_dirt_and_kind(self) -> VWPhysicalAction:
        if self.__is_wall_on_the_left():
            return UserMindSurrogate.__move_randomly(weights=[0.6, 0.0, 0.4])
        elif self.__is_wall_on_the_right():
            return UserMindSurrogate.__move_randomly(weights=[0.6, 0.4, 0.0])
        else:
            return UserMindSurrogate.__move_randomly(weights=[0.5, 0.25, 0.25])

    @staticmethod
    def __turn_randomly() -> VWPhysicalAction:
        if random() < 0.5:
            return VWTurnAction(direction=Direction.left)
        else:
            return VWTurnAction(direction=Direction.right)

    @staticmethod
    def __drop_random_dirt() -> VWPhysicalAction:
        if random() < 0.5:
            return VWDropAction(dirt_colour=Colour.green)
        else:
            return VWDropAction(dirt_colour=Colour.orange)

    @staticmethod
    def __move_randomly(weights: List[float]=[1/3, 1/3, 1/3]) -> VWPhysicalAction:
        assert type(weights) == list and len(weights) == 3 and sum(weights) == 1.0

        return UserMindSurrogate.__act_randomly(weights=[0.0, 0.0, weights[0], weights[1], weights[2]])

    @staticmethod
    def __move_or_drop_randomly(weights: List[float]=[1/3, 1/3, 1/3]) -> VWPhysicalAction:
        assert type(weights) == list and len(weights) == 3 and sum(weights) == 1.0

        return UserMindSurrogate.__act_randomly(weights=[weights[0], weights[1], weights[2], 0.0, 0.0])

    @staticmethod
    def __act_randomly(weights: List[float]=[0.2, 0.2, 0.2, 0.2, 0.2]) -> VWPhysicalAction:
        assert type(weights) == list and len(weights) == 5 and sum(weights) == 1.0

        rng_thresholds: List[float] = list(accumulate(weights))

        random_number: float = random()

        if random_number < rng_thresholds[0]:
            return VWDropAction(dirt_colour=Colour.green)
        elif random_number < rng_thresholds[1]:
            return VWDropAction(dirt_colour=Colour.orange)
        elif random_number < rng_thresholds[2]:
            return VWMoveAction()
        elif random_number < rng_thresholds[3]:
            return VWTurnAction(direction=Direction.left)
        else:
            return VWTurnAction(direction=Direction.right)

    def __be_inconsiderate(self) -> VWPhysicalAction:
        # Wall ahead
        if self.__is_wall_ahead():
            return self.__decide_if_wall_ahead_and_inconsiderate()
        # Agent ahead
        elif self.__is_actor_ahead():
            return self.__decide_if_agent_ahead_and_inconsiderate()
        # Right and left occupied
        elif self.__is_actor_on_the_left() and self.__is_actor_on_the_right():
            return UserMindSurrogate.__move_or_drop_randomly(weights=[0.1, 0.1, 0.8])
        # Agent on the left and no wall on the right
        elif self.__is_actor_on_the_left() and not self.__is_wall_on_the_right():
            return UserMindSurrogate.__move_randomly(weights=[0.5, 0.0, 0.5])
        # Agent on the right and no wall on the left
        elif self.__is_actor_on_the_right() and not self.__is_wall_on_the_left():
            return UserMindSurrogate.__move_randomly(weights=[0.5, 0.5, 0.0])
        # Wall on the left
        elif self.__is_wall_on_the_left():
            return self.__decide_if_wall_on_the_left_and_inconsiderate()
        # Wall on the right
        elif self.__is_wall_on_the_right():
            return self.__decide_if_wall_on_the_right_and_inconsiderate()
        # Any other possibility
        else:
            return self.__act_randomly(weights=[0.15, 0.15, 0.6, 0.05, 0.05])

        # Always wall ahead
    def __decide_if_wall_ahead_and_inconsiderate(self) -> list:
        if self.__is_wall_on_the_left(): # wall on the left
            return VWTurnAction(direction=Direction.right)
        elif self.__is_wall_on_the_right(): # wall on the right
            return VWTurnAction(direction=Direction.left)
        elif self.__is_actor_on_the_left() and self.__is_actor_on_the_right(): # both left and right are full
            return UserMindSurrogate.__turn_randomly()
        elif self.__is_actor_on_the_left(): # agent on the left
            return VWTurnAction(direction=Direction.right)
        elif self.__is_actor_on_the_right(): # agent on the right
            return VWTurnAction(direction=Direction.left)
        elif self.__is_on_dirt(): # both left and right are free, drop dirt?
            return UserMindSurrogate.__turn_randomly()
        else: # wall ahead, left and right free, no dirt on center.
            return self.__act_randomly(weights=[0.075, 0.075, 0.6, 0.0, 0.25])
        
    # Always agent ahead
    def __decide_if_agent_ahead_and_inconsiderate(self) -> list:
        if self.__is_wall_on_the_left():
            return VWTurnAction(direction=Direction.right)
        elif not self.__is_wall_on_the_right():
            return VWTurnAction(direction=Direction.left)
        elif self.__is_actor_on_the_left() and self.__is_actor_on_the_right(): # both left and right are full
            return self.__drop_random_dirt() # dropping a dirt in front of the agent, if possible
        elif self.__is_actor_on_the_left(): # agent on the left
            return VWTurnAction(direction=Direction.right)
        elif self.__is_actor_on_the_right(): # agent on the right
            return VWTurnAction(direction=Direction.left)
        elif self.__is_on_dirt(): # both left and right are free, drop dirt?
            return UserMindSurrogate.__turn_randomly()
        else:
            return UserMindSurrogate.__act_randomly(weights=[0.25, 0.25, 0.0, 0.25, 0.25])

    # Always wall on the left
    def __decide_if_wall_on_the_left_and_inconsiderate(self) -> list:
        if self.__is_on_dirt():
            return UserMindSurrogate.__move_randomly(weights=[0.9, 0.0, 0.1])
        else:
            return UserMindSurrogate.__act_randomly(weights=[0.075, 0.075, 0.6, 0.0, 0.25])

    # Always wall on the right
    def __decide_if_wall_on_the_right_and_inconsiderate(self) -> list:
        if self.__is_on_dirt():
            return UserMindSurrogate.__move_randomly(weights=[0.9, 0.1, 0.0])
        else:
            return UserMindSurrogate.__act_randomly(weights=[0.075, 0.075, 0.6, 0.25, 0.0])
