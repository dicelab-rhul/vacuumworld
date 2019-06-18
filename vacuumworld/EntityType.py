# -*- coding: utf-8 -*-

from enum import Enum

class CellType(Enum):
    AGENT = "Agent"
    DIRT="Dirt"
    USER="User"
    AGENTONDIRT = "AgentOnDirt"
    USERONDIRT = "AgentOnDirt"
    EMPTY="Empty"
    WALL="Wall"
class ActorType(Enum):
    AGENT = "Agent"
    USER="User"
   
class AgentColor(Enum):
    GREEN = "Green"
    ORANGE="Orange"
    WHITE="White"
    
class DirtColor(Enum):
    GREEN = "Green"
    ORANGE="Orange"
        