#!/usr/bin/env python3
import vacuumworld



class Mind:
    def __init__(_):
        super().__init__()

    def revise(self, observation, messages):
        self.observation = observation
        self.messages = messages

        print(self.observation)
        print(self.messages)

    def decide(_):
        # Dummy
        pass 


if __name__ == "__main__":
    vacuumworld.run(Mind())
