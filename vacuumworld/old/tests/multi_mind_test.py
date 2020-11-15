#!/usr/bin/env python3


from typing import Iterable, Union
from vacuumworld.core.common.observation import Observation
import vacuumworld

from vacuumworld.core.action import action
from vacuumworld.core.common.direction import Direction


class DefaultMind():
    def __init__(self) -> None:
        super().__init__()
        self.grid_size: int = -1
        self.stop: bool = False

    def revise(self, observation: Observation, messages: Iterable) -> None:
        self.observation: Observation = observation
        self.messages: Iterable = messages

        print(self.observation)
        print(self.messages)

    def decide(self) -> Union[list, tuple]:
        if not self.stop:
            return action.speak("Hello, I cannot predict my colour."), action.turn(Direction.left)


class WhiteMind(DefaultMind):
    def decide(self) -> Union[list, tuple]:
        if not self.stop:
            return action.speak("Hello, I am a white agent"), action.turn(Direction.right)


class GreenMind(DefaultMind):
    def decide(self) -> Union[list, tuple]:
        if not self.stop:
            return action.speak("Hello, I am a green agent"), action.turn(Direction.right)


class OrangeMind(DefaultMind):
    def decide(self) -> Union[list, tuple]:
        if not self.stop:
            return action.speak("Hello, I am an orange agent"), action.turn(Direction.right)

state_file_name: str = "full.vw"

# Non-named parameter --> default_mind=DefaultMind().
vacuumworld.run(DefaultMind(), load=state_file_name, play=True)

# default_mind=DefaultMind(). Nothing ovverrides it for any agent.
vacuumworld.run(default_mind=DefaultMind(), load=state_file_name, play=True)

# default_mind=DefaultMind(). GreenMind() overrides it for green agents.
vacuumworld.run(default_mind=DefaultMind(), green_mind=GreenMind(), load=state_file_name, play=True)

# default_mind=DefaultMind(). WhiteMind() overrides it for white agents.
vacuumworld.run(default_mind=DefaultMind(), white_mind=WhiteMind(), load=state_file_name, play=True)

# default_mind=DefaultMind(). OrangeMind() overrides it for orange agents.
vacuumworld.run(default_mind=DefaultMind(), orange_mind=OrangeMind(), load=state_file_name, play=True)

# default_mind=DefaultMind(). GreenMind() overrides it for green agents. OrangeMind() overrides it for orange agents.
vacuumworld.run(default_mind=DefaultMind(), green_mind=GreenMind(), orange_mind=OrangeMind(), load=state_file_name, play=True)

# default_mind=DefaultMind(). WhiteMind() overrides it for white agents. OrangeMind() overrides it for orange agents.
vacuumworld.run(default_mind=DefaultMind(), white_mind=WhiteMind(), orange_mind=OrangeMind(), load=state_file_name, play=True)

# default_mind=DefaultMind(). WhiteMind() overrides it for white agents. GreenMind() overrides it for green agents.
vacuumworld.run(default_mind=DefaultMind(), white_mind=WhiteMind(), green_mind=GreenMind(), load=state_file_name, play=True)

# default_mind=DefaultMind(). WhiteMind() overrides it for white agents. GreenMind() overrides it for green agents. OrangeMind() overrides it for orange agents.
vacuumworld.run(default_mind=DefaultMind(), white_mind=WhiteMind(), green_mind=GreenMind(), orange_mind=OrangeMind(), load=state_file_name, play=True)

# no default_mind. WhiteMind() assigned to white agents. GreenMind() assigned to green agents. OrangeMind() assigned to orange agents.
vacuumworld.run(white_mind=WhiteMind(), green_mind=GreenMind(), orange_mind=OrangeMind(), load=state_file_name, play=True)
