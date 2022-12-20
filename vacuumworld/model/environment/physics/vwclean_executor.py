from __future__ import annotations
from typing import TYPE_CHECKING

from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome

from ..vwlocation import VWLocation
from ...actions.vwclean_action import VWCleanAction
from ....common.vwcoordinates import VWCoord
from ....common.vwcolour import VWColour

if TYPE_CHECKING:
    from ..vwenvironment import VWEnvironment


class VWCleanExecutor(ActionExecutor):
    '''
    This class is an `ActionExecutor` for `VWCleanAction`.
    '''
    def is_possible(self, env: VWEnvironment, action: VWCleanAction) -> bool:
        '''
        Returns whether or not `action` is possible in `env`.

        In any `VWEnvironment` a `VWCleanAction` is possible if:

        * The `VWLocation` that contains the `VWActor` whose ID matches the actor ID of `action` has a `VWDirt` on it

        * The `VWLocation` that contains the `VWActor` whose ID matches the actor ID of `action` has a `VWCleaningAgent` in it.

        * The `VWColour` of the aforementioned `VWDirt` matches the `VWColour` of the aforementioned `VWCleaningAgent`, or the `VWColour` of the aforementioned `VWCleaningAgent` is `VWColour.white`.
        '''
        actor_id: str = action.get_actor_id()
        actor_colour: VWColour = env.get_actor_colour(actor_id=actor_id)
        actor_location: VWLocation = env.get_actor_location(actor_id=actor_id)

        if not actor_location.has_dirt():
            return False
        elif actor_colour == VWColour.white:
            return True
        elif actor_colour == VWColour.user:
            return False
        else:
            return actor_location.get_dirt_appearance().or_else_raise().get_colour() == actor_colour

    def attempt(self, env: VWEnvironment, action: VWCleanAction) -> ActionResult:
        '''
        Attempts to execute `action` in `env`, returning a provisional `ActionResult`.

        If an `Exception` is raised, the provisional `ActionResult` will have an `ActionOutcome` of `ActionOutcome.failure`.

        Otherwise, the provisional `ActionResult` will have an `ActionOutcome` of `ActionOutcome.success`.
        '''
        try:
            actor_id: str = action.get_actor_id()
            actor_position: VWCoord = env.get_actor_position(actor_id=actor_id)
            actor_colour: VWColour = env.get_actor_colour(actor_id=actor_id)
            actor_location: VWLocation = env.get_actor_location(actor_id=actor_id)

            assert actor_location.has_dirt()
            assert actor_colour == VWColour.white or actor_location.get_dirt_appearance().or_else_raise().get_colour() == actor_colour

            env.remove_dirt(coord=actor_position)

            return ActionResult(ActionOutcome.success)
        except Exception:
            return ActionResult(ActionOutcome.failure)

    def succeeded(self, env: VWEnvironment, action: VWCleanAction) -> bool:
        '''
        Returns whether or not the post-conditions of `action` are satisfied in `env`.

        The post-conditions of a `VWCleanAction` are satisfied if the `VWLocation` that contains the `VWActor` whose ID matches the actor ID of `action` has no `VWDirt` on it.
        '''
        actor_id: str = action.get_actor_id()
        actor_location: VWLocation = env.get_actor_location(actor_id=actor_id)

        return not actor_location.has_dirt()
