from __future__ import annotations
from typing import TYPE_CHECKING

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.utils.utils import ignore

from ..vwlocation import VWLocation
from ...actions.drop_action import VWDropAction
from ....common.coordinates import Coord
from ....common.colour import Colour

if TYPE_CHECKING:
    from ..vwenvironment import VWEnvironment


class DropExecutor(ActionExecutor):
    '''
    This class is an `ActionExecutor` for `VWDropAction`.
    '''
    def is_possible(self, env: VWEnvironment, action: VWDropAction) -> bool:
        '''
        Returns whether or not `action` is possible in `env`.

        In any `VWEnvironment` a `VWDropAction` is possible if:

        * The `VWLocation` that contains the `VWActor` whose ID matches the actor ID of `action` has no `Dirt` on it

        * The `VWLocation` that contains the `VWActor` whose ID matches the actor ID of `action` has a `VWUser` in it.
        '''
        ignore(self)

        actor_id: str = action.get_actor_id()
        actor_colour: Colour = env.get_actor_colour(actor_id=actor_id)
        actor_location: VWLocation = env.get_actor_location(actor_id=actor_id)

        return not actor_location.has_dirt() and actor_colour == Colour.user

    def attempt(self, env: VWEnvironment, action: VWDropAction) -> ActionResult:
        '''
        Attempts to execute `action` in `env`, returning a provisional `ActionResult`.

        If an `Exception` is raised, the provisional `ActionResult` will have an `ActionOutcome` of `ActionOutcome.failure`.

        Otherwise, the provisional `ActionResult` will have an `ActionOutcome` of `ActionOutcome.success`.
        '''
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
        '''
        Returns whether or not the post-conditions of `action` are satisfied in `env`.

        The post-conditions of a `VWDropAction` are satisfied if:

        * The `VWLocation` that contains the `VWActor` whose ID matches the actor ID of `action` has a `Dirt` on it.

        * The `Colour` of the aforementioned `Dirt` is the same as the `Colour` in `action`.
        '''
        ignore(self)

        actor_id: str = action.get_actor_id()
        actor_location: VWLocation = env.get_actor_location(actor_id=actor_id)

        return actor_location.has_dirt() and actor_location.get_dirt_appearance().get_colour() == action.get_dirt_colour()
