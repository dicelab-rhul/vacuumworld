from typing import Iterable, List, Union
from random import choice, choices

from ..common.direction import Direction
from ..common.colour import Colour



'''
Actions may be attempted by agents at each cycle. An agent can attempt actions by returning them in the ``decide`` method.
An agent can attempt at most one physical action and one speech action per cycle.

Physical Actions
---------

* move - ``move()`` moves the agent one location in the direction of its current ``orientation`` - ``north``, ``east``, ``south`` or ``west``.
* turn - ``turn(direction)`` turns the agent in the given ``direction`` - ``left`` or ``right``.
* clean - ``clean()`` cleans any compatible dirt that is at the agents current ``location``.
* idle - ``idle()`` the agent is idle (no action is attempted).
* drop - ``drop(colour)`` the agent will drop dirt of the given ``colour`` at its current ``location``.

Speech Actions
---------

* speak - ``speak(message, *to)`` sends the given ``message`` to recipient agents specified by their ``name`` in ``*to``. If no recipients are specified the message with be broadcast to all agents.

Example 1
---------
::
    
    def decide(self):
        if self.observation.forward:
            return action.move()
        else:
            return action.idle()

In this example the agent will attempt to move forward until it reaches the edge of the grid (where ``self.observation.foward`` will be ``None``) and will then remain idle.

Example 2
---------
::
    
    def decide(self):
        return action.turn(direction.left), action.speak('hello!')

In this example the agent will spin around anti-clockwise - turning once per cycle, while broadcasting ``'hello'`` to all other agents.
'''


def move() -> List[str]:
    '''
        Moves an agent one tile in the direction it is facing.

        Returns: 
            ``['move',]``
    '''
    return ["move",]


def turn(direction: Union[Direction, str]) -> List[Union[str, Direction]]:
    '''
        Turns an agent in the given direction ``left`` or``right``. 
        
        Returns: 
            ``['turn', direction]``
    '''

    assert callable(direction)

    return ["turn", direction]


def clean() -> List[str]:
    '''
        Cleans any compatible dirt at an agents current location. 
        
        Compatibility:
            * Green Agent -> Green Dirt
            * Orange Agent -> Orange Dirt
            * White Agent -> Green & Orange Dirt
            * User -> None
        
        Returns:
            ``['clean',]``
    '''
    return ["clean",]


def idle() -> List[str]:
    '''
        The agent is idle (no action is attempted). This is the equivalent of returning ``None``.
        
        Returns:
            ``['idle',]``
    '''
    return ["idle",]


def speak(message: Union[str, list, tuple, float, bool], *to) -> List[Union[str, list, tuple, int, float, bool, Iterable]]:
    '''
        Sends the given ``message`` to recipient agents specified by their ``name`` in ``*to``. If no recipients are specified the message with be broadcast to all agents.
        
        Arguments:
            ``message (str, list, tuple, int, float, bool)``: the message to send.
        
            ``*to (str, variable, optional)``: The recipients of the messages. If empty, the message will be broadcast to all agents.
        
        Returns:
            ``['speak', message, to]``
    '''

    assert type(message) in [str, list, tuple, float, bool]
    assert isinstance(to, Iterable)

    return ["speak", message, to]


def drop(colour: Colour) -> List[Union[str, Colour]]:
    '''
        The agent will drop dirt of the given colour at its current location. Only a user agent can perform this action.
        
        Arguments:
            ``colour (vwc.colour)``: The colour of the dirt (``green`` or ``orange``). 
            
        Returns:
            ``['drop', colour]``
    '''

    assert colour in [Colour.green, Colour.orange]

    return ["drop", colour]


def random(actions: List[list], p=None) -> list: # An action is represented as a list
    '''
        Selects a random action from ``actions`` with given probabilities ``p``. 
        If ``p`` is ``None`` then the action will be selected uniformly.
        Otherwise, both arguments should have the same length.
        
        Arguments:
            * ``actions (list)``: a list of actions to choose from.
            * ``p (list)``:  a list of probabilities, one per action in ``actions`` that sum to 1, or ``None``.
            
        Returns:
           ``(any)``: the selected action.
           
        Example
        ----------
        ::
            
            def decide(self):
                return random([action.move(), action.turn(direction.left)], [0.8, 0.2])
        
        The agent will move with 0.8 probability and turn left with 0.2 probability.
    '''

    assert actions is not None and isinstance(actions, Iterable)

    if p is None:
        return choice(actions)
    else:
        assert isinstance(p, Iterable) and len(actions) == len(p)
        return choices(actions, weights=p, k=1)[0]
