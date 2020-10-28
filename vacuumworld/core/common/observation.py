from typing import Iterable, NamedTuple, Type

from ..environment.location_interface import Location



class Observation(NamedTuple):
    '''
        A datastructure representing an observation (perception) of the agent. 
        An observation consists of six locations, the center location always 
        contains the observing agent. Each of the other 5 locations are relative 
        to the center location.
        
        Example 1
        -----------
        ::
            
            def revise(self, observation, messages):
                self.observation = observation
                self.colour = observation.center.agent.colour
                self.position = observation.center.agent.coordinate
        
        An agent should update its beliefs with new information that it has 
        perceived for later use in decision making.
        
        Example 2
        ----------
        ::
            
            def decide(self):
                if self.observation.forward.agent:
                    return action.turn(direction.left)
                elif self.observation.forward:
                    return action.move()
                else:
                    return action.idle()
                    
        This agent will turn if there is an agent in-front of it, move until it 
        reachs the edge of the grid and then remains idle.
    '''
    center : Location
    left : Location
    right : Location
    forward : Location
    forwardleft : Location
    forwardright : Location

    def __iter__(self) -> Iterable:
        return (self[i] for i in range(len(self)) if self[i] is not None)

observation: Type = Observation
