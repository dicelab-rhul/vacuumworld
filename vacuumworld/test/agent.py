import vacuumworld
from vacuumworld.vwc import action, Direction

class MyMind:

    def decide(self):
        if self.observation.center.dirt is not None:
            return action.clean()

        elif self.observation.forward is not None and self.observation.forward.dirt is not None:
            return action.move()
        return action.turn(Direction.left)

        
    def revise(self, observation, messages):
        self.observation = observation
        #print(self.observation.forward)



vacuumworld.run(MyMind(), load="abc.vw")