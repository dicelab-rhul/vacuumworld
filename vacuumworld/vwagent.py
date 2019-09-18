from pystarworlds.Agent import Mind, Body

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
    
    def __init__(self, surrogate, observers = []):
        super(VWMind, self).__init__()
        self.surrogate = surrogate
        self.observers = []
        for observer in observers:
            self.observers.append()
       
    def cycle(self):
 
        observation = [percept for percept in self.body._sensors["vision"]]
        assert(len(observation) == 1)
        
        messages = [percept for percept in self.body._sensors["communication"]]
        self.surrogate.revise(*observation, messages)
    
        actions = self.surrogate.decide()

        if actions is None:
            return
        
        speak_actions = []
        physical_actions = []

        if isinstance(actions, tuple):
            if type(actions) in vwc.action_types:
               actions = [actions]
            for action in actions:
                if action is None:
                    continue
                if type(action) in vwc.action_types:
                    if type(action) == vwc.idle:
                        continue
                    if type(action) == vwc.speak:
                        _a = vwaction._action_factories[type(action).__name__](action.message, *action.to)
                        speak_actions.append((_a, type(action).__name__))
                    else:
                        _a = vwaction._action_factories[type(action).__name__](*action[:])
                        physical_actions.append((_a, type(action).__name__))
                elif callable(action):
                    raise ActionError(str(action) + " should not be callable, did you forget ()?")
                else:
                    raise ActionError(str(action) + " is an invalid action.")
                    
            _assert(len(speak_actions) <= 1, ' an agent can perform at most one speech action per cycle, attempted:' + str([s[1] for s in speak_actions]))
            _assert(len(physical_actions) <= 1, 'an agent can perform at most one physical action per cycle, attempted:' +  str([s[1] for s in physical_actions]))
            
            for action in speak_actions + physical_actions:
                actuators = self.body.find_actuators(action[0])
                _assert(len(actuators) == 1,  str(action[1]) + ' for agent - actuator does not exist')
                actuators[0].attempt(action[0])
        else:
            raise ActionError(str(actions) + " is an invalid action.")
            
            
        
        
        
def validate_action(action):
    pass
    #_assert(not callable(action), 'invalid action, did you forget to call the action? - e.g. move()')
    #_assert(isinstance(action, tuple), str(action) + 'please make use of vwc.action')
   #_assert(action[0] in vwc.action_names,  str(action) + 'must be one of ' + str(list(vwc.action_names)) + ' from vwc.action')

class ActionError(Exception):
    
    def __init__(self, message):
        super(ActionError, self).__init__("Invalid action: " + message)

def _assert(condition, exception):
    if not condition:
        raise ActionError(exception)
