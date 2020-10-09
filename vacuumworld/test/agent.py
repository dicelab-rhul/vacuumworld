import vacuumworld
from vacuumworld.vwc import action, Direction

class MyMind:

    def decide(self):
        #return action.clean, action.speak("")
        #return action.speak("")
        #return action.clean()
        #return 1,2,3
        #return []
        #return ['garbage']
        #return ('speak',)
        return None, action.speak("")

        if self.observation.center.dirt is not None:
            return action.clean()

        elif self.observation.forward is not None and self.observation.forward.dirt is not None:
            return action.move()
        return action.turn(Direction.left)

    def revise(self, observation, messages):
        self.observation = observation
        #print(self.observation.forward)
        #raise ValueError("{0} BAR".format("FOO"))

vacuumworld.run(MyMind(), load="abc.vw", play=True)