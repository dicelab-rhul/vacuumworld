from pystarworlds.Action import Action

from . import vwc

class VWPhysicalAction(Action):
     def __init__(self, actor):
         super(VWPhysicalAction, self).__init__(actor)
    
class MoveAction(VWPhysicalAction):
    pass
             
class CleanAction(VWPhysicalAction):
    pass

class DropAction(VWPhysicalAction):
    
    def __init__(self, actor, colour):
        super(DropAction, self).__init__(actor)
        assert colour in vwc._colour_dirt
        self.colour = colour
        
class TurnAction(VWPhysicalAction):
    
    def __init__(self, actor, direction):
        super(TurnAction, self).__init__(actor)
        self.direction = direction

class CommunicativeAction(Action):
    
    def __init__(self, sender, content, *to):
        super(CommunicativeAction, self).__init__(sender)
        self.sender = sender
        self.content = content
        self.to = to
                  
class ActionFactory:
    
    def __init__(self):
        pass
    
class DropActionFactory(ActionFactory):
    
    def __init__(self):
        super(DropActionFactory, self).__init__()
        
    def __call__(self, _actor, _colour):
        return DropAction(_actor, _colour)
    
class TurnActionFactory(ActionFactory):
    
    def __init__(self):
        super(TurnActionFactory, self).__init__()
        
    def __call__(self, _actor, _direction):
        return TurnAction(_actor, _direction)
    
class SpeakActionFactory(ActionFactory):
    
    def __init__(self):
        super(SpeakActionFactory, self).__init__()
        
    def __call__(self, _actor, _message, *_to):
        assert(isinstance(_message, str))
        for t in _to:
            #print(_actor, _message, _to)
            assert(isinstance(t, str))
        return CommunicativeAction(_actor, _message, *_to)
    
_action_factories = {'move':lambda actor: MoveAction(actor), 
                     'turn':TurnActionFactory(), 
                     'clean':lambda actor: CleanAction(actor), 
                     'drop':lambda actor: DropAction(actor),
                     'speak':SpeakActionFactory()}