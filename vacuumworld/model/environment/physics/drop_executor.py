from __future__ import annotations
from typing import TYPE_CHECKING

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome

from ..vwlocation import VWLocation
from ...actions.drop_action import VWDropAction
from ....common.coordinates import Coord
from ....common.colour import Colour

from ....utils.vwutils import ignore

if TYPE_CHECKING:
    from ..vwenvironment import VWEnvironment



class DropExecutor(ActionExecutor):
    def is_possible(self, env: VWEnvironment, action: VWDropAction) -> bool:
        ignore(self)

        actor_id: str = action.get_actor_id()
        actor_colour: Colour = env.get_actor_colour(actor_id=actor_id)
        actor_location: VWLocation = env.get_actor_location(actor_id=actor_id)

        return not actor_location.has_dirt() and actor_colour == Colour.user

    def attempt(self, env: VWEnvironment, action: VWDropAction) -> ActionResult:
        ignore(self)
        
        try:
            actor_id: str = action.get_actor_id()
            actor_position: Coord = env.get_actor_position(actor_id=actor_id)
            actor_colour: Colour = env.get_actor_colour(actor_id=actor_id)
            actor_location: VWLocation = env.get_actor_location(actor_id=actor_id)

            assert not actor_location.has_dirt() and actor_colour == Colour.user

            env.drop_dirt(coord=actor_position, dirt_colour=action.get_dirt_colour())

            return ActionResult(ActionOutcome.success)
        except Exception:
            return ActionResult(ActionOutcome.failure)

    def succeeded(self, env: VWEnvironment, action: VWDropAction) -> bool:
        ignore(self)
        
        actor_id: str = action.get_actor_id()
        actor_location: VWLocation = env.get_actor_location(actor_id=actor_id)

        return actor_location.has_dirt() and actor_location.get_dirt_appearance().get_colour() == action.get_dirt_colour()
