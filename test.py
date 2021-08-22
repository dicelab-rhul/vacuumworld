#!/usr/bin/env python3

from vacuumworld import run
from vacuumworld.model.actor.actor_mind_surrogate import ActorMindSurrogate
from vacuumworld.model.actions.move_action import VWMoveAction
from vacuumworld.model.actions.turn_action import VWTurnAction
from vacuumworld.model.actions.broadcast_action import VWBroadcastAction
from vacuumworld.common.direction import Direction

from random import randint

class WhiteMind(ActorMindSurrogate):    
    def decide(self):
        return [VWMoveAction(), VWTurnAction(direction=Direction.left), VWTurnAction(direction=Direction.right)][randint(0, 2)]
       
    def revise(self, observation, messages):
        self.observation = observation
        self.messages = messages

class GreenMind(ActorMindSurrogate):
    def decide(self):
        return VWBroadcastAction(message="I am a green agent.")
       
    def revise(self, observation, messages):
        self.observation = observation
        self.messages = messages

class OrangeMind(ActorMindSurrogate):
    def decide(self):
        return VWTurnAction(direction=Direction.left)

    def revise(self, observation, messages):
        self.observation = observation
        self.messages = messages

if __name__ == "__main__":
    run(green_mind=GreenMind(), orange_mind=OrangeMind(), white_mind=WhiteMind())