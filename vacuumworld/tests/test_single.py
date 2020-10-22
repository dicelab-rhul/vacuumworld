#!/usr/bin/env python3
import vacuumworld
from vacuumworld.vwc import action, direction

class Mind:
    def __init__(self):
        super().__init__()

    def revise(self, observation, messages):
        self.observation = observation
        self.messages = messages

        print(self.observation)
        print(self.messages)

    def decide(self):
        pass 


vacuumworld.run(Mind())