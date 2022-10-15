from __future__ import annotations
from typing import List, Tuple, Dict, Type
from inspect import getfile
from itertools import product
from math import floor, sqrt

from pystarworldsturbo.common.action import Action
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.environment.environment import Environment
from pystarworldsturbo.environment.physics.action_executor import ActionExecutor
from pystarworldsturbo.utils.utils import ignore

from .physics.vwexecutor_factory import VWExecutorFactory
from .vwambient import VWAmbient
from .vwlocation import VWLocation
from ..actor.vwactor import VWActor
from ..actor.vwuser import VWUser
from ..actor.vwactor_appearance import VWActorAppearance
from ..actor.actor_factories import VWCleaningAgentsFactory, VWUsersFactory
from ..dirt.dirt import Dirt
from ..dirt.dirt_appearance import VWDirtAppearance
from ...common.coordinates import Coord
from ...common.direction import Direction
from ...common.colour import Colour
from ...common.observation import Observation
from ...common.orientation import Orientation
from ...common.exceptions import VWActionAttemptException, VWMalformedActionException
from ...model.actions.vwactions import VWAction, VWPhysicalAction, VWCommunicativeAction


class VWEnvironment(Environment):
    def __init__(self, config: dict, ambient: VWAmbient, initial_actors: List[VWActor]=[], initial_dirts: List[Dirt]=[]) -> None:
        super(VWEnvironment, self).__init__(ambient=ambient, initial_actors=initial_actors, initial_passive_bodies=initial_dirts)

        self.__cycle: int = 0
        self.__surrogate_minds_metadata: Dict[str, str] = {}
        self.__config: dict = config

    def get_surrogate_minds_metadata(self) -> Dict[str, str]:
        return self.__surrogate_minds_metadata()

    def get_current_cycle_number(self) -> int:
        return self.__cycle

    def get_actors(self) -> Dict[str, VWActor]:
        return super(VWEnvironment, self).get_actors()

    def get_actor(self, actor_id: str) -> VWActor:
        return super(VWEnvironment, self).get_actor(actor_id=actor_id)

    def get_user(self, user_id) -> VWUser:
        assert self.get_actor_colour(actor_id=user_id) == Colour.user

        return self.get_actor(actor_id=user_id)

    def validate_actions(self, actions: List[Action]) -> None:
        ignore(self)

        n: int = self.__config["max_number_of_actions_per_actor_per_cycle"]

        if len(actions) > n:
            raise VWActionAttemptException("Too many actions were attempted. There is a hard limit of 1 physical action, and 1 communicative action per actor per cycle.")
        elif len(actions) == n and isinstance(actions[0], VWPhysicalAction) and isinstance(actions[1], VWPhysicalAction):
            raise VWActionAttemptException("Too many physical actions were attempted. There is a hard limit of 1 physical action, and 1 communicative action per actor per cycle.")
        elif len(actions) == n and isinstance(actions[0], VWCommunicativeAction) and isinstance(actions[1], VWCommunicativeAction):
            raise VWActionAttemptException("Too many communicative actions were attempted. There is a hard limit of 1 physical action, and 1 communicative action per actor per cycle.")

        for action in actions:
            if not isinstance(action, VWPhysicalAction) and not isinstance(action, VWCommunicativeAction):
                raise VWMalformedActionException("Unrecognised action: {}.".format(type(action)))

    def get_executor_for(_, action: Action) -> ActionExecutor:
        return VWExecutorFactory.get_executor_for(action=action)

    def evolve(self) -> None:
        if self.__cycle == 0:
            self.__force_initial_perception_to_actors()  # For back compatibility with 4.1.8.
        else:
            self.execute_cycle_actions()

        self.__cycle += 1

    def __force_initial_perception_to_actors(self) -> None:
        for actor_id in self.get_actors():
            observation: Observation = self.generate_perception_for_actor(actor_id=actor_id, action_type=VWAction, action_result=ActionResult(outcome=ActionOutcome.impossible))

            self.send_perception_to_actor(perception=observation, actor_id=actor_id)

    def get_ambient(self) -> VWAmbient:
        return super(VWEnvironment, self).get_ambient()

    def move_actor(self, from_coord: Coord, to_coord: Coord) -> None:
        self.get_ambient().move_actor(from_coord=from_coord, to_coord=to_coord)

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

    def generate_perception_for_actor(self, actor_id: str, action_type: Type[VWAction], action_result: ActionResult) -> Observation:
        assert actor_id in self.get_actors()

        coord: Coord = self.get_actor_position(actor_id=actor_id)

        return self.get_ambient().generate_perception(actor_position=coord, action_type=action_type, action_result=action_result)

    def get_actor_position(self, actor_id) -> Coord:
        assert actor_id in self.get_actors()

        return self.__get_actor_position_and_location(actor_id=actor_id)[0]

    def get_actor_location(self, actor_id) -> VWLocation:
        assert actor_id in self.get_actors()

        return self.__get_actor_position_and_location(actor_id=actor_id)[1]

    def __get_actor_position_and_location(self, actor_id) -> Tuple[Coord, VWLocation]:
        assert actor_id in self.get_actors()

        for c, l in self.get_ambient().get_grid().items():
            if l.has_actor() and l.get_actor_appearance().get_id() == actor_id:
                return c, l

        raise ValueError("Actor {} not found: there is an inconsistency between the grid and the list of actors.".format(actor_id))

    def get_actor_orientation(self, actor_id: str) -> Orientation:
        assert actor_id in self.get_actors()

        return self.get_actor_location(actor_id=actor_id).get_actor_appearance().get_orientation()

    def get_actor_previous_orientation(self, actor_id: str) -> Orientation:
        assert actor_id in self.get_actors()

        return self.get_actor_location(actor_id=actor_id).get_actor_appearance().get_previous_orientation()

    def get_actor_colour(self, actor_id: str) -> Colour:
        assert actor_id in self.get_actors()

        return self.get_actor_location(actor_id=actor_id).get_actor_appearance().get_colour()

    def __get_actor_surrogate_mind_file(self, actor_id: str) -> str:
        assert actor_id in self.get_actors()

        return getfile(self.get_actor(actor_id=actor_id).get_mind().get_surrogate().__class__)

    # Note that the actor IDs, progressive IDs, and the user difficulty level are not stored.
    # Therefore, on load the actors will have fresh IDs and progressive IDs, and the user will be in easy mode.
    def to_json(self) -> Dict[str, List[Dict[str, Dict[str, str | int]]]]:
        state: Dict[str, List[Dict[str, Dict[str, str | int]]]] = {
            "locations": []
        }

        for loc in self.get_ambient().get_grid().values():
            location: dict = loc.to_json()

            if loc.has_cleaning_agent():
                actor_id: str = loc.get_actor_appearance().get_id()

                location["actor"]["surrogate_mind_file"] = self.__get_actor_surrogate_mind_file(actor_id=actor_id)
                location["actor"]["surrogate_mind_class_name"] = self.get_actor(actor_id=actor_id).get_mind().get_surrogate().__class__.__name__

            state["locations"].append(location)

        return state

    # This is meant to throw an exception if something goes wrong.
    @staticmethod
    def from_json(data: Dict[str, List[Dict[str, Dict[str, str | int]]]], config: dict) -> VWEnvironment:
        grid: Dict[Coord, VWLocation] = {}
        actors: List[VWActorAppearance] = []
        dirts: List[Dirt] = []

        if not data:
            return VWEnvironment.generate_empty_env(config=config)

        for location_data in data["locations"]:
            coord: Coord = Coord(x=location_data["coords"]["x"], y=location_data["coords"]["y"])
            actor: VWActor = None
            actor_appearance: VWActorAppearance = None
            dirt: Dirt = None
            dirt_appearance: VWDirtAppearance = None

            if "actor" in location_data and location_data["actor"]["colour"] != str(Colour.user):
                actor, actor_appearance = VWCleaningAgentsFactory.create_cleaning_agent_from_json_data(data=location_data["actor"])
                actors.append(actor)
            elif "actor" in location_data and location_data["actor"]["colour"] == str(Colour.user):
                actor, actor_appearance = VWUsersFactory.create_user_from_json_data(data=location_data["actor"])
                actors.append(actor)

            if "dirt" in location_data:
                dirt = Dirt(colour=Colour(location_data["dirt"]["colour"]))
                dirt_appearance = VWDirtAppearance(dirt_id=dirt.get_id(), progressive_id=dirt.get_progressive_id(), colour=dirt.get_colour())
                dirts.append(dirt)

            wall: Dict[Orientation, bool] = {Orientation.north: location_data["wall"][str(Orientation.north)], Orientation.south: location_data["wall"][str(Orientation.south)], Orientation.west: location_data["wall"][str(Orientation.west)], Orientation.east: location_data["wall"][str(Orientation.east)]}

            grid[coord] = VWLocation(coord=coord, actor_appearance=actor_appearance, dirt_appearance=dirt_appearance, wall=wall)

        VWEnvironment.__validate_grid(grid=grid, config=config)

        return VWEnvironment(config=config, ambient=VWAmbient(grid=grid), initial_actors=actors, initial_dirts=dirts)

    @staticmethod
    def generate_empty_env(config: dict, forced_line_dim: int=-1) -> VWEnvironment:
        try:
            line_dim: int = config["initial_environment_dim"]

            if forced_line_dim != -1:
                assert forced_line_dim >= config["min_environment_dim"] and forced_line_dim <= config["max_environment_dim"]
                line_dim = forced_line_dim

            grid: Dict[Coord, VWLocation] = {Coord(x, y): VWLocation(coord=Coord(x, y), actor_appearance=None, dirt_appearance=None, wall=VWEnvironment.generate_wall_from_coordinates(coord=Coord(x, y), grid_size=line_dim)) for x, y in product(range(line_dim), range(line_dim))}

            VWEnvironment.__validate_grid(grid=grid, config=config, candidate_grid_line_dim=line_dim)

            return VWEnvironment(config=config, ambient=VWAmbient(grid=grid), initial_actors=[], initial_dirts=[])
        except AssertionError as e:
            raise e
        except Exception:
            raise IOError("Could not construct the environment from the given config.")

    @staticmethod
    def generate_wall_from_coordinates(coord: Coord, grid_size: int) -> Dict[Orientation, bool]:
        default_wall: Dict[Orientation, bool] = {Orientation.north: False, Orientation.south: False, Orientation.west: False, Orientation.east: False}

        if coord.x == 0:
            default_wall[Orientation.west] = True
        if coord.x == grid_size - 1:
            default_wall[Orientation.east] = True
        if coord.y == 0:
            default_wall[Orientation.north] = True
        if coord.y == grid_size - 1:
            default_wall[Orientation.south] = True

        return default_wall

    @staticmethod
    def __validate_grid(grid: Dict[Coord, VWLocation], config: dict, candidate_grid_line_dim: int=-1) -> None:
        assert grid is not None and type(grid) == dict

        grid_line_dim: int = sqrt(len(grid))

        assert floor(grid_line_dim) == grid_line_dim

        if candidate_grid_line_dim != -1:
            assert candidate_grid_line_dim >= config["min_environment_dim"] and candidate_grid_line_dim <= config["max_environment_dim"]
            assert candidate_grid_line_dim == grid_line_dim

    def __str__(self) -> str:
        return str(self.get_ambient())
