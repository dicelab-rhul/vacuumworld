from .orientation import Orientation



class Direction():
    '''
        An indicator used in the turn action. May also be used to turn orientations.
        
        Attributes:
            * `left (callable)`: Turns an orientation left,  indicates a left turn in the turn action.  
            * `right (callable)`: Turns an orientation right,  indicates a right turn in the turn action.  
        
        Example 1
        ---------
        ::
            
            def decide(self):
                return action.turn(direction.left)
                
        Example 2
        ---------
        ::
            
            def revise(self, observation, messages):
                self.orientation = observation.center.agent.orientation
                self.left_orientation = direction.left(self.orientation)
                self.right_orientation = direction.right(self.orientation)
    '''

    @staticmethod
    def left(_orientation):
        '''
            Turns an orientation left. Indicates a left turn in the turn action.                        
        '''
        od = (Orientation.north, Orientation.east, Orientation.south, Orientation.west)
        return od[(od.index(_orientation) - 1) % 4]

    @staticmethod
    def right(_orientation):
        '''
            Turns an orientation left. Indicates a left turn in the turn action.                        
        '''
        od = (Orientation.north, Orientation.east, Orientation.south, Orientation.west)
        return od[(od.index(_orientation) + 1) % 4]

direction = Direction
