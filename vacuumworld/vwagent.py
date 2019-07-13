from pystarworlds.Agent import Mind

'''
from GridPerception import Observation,Message,ActionResultPerception
from GridWorldAction import  MoveRightAction,MoveLeftAction,ForwardMoveMentAction,SpeakAction,NoMoveMentAction,BroadcastAction,CleanDirtAction,DropDirtAction

from pystarworlds.Factories import ActionFactory 
from VWFactories import Speak,SpeakToAll,Move,TurnLeft,TurnRight,CleanDirt
'''

from pystarworlds.Agent import AgentBody

class CleaningAgentBody(AgentBody):
    
    def __init__(self, mind, actuators, sensors, orientation, coordinate, colour):
        super(CleaningAgentBody, self).__init__(mind, actuators, sensors)
        self.orientation = orientation
        self.colour = colour 
        self.coordinate = coordinate

class CleaningAgentMind(Mind):
       
    def cycle(self):
        print("cycle!")
        for sensor in self.body.sensors:
            for percept in sensor:
                print(sensor, "->", percept)
        
    



