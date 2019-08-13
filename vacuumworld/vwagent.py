from pystar.Agent import Mind, Body

from . import vwsensor
from . import vwactuator
from . import vwagent 
from . import vwaction
from . import vwc

from collections import namedtuple
agent_type = namedtuple('agent_type', 'cleaning user')('cleaning', 'user')

class VWBody(Body):
    
    def __init__(self, _type, ID, mind, orientation, coordinate, colour):
        mind = vwagent.VWMind(mind)
        assert _type in agent_type
        if _type == agent_type.cleaning:
            actuators = {"physical":vwactuator.CleaningAgentActuator(),
                         "communication":vwactuator.CommunicationActuator()}
        else:
            actuators = {"physical":vwactuator.UserActuator(),
                         "communication":vwactuator.CommunicationActuator()}

        sensors = {"vision":vwsensor.VisionSensor(),
                   "communication":vwsensor.CommunicationSensor()}
        self.ID = ID
        
        super(VWBody, self).__init__(mind, actuators, sensors)
        
        self.orientation = orientation
        self.colour = colour 
        self.coordinate = coordinate

class VWMind(Mind):
    
    def __init__(self, surrogate):
        super(VWMind, self).__init__()
        self.surrogate = surrogate
       
    def cycle(self):
 
        observation = [percept for percept in self.body._sensors["vision"]]
        assert(len(observation) == 1)
        
        messages = [percept for percept in self.body._sensors["communication"]]
        self.surrogate.revise(*observation, messages)
        
        physical_action = self.surrogate.do()
        communicative_action = self.surrogate.speak()
        
        if communicative_action is not None:
            validate_action(communicative_action)
            _assert(communicative_action[0] == vwc.action_names.speak, 'please use vwc.action.speak for communication')
            _assert(len(communicative_action) >= 2, 'please use vwc.action.speak for communication')
            action = vwaction._action_factories[communicative_action[0]](*communicative_action[1:])
            actuator, = self.body.find_actuators(action)
            actuator.attempt(action)
            
        if physical_action is not None:
            validate_action(physical_action)
            _assert(physical_action[0] != vwc.action_names.speak, 'please use speak() for communication and not do()')
            action = vwaction._action_factories[physical_action[0]](*physical_action[1:])
            actuator = self.body.find_actuators(action)
            _assert(len(actuator) == 1, 'invalid action ' + physical_action[0] + ' for agent') #the actuator doesnt exists for the agent?
            actuator[0].attempt(action)
              
def validate_action(action):
    _assert(isinstance(action, tuple), str(action) + 'please make use of vwc.action')
    _assert(action[0] in vwc.action_names,  str(action) + 'must be one of ' + str(list(vwc.action_names)) + ' from vwc.action')

class ActionError(Exception):
    
    def __init__(self, message):
        super(ActionError, self).__init__("Invalid action: " + message)

def _assert(condition, exception):
    if not condition:
        raise ActionError(exception)
