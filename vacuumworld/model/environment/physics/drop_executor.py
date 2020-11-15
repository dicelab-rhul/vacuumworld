from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.common.action_outcome import ActionOutcome

from ..vwlocation import VWLocation
from ..vwenvironment import VWEnvironment
from ...actions.drop_action import VWDropAction
from ....common.coordinates import Coord
from ....common.colour import Colour



class DropExecutor(ActionExecutor):
    @staticmethod
    def is_possible(env: VWEnvironment, action: VWDropAction) -> bool:
        actor_id: str = action.get_actor_appearance().get_id()
        actor_position: Coord = env.get_actor_position(actor_id=actor_id)
        actor_colour: Colour = action.get_actor_appearance().get_colour()
        dirt_location: VWLocation = env.get_ambient().get_grid()[actor_position]

        return not dirt_location.has_dirt() and actor_colour == Colour.user

    @staticmethod
    def attempt(env: VWEnvironment, action: VWDropAction) -> ActionResult:
        try:
            actor_id: str = action.get_actor_appearance().get_id()
            actor_position: Coord = env.get_actor_position(actor_id=actor_id)
            actor_colour: Colour = action.get_actor_appearance().get_colour()
            dirt_location: VWLocation = env.get_ambient().get_grid()[actor_position]

            assert not dirt_location.has_dirt() and actor_colour == Colour.user

            env.drop_dirt(coord=actor_position, dirt_colour=action.get_dirt_colour())

            return ActionResult(ActionOutcome.success)
        except Exception:
            return ActionResult(ActionOutcome.failure)

    @staticmethod
    def succeeded(env: VWEnvironment, action: VWDropAction) -> bool:
        actor_id: str = action.get_actor_appearance().get_id()
        actor_position: Coord = env.get_actor_position(actor_id=actor_id)

        return env.get_ambient().get_grid()[actor_position].has_dirt() and env.get_ambient().get_grid()[actor_position].get_dirt_appearance().get_colour() == action.get_dirt_colour()
