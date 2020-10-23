from enum import Enum



class Orientation(Enum):
    '''
        Representation of an agents orientation. An agent can be orientated in 
        one of the cardinal directions (north, east, south, west). This class is useful
        for checking in which of theese directions the agent is facing.
        
        Example
        --------
        ::
            
            from vwc import action, direction, orientation
            
            def revise(self, observation, messages):
                self.orientation = observation.center.agent.orientation
            
            def decide(self):
                if self.orientation == orientation.north:
                    return action.turn(direction.right)
                
        
        If the agent is facing northward it will turn to the right.
        
        Attributes:
            * ``north``
            * ``east``
            * ``south``
            * ``west``
    '''
    north = "north"
    east = "east"
    south = "south"
    west = "west"

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return str(self)

orientation = Orientation
