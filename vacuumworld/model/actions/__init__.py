from typing import Type

from .broadcast_action import VWBroadcastAction
from .clean_action import VWCleanAction
from .drop_action import VWDropAction
from .idle_action import VWIdleAction
from .move_action import VWMoveAction
from .speak_action import VWSpeakAction
from .turn_action import VWTurnAction



broadcast: Type = VWBroadcastAction
clean: Type = VWCleanAction
drop: Type = VWDropAction
idle: Type = VWIdleAction
move: Type = VWMoveAction
speak: Type = VWSpeakAction
turn: Type = VWTurnAction
