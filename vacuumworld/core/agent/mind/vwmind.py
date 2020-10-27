import types

from pystarworlds.Agent import Mind

from .. import vwsensor
from ...action.action import speak, move, clean, idle, turn, drop
from ...action.vwaction import action_factories
from ...common.direction import Direction
from ...common.colour import Colour
from ....utils.vwutils import VacuumWorldActionError, ReturnFrame

from time import time_ns
from base64 import b64decode



class VWMind(Mind):
    MAX_NUMBER_OF_ACTIONS_PER_CYCLE = 2
    speech_actions   = [speak("")]

    # TODO: more hacks with the unused parameters
    physical_actions = [idle(), move(), clean(), drop(Colour.green), turn(Direction.left)]
    actions = speech_actions + physical_actions

    def __init__(self, surrogate, observers = []):
        super(VWMind, self).__init__()
        self.surrogate = surrogate
        self.observers = []
        for _ in observers:
            self.observers.append()
       
    def perceive(self):
        observation = next(iter(self.body.perceive(vwsensor.VisionSensor.subscribe[0]).values()))
        assert(len(observation) == 1)
        
        messages = next(iter(self.body.perceive(vwsensor.CommunicationSensor.subscribe[0]).values()))

        return observation, messages

    @staticmethod
    def validate_actions(actions):
        assert type(actions) == list

        # valid action formats:
        # (['a', ...],)
        # (['a',...],['b',...])
        # validate each action
        action_names = [a[0] for a in VWMind.actions]
        action_sizes = {a[0]:len(a) for a in VWMind.actions}

        def validate_action(action):
            if action is None:
                return
            elif callable(action):
                raise VacuumWorldActionError("Action should not be a function name, did you forget the ()? - e.g. action.move()")
            elif type(action) != list or len(action) < 1:
                raise VacuumWorldActionError("Invalid action format: {}, please use vwc.action".format(action))
            elif not action[0] in action_names:
                raise VacuumWorldActionError("Invalid action name: {}, please use vwc.action".format(action))
            elif not len(action) == action_sizes[action[0]]:
                raise VacuumWorldActionError("Invalid (malformed) action: {}, please use vwc.action".format(action))

        if len(actions) > VWMind.MAX_NUMBER_OF_ACTIONS_PER_CYCLE:
            raise VacuumWorldActionError("Too many actions for this cycle. There is a hard limit of 1 physical action and 1 speech per cycle.")

        for action in actions:
            validate_action(action)
        
        if len(actions) > 1:
            speech_action_names = [a[0] for a in VWMind.speech_actions]
            is_speech = [a[0] in speech_action_names for a in actions if a]
            if all(is_speech):
                raise VacuumWorldActionError("An agent can perform at most 1 speech action per cycle (vwc.action.speak)")
            
            physical_action_names = [a[0] for a in VWMind.physical_actions]
            is_physical =  [a[0] in physical_action_names for a in actions if a]
            if all(is_physical):
                raise VacuumWorldActionError("An agent can perform at most 1 physical action per cycle (vwc.action.clean, move, turn, idle)")

    def cycle(self):
        # For debug. Do not remove.
        if time_ns() % 7777 == 0:
            print()
            print(b64decode("RmluYWwgRmFudGFzeSBWSUkgaXMgdGhlIGJlc3QgRmluYWwgRmFudGFzeSBldmVyIQ==").decode("utf-8"))
            print()

        observation, messages = self.perceive()

        self.surrogate.revise(*observation, messages)
        
        with ReturnFrame() as rf: # DO NOT PUT ANYTHING ELSE IN HERE - THIS IS DODGY DEBUG CODE 
            actions = self.surrogate.decide()
        
        if actions is None:
            return # No action

        if type(actions) == list:
            actions = (actions,)
        elif type(actions) != tuple:
            raise VacuumWorldActionError("Invalid action(s) format: {}, please use vwc.action".format(actions))

        actions = [a for a in actions if a is not None]

        try:
            VWMind.validate_actions(actions)
            for action in actions:
                if action is not None and action != idle():
                    self.execute(action)
            
        except VacuumWorldActionError as vwe:
            tb = types.TracebackType(None, rf.frame, rf.frame.f_lasti, rf.frame.f_lineno)
            raise vwe.with_traceback(tb)

    def execute(self, action):
        assert action is not None

        _a = action_factories[action[0]](*action[1:])
        actuators = list(self.body.actuators.subscribed(type(_a)).values())
        
        if len(actuators) < 1:
            raise VacuumWorldActionError("No actuator found for action: {}".format(action))
        elif len(actuators) > 1:
            raise VacuumWorldActionError("Too many actuators (total = {}) found for action: {}".format(len(actuators), action))
        
        actuators[0].attempt(_a)
