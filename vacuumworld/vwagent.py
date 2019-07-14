from pystarworlds.Agent import Mind

'''
from GridPerception import Observation,Message,ActionResultPerception
from GridWorldAction import  MoveRightAction,MoveLeftAction,ForwardMoveMentAction,SpeakAction,NoMoveMentAction,BroadcastAction,CleanDirtAction,DropDirtAction

from pystarworlds.Factories import ActionFactory 
from VWFactories import Speak,SpeakToAll,Move,TurnLeft,TurnRight,CleanDirt
'''

from pystarworlds.Agent import AgentBody

from . import vwsensor
from . import vwactuator
from . import vwagent 
from . import vwaction


class CleaningAgentBody(AgentBody):
    
    def __init__(self, mind, orientation, coordinate, colour):
        mind = vwagent.CleaningAgentMind(mind)
        actuators = {"physical":vwactuator.CleaningAgentActuator(),
                     "communication":vwactuator.CommunicationActuator()}
        sensors = {"vision":vwsensor.VisionSensor(),
                   "communication":vwsensor.CommunicationSensor()}
        super(CleaningAgentBody, self).__init__(mind, actuators, sensors)
        self.orientation = orientation
        self.colour = colour 
        self.coordinate = coordinate

class CleaningAgentMind(Mind):
    
    def __init__(self, surrogate):
        self.surrogate = surrogate
       
    def cycle(self):
        print("cycle!")
        
        observation = [percept for percept in self.body._sensors["vision"]]
        print(observation)
        assert(len(observation) == 1)
        
        
        messages = [percept for percept in self.body._sensors["communication"]]
        self.surrogate.revise(observation, messages)
        
        physical_action = self.surrogate.do()
        communicative_action = self.surrogate.speak()
        
        assert(isinstance(communicative_action, vwaction.CommunicativeAction))
        assert(isinstance(physical_action, vwaction.VWPhysicalAction))
        
        self.body._actuators["communication"].attempt(communicative_action)
        self.body._actuators["physical"].attempt(physical_action)
        
        '''
        for sensor in self.body.sensors:
            for percept in sensor:
                print(sensor, "->", percept)
        '''


    


