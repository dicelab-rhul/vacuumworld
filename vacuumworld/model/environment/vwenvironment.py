from typing import List

from pystarworldsturbo.common.action import Action
from pystarworldsturbo.environment.environment import Environment

from .vwambient import VWAmbient
from ..actor.vwagent import VWCleaningAgent
from ..dirt.dirt import Dirt
from ..dirt.dirt_appearance import VWDirtAppearance
from ...common.coordinates import Coord
from ...common.direction import Direction
from ...common.colour import Colour
from ...common.observation import Observation
from ...model.actions.vwactions import VWPhysicalAction, VWCommunicativeAction
from ...utils.exceptions import VWActionAttemptException, VWMalformedActionException



class VWEnvironment(Environment):
    def __init__(self, ambient: VWAmbient, initial_actors: List[VWCleaningAgent]=[], initial_dirts: List[Dirt]=[]) -> None:
        super(VWEnvironment, self).__init__(ambient=ambient, initial_actors=initial_actors, initial_passive_bodies=initial_dirts)

    # TODO: extract the magic number to the config file.
    def validate_actions(*actions: Action) -> None:
        if len(actions) > 2:
            raise VWActionAttemptException("Too many actions were attempted. There is a hard limit of 1 physical action, and 1 communicative action per agent per cycle.")
        elif len(actions) == 2 and isinstance(actions[0], VWPhysicalAction) and isinstance(actions[1], VWPhysicalAction):
            raise VWActionAttemptException("Too many physical actions were attempted. There is a hard limit of 1 physical action, and 1 communicative action per agent per cycle.")
        elif len(actions) == 2 and isinstance(actions[0], VWCommunicativeAction) and isinstance(actions[1], VWCommunicativeAction):
            raise VWActionAttemptException("Too many communicative actions were attempted. There is a hard limit of 1 physical action, and 1 communicative action per agent per cycle.")
        
        for action in actions:
            if not isinstance(action, VWPhysicalAction) and not isinstance(action, VWCommunicativeAction):
                raise VWMalformedActionException("Unrecognised action: {}.".format(type(action)))

    def run(self) -> None:
        while True:
            self.execute_cycle_actions()

    def get_ambient(self) -> VWAmbient:
        return super(VWEnvironment, self).get_ambient()

    def move_actor(self, from: Coord, to: Coord) -> None:
        self.get_ambient().move_actor(from=from, to=to)

    def turn_actor(self, coord: Coord, direction: Direction) -> None:
        self.get_ambient().turn_actor(coord=coord, direction=direction)

    def remove_dirt(self, coord: Coord) -> None:
        assert self.get_ambient().is_dirt_at(coord=coord)
        
        dirt_id: str = self.get_ambient().get_grid()[coord].get_dirt_appearance().get_id()

        # Removing the dirt from the list of passive bodies.
        self.remove_passive_body(passive_body_id=dirt_id)

        # Removing the dirt from the grid.
        self.get_ambient().remove_dirt(coord=coord)

    def drop_dirt(self, coord: Coord, dirt_colour: Colour) -> None:
        dirt: Dirt = Dirt(colour=dirt_colour)
        dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=dirt.get_id(), progressive_id=dirt.get_progressive_id(), colour=dirt.get_colour())

        # Adding the dirt to the list of passive bodies.
        self.add_passive_body(passive_body=dirt)

        # Adding the dirt to the grid.
        self.get_ambient().drop_dirt(coord=coord, dirt_appearance=dirt_appearance)

    def generate_perception_for_actor_at(self, coord: Coord) -> Observation:
        return self.get_ambient().generate_perception(coord=coord)

    def get_actor_position(self, actor_id) -> Coord:
        assert actor_id in self.get_actors()

        for c, l in self.get_ambient().get_grid().items():
            if l.has_actor() and l.get_actor_appearance().get_id() == actor_id:
                return c
