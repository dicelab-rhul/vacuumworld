from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome

from ..vwenvironment import VWEnvironment
from ..vwlocation import VWLocation
from ...actions.clean_action import VWCleanAction
from ....common.coordinates import Coord
from ....common.colour import Colour



class CleanExecutor(ActionExecutor):
    @staticmethod
    def is_possible(env: VWEnvironment, action: VWCleanAction) -> bool:
        actor_id: str = action.get_actor_appearance().get_id()
        actor_position: Coord = env.get_actor_position(actor_id=actor_id)
        actor_colour: Colour = action.get_actor_appearance().get_colour()
        dirt_location: VWLocation = env.get_ambient().get_grid()[actor_position]

        if not dirt_location.has_dirt():
            return False
        elif actor_colour == Colour.white:
            return True
        elif actor_colour == Colour.user:
            return False
        else:
            return dirt_location.get_dirt_appearance().get_colour() == actor_colour

    @staticmethod
    def attempt(env: VWEnvironment, action: VWCleanAction) -> ActionResult:
        try:
            actor_id: str = action.get_actor_appearance().get_id()
            actor_position: Coord = env.get_actor_position(actor_id=actor_id)
            actor_colour: Colour = action.get_actor_appearance().get_colour()
            dirt_location: VWLocation = env.get_ambient().get_grid()[actor_position]

            assert dirt_location.has_dirt()
            assert actor_colour == Colour.white or dirt_location.get_dirt_appearance().get_colour() == actor_colour

            env.remove_dirt(coord=actor_position)

            return ActionResult(ActionOutcome.success)
        except Exception:
            return ActionResult(ActionOutcome.failure)

    @staticmethod
    def succeeded(env: VWEnvironment, action: VWCleanAction) -> bool:
        actor_id: str = action.get_actor_appearance().get_id()
        actor_position: Coord = env.get_actor_position(actor_id=actor_id)

        return not env.get_ambient().get_grid()[actor_position].has_dirt()
