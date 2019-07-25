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
 
        observation = [percept for percept in self.body._sensors["vision"]]
        assert(len(observation) == 1)
        
        
        messages = [percept for percept in self.body._sensors["communication"]]
        self.surrogate.revise(*observation, messages)
        
        physical_action = self.surrogate.do()
        communicative_action = self.surrogate.speak()
        
        if communicative_action is not None:
            assert isinstance(communicative_action, tuple)
            action = vwaction._action_factories[communicative_action[0]](self.body.ID, *communicative_action[1:])
            self.body._actuators["communication"].attempt(action)
        if physical_action is not None and physical_action[0] != 'idle':
            assert isinstance(physical_action, tuple)
            action = vwaction._action_factories[physical_action[0]](self.body.ID, *physical_action[1:])
            self.body._actuators["physical"].attempt(action)
              
        


    


