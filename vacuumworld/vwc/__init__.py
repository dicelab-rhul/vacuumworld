from typing import List, Type
# This whole module only exists to ensure back compatibility with 4.1.8.

from ..common.colour import Colour # For back compatibility with 4.1.8
from ..common.coordinates import Coord # For back compatibility with 4.1.8
from ..common.direction import Direction # For back compatibility with 4.1.8
from ..common.observation import Observation # For back compatibility with 4.1.8
from ..common.orientation import Orientation # For back compatibility with 4.1.8
from ..model import actions as action # For back compatibility with 4.1.8



colour: Type = Colour # For back compatibility with 4.1.8
coord: Type = Coord # For back compatibility with 4.1.8
direction: Type = Direction # For back compatibility with 4.1.8
observation: Type = Observation # For back compatibility with 4.1.8
orientation: Type = Orientation # For back compatibility with 4.1.8

# For back compatibility with 4.1.8
__all__: List[str] = [Colour, Coord, Direction, Observation, Orientation, colour, coord, direction, observation, orientation, action]
