from pystarworlds.Action import Action

class VWPhysicalAction(Action):
     def __init__(self, actor):
         super(VWPhysicalAction, self).__init__(actor)
    
class MoveAction(VWPhysicalAction):
    pass
             
class CleanAction(VWPhysicalAction):
    pass

class DropAction(VWPhysicalAction):
    pass

class TurnAction(VWPhysicalAction):
    
    def __init__(self, actor, direction):
        super(TurnAction, self).__init__(actor)
        self.direction = direction

class CommunicativeAction(Action):
    
    def __init__(self, sender, message, *to):
        super(CommunicativeAction, self).__init__(sender)
        self.sender = sender
        self.message = message
        self.to = to
                  
