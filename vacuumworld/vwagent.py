from pystarworlds.Agent import Mind, Body

from . import vwsensor
from . import vwactuator
from . import vwagent 
from . import vwaction
from . import vwc
from . import vwutils

import traceback

from collections import namedtuple
agent_type = namedtuple('agent_type', 'cleaning user')('cleaning', 'user')

class VWBody(Body):
    
    def __init__(self, _type, ID, mind, orientation, coordinate, colour):
        mind = vwagent.VWMind(mind)
        assert _type in agent_type
        if _type == agent_type.cleaning:
            actuators = [vwactuator.CleaningAgentActuator(), vwactuator.CommunicationActuator()]
        else:
            actuators = [vwactuator.UserActuator(), vwactuator.CommunicationActuator()]

        sensors = [vwsensor.VisionSensor(), vwsensor.CommunicationSensor()]
        self._Identifiable__ID = ID #hack...
        
        super(VWBody, self).__init__(mind, actuators, sensors)
        
        self.orientation = orientation
        self.colour = colour 
        self.coordinate = coordinate

class VWMind(Mind):
    
    action_names = [vwc.action.move.__name__, vwc.action.clean.__name__, vwc.action.idle.__name__,
                    vwc.action.drop.__name__, vwc.action.turn.__name__, vwc.action.speak.__name__]
    speech_action_names = [vwc.action.speak.__name__]
    physical_action_names =  [vwc.action.move.__name__, vwc.action.clean.__name__,
                              vwc.action.drop.__name__, vwc.action.turn.__name__]
    action_size = {vwc.action.move.__name__:1, vwc.action.clean.__name__:1, vwc.action.idle.__name__:1,
                   vwc.action.drop.__name__:2, vwc.action.turn.__name__:2, vwc.action.speak.__name__:3}
    
    def __init__(self, surrogate, observers = []):
        super(VWMind, self).__init__()
        self.surrogate = surrogate
        self.observers = []
        for observer in observers:
            self.observers.append()
       
    def cycle(self):
        observation = next(iter(self.body.perceive(vwsensor.VisionSensor.subscribe[0]).values()))
        assert(len(observation) == 1)
        
        messages = next(iter(self.body.perceive(vwsensor.CommunicationSensor.subscribe[0]).values()))
        self.surrogate.revise(*observation, messages)
    
        actions = self.surrogate.decide()
        #https://pymotw.com/2/sys/tracing.html
        #to get helpful exception information it will be better to trace decide!

        if actions is None:
            return

        if type(actions) == tuple:
            actions = tuple([action for action in actions if action is not None])
            if len(actions) == 0:
                return
            
            if type(actions[0]) == str: #validate a single action
                self.attempt_action(self.validate_action(actions))
                return 
            elif type(actions[0]) == tuple: #validate multiple actions
                if len(actions) == 2:
                    if type(actions[1]) == tuple:
                        actions = [self.validate_action(action) for action in actions]
                        names = [action[0] for action in actions]
                        is_speech = [name in VWMind.speech_action_names for name in names]
                        is_physical = [name in VWMind.physical_action_names for name in names]
                        if all(is_speech):
                            raise vwutils.VacuumWorldActionError("An agent can perform at most 1 speech action per cycle (vwc.action.speak)")
                        if all(is_physical):
                            raise vwutils.VacuumWorldActionError("An agent can perform at most 1 physical action per cycle (vwc.action.clean, move, turn, idle, drop)")
                        for action in actions:
                            self.attempt_action(action)
                        return
                else:
                    vwutils.VacuumWorldActionError("Invalid action(s): " + str(actions) + ", an agent can perform at most 1 physical action and 1 speech action per cycle (a total of 2 actions)")
                    
        raise vwutils.VacuumWorldActionError("Invalid action(s): " + str(actions) + ", please use vwc.action")
    
    def attempt_action(self, action):
        _a = vwaction._action_factories[action[0]](*action[1:])
        if _a is None: #idle action
            return 
        actuators = list(self.body.actuators.subscribed(type(_a)).values())
        if len(actuators) != 1:
            raise vwutils.VacuumWorldActionError("No actuator found for action: " + str(action))
        actuators[0].attempt(_a)
        
    def validate_action(self, action):
        if type(action) == tuple:
            if len(action) > 0 and action[0] in VWMind.action_names:
                if len(action) == VWMind.action_size[action[0]]:
                    return action
        elif callable(action):
            raise vwutils.VacuumWorldActionError("Action should not be a function, did you forget the ()? - e.g. action.move()")
        raise vwutils.VacuumWorldActionError("Invalid action: " + str(action) + " please use vwc.action.")
        
