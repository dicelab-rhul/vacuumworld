import unittest
import inspect

from vacuumworld.vwagent import VWMind, VWBody, agent_type
from vacuumworld.vwc import action, direction, colour

#actions = [for m in inspect.getmembers(action) if inspect.isfunction(m)]

class TestAgent:

    def __init__(self, action):
        self.action = action
    
    def revise(self, observation, messages):
        pass

    def decide(self):
        return action

def test_action(a):
    pass 

class TestValidation(unittest.TestCase):

    def test_valid(self):
        # NO EXCEPTIONS! 
        #TODO: cycle... not sure how to fake this
        VWBody(agent_type.cleaning, "A-1", TestAgent(action.clean()),None,None,None)
        VWBody(agent_type.cleaning, "A-1", TestAgent(action.move()),None,None,None)
        VWBody(agent_type.cleaning, "A-1", TestAgent(action.idle()),None,None,None)
        VWBody(agent_type.cleaning, "A-1", TestAgent(action.turn(direction.left)),None,None,None)
        VWBody(agent_type.cleaning, "A-1", TestAgent(action.drop(colour.green)),None,None,None)
        VWBody(agent_type.cleaning, "A-1", TestAgent(action.speak("")),None,None,None)
        VWBody(agent_type.cleaning, "A-1", TestAgent(action.speak("", "A-1", "A-2")),None,None,None)

    def test_invalid(self):
        # EXCEPTIONS!
        pass 
        







if __name__ == "__main__":
    unittest.main()