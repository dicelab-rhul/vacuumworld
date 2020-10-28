# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 12:00:27 2019

@author: ben
"""
from typing import Iterable, Type, List
from vacuumworld.core.common.observation import Observation
from ..action.action import random, move, drop, turn
from ..common.colour import Colour
from ..common.direction import Direction
from ...utils.vwutils import ignore


class User():
    def __init__(self) -> None:
        self.observation: Observation = None
        self.id: str = None

    def decide(_) -> list:
        raise NotImplementedError("Abstract class.")

    def revise(self, observation: Observation, messages: Iterable):
        self.id: str = observation.center.agent.name
        self.observation: Observation = observation

        # A user is not supposed to manage any message.
        ignore(messages)

    def is_wall_ahead(self) -> bool:
        return not self.observation.forward

    def is_wall_on_the_left(self) -> bool:
        return not self.observation.left

    def is_wall_on_the_right(self) -> bool:
        return not self.observation.right

    def is_on_dirt(self) -> bool:
        return self.observation.center.dirt

    def is_agent_ahead(self) -> bool:
        return self.observation.forward and self.observation.forward.agent

    def is_agent_on_the_left(self) -> bool:
        return self.observation.left and self.observation.left.agent

    def is_agent_of_the_right(self) -> bool:
        return self.observation.right and self.observation.right.agent


class EasyUser(User):
    def __init__(self) -> None:
        super().__init__()
        self.move_actions: List[list] = [move(), turn(Direction.left), turn(Direction.right)]
        self.actions: List[list] = [drop(Colour.green), drop(Colour.orange)]
        self.actions.extend(self.move_actions)
        
    def _decide_if_wall_ahead(self) -> list:
        if self.is_wall_on_the_left():
            return turn(Direction.right)
        elif self.is_wall_on_the_right():
            return turn(Direction.left)
        else:
            return random(self.move_actions[1:])

    def _decide_if_on_dirt(self) -> list:
        if self.is_wall_on_the_left():
            return random(self.move_actions, [0.6, 0.0, 0.4])
        elif self.is_wall_on_the_right():
            return random(self.move_actions, [0.6, 0.4, 0.0])
        else:
            return random(self.move_actions, [0.5, 0.25, 0.25])

    def decide(self) -> list: 
        if self.is_wall_ahead():
            return self._decide_if_wall_ahead()
        elif self.is_on_dirt():
            #if there is already a dirt at this location, move or turn
            return self._decide_if_on_dirt()
        else:
            #otherwise do a random action (including dropping dirt)
            return random(self.actions, [0.2, 0.2, 0.45, 0.075, 0.075])

        
class MediumUser(User):
    # Always wall ahead
    def _decide_if_wall_ahead(self) -> list:
        if self.is_wall_on_the_left(): # wall on the left
            return turn(Direction.right)
        elif self.is_wall_on_the_right(): # wall on the right
            return turn(Direction.left)
        elif self.is_agent_on_the_left() and self.is_agent_of_the_right(): # both left and right are full
            return random([turn(Direction.left), turn(Direction.right)])
        elif self.is_agent_on_the_left(): # agent on the left
            return turn(Direction.right)
        elif self.is_agent_of_the_right(): # agent on the right
            return turn(Direction.left)
        elif self.is_on_dirt(): # both left and right are free, drop dirt?
            return random([turn(Direction.left), turn(Direction.right)])
        else: # wall ahead, left and right free, no dirt on center.
            return random([turn(Direction.left), turn(Direction.right), drop(Colour.green), drop(Colour.orange)])
        
    # Always agent ahead
    def _decide_if_agent_ahead(self) -> list:
        if self.is_wall_on_the_left():
            return turn(Direction.right)
        elif not self.is_wall_on_the_right():
            return turn(Direction.left)
        elif self.is_agent_on_the_left() and self.is_agent_of_the_right(): # both left and right are full
            return random([drop(Colour.green), drop(Colour.orange)]) #TODO: is this logic correct? Compare with the method above.
        elif self.is_agent_on_the_left(): # agent on the left
            return turn(Direction.right)
        elif self.is_agent_of_the_right(): # agent on the right
            return turn(Direction.left)
        elif self.is_on_dirt(): # both left and right are free, drop dirt?
            return random([turn(Direction.left), turn(Direction.right)])
        else:
            return random([turn(Direction.left), turn(Direction.right), drop(Colour.green), drop(Colour.orange)])

    # Always wall on the left
    def _decide_if_wall_on_the_left(self) -> list:
        if self.is_on_dirt():
            return random([move(), turn(Direction.right)], [0.9, 0.1])
        else:
            return random([move(), turn(Direction.right), drop(Colour.green), drop(Colour.orange)], [0.6, 0.25, 0.075, 0.075])

    # Always wall on the right
    def _decide_if_wall_on_the_right(self) -> list:
        if self.is_on_dirt():
            return random([move(), turn(Direction.left)], [0.9, 0.1])
        else:
            return random([move(), turn(Direction.left), drop(Colour.green), drop(Colour.orange)], [0.6, 0.25, 0.075, 0.075])

    def decide(self) -> list: 
        # Wall ahead
        if self.is_wall_ahead():
            return self._decide_if_wall_ahead()
        # Agent ahead
        elif self.is_agent_ahead():
            return self._decide_if_agent_ahead()
        # Right and left occupied
        elif self.is_agent_on_the_left() and self.is_agent_of_the_right():
            return MediumUser.move_or_drop()
        # Agent on the left and no wall on the right
        elif self.is_agent_on_the_left() and not self.is_wall_on_the_right():
            return random([turn(Direction.right), move()])
        # Agent on the right and no wall on the left
        elif self.is_agent_of_the_right() and not self.is_wall_on_the_left():
            return random([turn(Direction.left), move()])
        # Wall on the left
        elif self.is_wall_on_the_left():
            return self._decide_if_wall_on_the_left()
        # Wall on the right
        elif self.is_wall_on_the_right():
            return self._decide_if_wall_on_the_right()
        # Any other possibility
        else:
            return MediumUser.random_all()         
    
    @staticmethod
    def move_or_drop() -> list:
        return random([move(), drop(Colour.green), drop(Colour.orange)], [0.8, 0.1, 0.1])   
     
    @staticmethod
    def random_all() -> list:
        return random([move(), drop(Colour.green), drop(Colour.orange), turn(Direction.left), turn(Direction.right)], [0.6, 0.15, 0.15, 0.05, 0.05]) 


#the users that can be used in vacuumworld
USERS: List[Type] = [EasyUser, MediumUser]
DIFFICULTY_LEVELS: int = len(USERS)
