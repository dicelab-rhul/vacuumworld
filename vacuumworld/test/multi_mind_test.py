#!/usr/bin/env python3


import vacuumworld

from sys import exit
from vacuumworld.vwc import action, direction


class DefaultMind():
    def __init__(self):
        super().__init__()
        self.grid_size = -1

    def revise(self, observation, messages):
        print(observation)
        print(messages)

    def decide(self):
        return action.speak("Hello, I cannot predict my colour."), action.turn(direction.left)


class WhiteMind():
    def __init__(self):
        super().__init__()
        self.grid_size = -1

    def revise(self, observation, messages):
        print(observation)
        print(messages)

    def decide(self):
        return action.speak("Hello, I am a white agent"), action.turn(direction.right)


class GreenMind():
    def __init__(self):
        super().__init__()
        self.grid_size = -1

    def revise(self, observation, messages):
        print(observation)
        print(messages)

    def decide(self):
        return action.speak("Hello, I am a green agent"), action.turn(direction.right)


class OrangeMind():
    def __init__(self):
        super().__init__()
        self.grid_size = -1

    def revise(self, observation, messages):
        print(observation)
        print(messages)

    def decide(self):
        return action.speak("Hello, I am an orange agent"), action.turn(direction.right)

state_file_name = "treble.vw"

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