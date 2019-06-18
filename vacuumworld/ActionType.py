# -*- coding: utf-8 -*-from enum import Enum
from enum import Enum

class ActionType(Enum):
    
    CLEANDIRT="Clean",
    MOVEFORWARD="Forward",
    MOVERIGHT="Right",
    MOVELEFT="Left",
    
    SPEAK="Speak"
    BROADCAST="Broadcast"
    DROPDIRT="Dropdirt"

class PerceptionType(Enum):
      COMMUNICATION="CommunicationPerception"
      VISION="VisionPerception"
     
class ActionResult(Enum):
      SUCCESS="SUCCESS"
      FAILURE="FAILURE"
      IMPOSSIBLE="Impossible"          