from __future__ import annotations
from typing import List, Tuple, Dict, Type, Optional, Union
from inspect import getsourcefile
from itertools import product
from math import floor, sqrt
from random import randint

from pystarworldsturbo.common.action import Action
from pystarworldsturbo.common.action_outcome import ActionOutcome
from pystarworldsturbo.common.action_result import ActionResult
from pystarworldsturbo.environment.environment import Environment
from pystarworldsturbo.environment.physics.action_executor import ActionExecutor

from .physics.vwexecutor_factory import VWExecutorFactory
from .vwambient import VWAmbient
from .vwlocation import VWLocation
from ..actor.vwactor import VWActor
from ..actor.vwuser import VWUser
from ..actor.appearance.vwactor_appearance import VWActorAppearance
from ..actor.vwactor_factories import VWCleaningAgentsFactory, VWUsersFactory
from ...common.vwuser_difficulty import VWUserDifficulty
from ..actor.mind.surrogate.vwhysteretic_mind_surrogate import VWHystereticMindSurrogate
from ..dirt.vwdirt import VWDirt
from ..dirt.vwdirt_appearance import VWDirtAppearance
from ...common.vwcoordinates import VWCoord
from ...common.vwdirection import VWDirection
from ...common.vwcolour import VWColour
from ...common.vwobservation import VWObservation
from ...common.vworientation import VWOrientation
from ...common.vwexceptions import VWActionAttemptException, VWMalformedActionException, VWInternalError
from ...model.actions.vwactions import VWAction, VWPhysicalAction, VWCommunicativeAction


class VWEnvironment(Environment):
    '''
    This class represents the environment in which the simulation takes place.

    A `VWEnvironment` is made of:

    * A `VWAmbient` (itself a wrapper for a grid mapping `VWCoord` objects to `VWLocation` objects)

    * A collection of `VWActor` objects.

    * A collection of `VWDirt` objects.

    An API is provided to interact with the `VWAmbient`, the `VWActor` objects, and the `VWDirt` objects.

    A `VWEnvironment` evolves in cycles, starting at cycle `0`. Each environmental cycle is composed of:

    * A feedback phase, in which the `VWEnvironment` sends to each `VWActor` a `VWObservation` of the surroundings of such `VWActor` and pending messages from other `VWActor` instances.

    * A physical/communicative evolution phase, in which each `VWActor` potentially attempts to modify the `VWEnvironment` via a `VWPhysicalAction`, and potentially engages in communications via a `VWCommunicativeAction`.
    Only one `VWPhysicalAction` and one `VWCommunicativeAction` can be attempted per cycle per `VWActor`.
    '''
    def __init__(self, config: dict, ambient: VWAmbient, initial_actors: List[VWActor]=[], initial_dirts: List[VWDirt]=[]) -> None:
        super(VWEnvironment, self).__init__(ambient=ambient, initial_actors=initial_actors, initial_passive_bodies=initial_dirts)

        self.__cycle: int = -1
        self.__config: dict = config

    def can_evolve(self) -> bool:
        '''
        Returns whether or not this `VWEnvironment` can evolve.

        The `VWEnvironment` can evolve if the (potentially infinite) upper limit on the number of cycles has not been reached yet.
        '''
        if self.__config["total_cycles"] == 0:
            return True
        else:
            return self.__cycle < self.__config["total_cycles"]

    def get_current_cycle_number(self) -> int:
        '''
        Returns the current cycle number as an `int`.
        '''
        return self.__cycle

    def get_actors(self) -> Dict[str, VWActor]:
        '''
        Returns a `Dict[str, VWActor]` mapping `VWActor` IDs to `VWActor` objects for each `VWActor` in the `VWEnvironment`.
        '''
        return super(VWEnvironment, self).get_actors()

    def get_actor(self, actor_id: str) -> Optional[VWActor]:
        '''
        Returns the `VWActor` with the given `actor_id` if it exists, `None` otherwise.
        '''
        return super(VWEnvironment, self).get_actor(actor_id=actor_id)

    def get_user(self, user_id) -> Optional[VWUser]:
        '''
        Returns the `VWUser` with the given `user_id` if it exists, `None` otherwise.

        This method assumes (via assertion) that the potential `VWActor` whose ID matches `user_id` is a `VWUser`.
        '''
        assert self.get_actor_colour(actor_id=user_id) == VWColour.user

        return self.get_actor(actor_id=user_id)

    def validate_actions(self, actions: List[Action]) -> None:
        '''
        Validates the pool of `VWAction` instances attempted by a certain `VWActor` in this cycle, before the proper attempts can begin.

        In particular, this method checks that:

        * The number of actions attempted is within the allowed range.

        * Each attempted `VWAction` is compatible with the `VWEnvironment`.

        * The correct mix of `VWPhysicalAction` and `VWCommunicativeAction` is attempted.
        '''
        self.__validate_number_of_actions(actions=actions)

        VWEnvironment.__validate_action_types(actions=actions)

        self.__validate_pool_of_actions(actions=actions)

    def __validate_number_of_actions(self, actions: List[Action]) -> None:
        n: int = self.__config["max_number_of_actions_per_actor_per_cycle"]

        assert n > 0

        if len(actions) == 0:
            raise VWActionAttemptException("No actions were attempted. At least 1 action must be attempted per cycle.")
        elif len(actions) > n:
            raise VWActionAttemptException("Too many actions were attempted. There is a hard limit of {} actions per actor per cycle.".format(n))

    @staticmethod
    def __validate_action_types(actions: List[Action]) -> None:
        for action in actions:
            if not isinstance(action, VWPhysicalAction) and not isinstance(action, VWCommunicativeAction):
                raise VWMalformedActionException("Unrecognised action: {}.".format(type(action)))

    def __validate_pool_of_actions(self, actions: List[Action]) -> None:
        n: int = self.__config["max_number_of_actions_per_actor_per_cycle"]
        n_physical: int = self.__config["max_number_of_physical_actions_per_actor_per_cycle"]
        n_communicative: int = self.__config["max_number_of_communicative_actions_per_actor_per_cycle"]

        # Self-consistency assertion in the config data.
        assert n_physical + n_communicative == n

        # The check that at least one `VWAction` (and no more than `n`) is attempted has already been done in `__validate_number_of_actions()`. Hence, this is an assertion, and not a conditional statement.
        assert 0 < len(actions) <= n

        if sum(map(lambda action: isinstance(action, VWPhysicalAction), actions)) > n_physical:
            raise VWActionAttemptException("Too many physical actions were attempted. There is a hard limit of {} physical action, and {} communicative action per actor per cycle.".format(n_physical, n_communicative))

        if sum(map(lambda action: isinstance(action, VWCommunicativeAction), actions)) > n_communicative:
            raise VWActionAttemptException("Too many communicative actions were attempted. There is a hard limit of {} physical action, and {} communicative action per actor per cycle.".format(n_physical, n_communicative))

    def get_executor_for(_, action: Action) -> Optional[ActionExecutor]:
        '''
        Returns the `ActionExecutor` that can execute the given `Action` if it exists, `None` otherwise.
        '''
        return VWExecutorFactory.get_executor_for(action=action)

    def evolve(self) -> None:
        '''
        Evolves this `VWEnvironment` by one cycle.
        '''
        if self.__cycle == -1:
            self.__force_initial_perception_to_actors()  # For back compatibility with 4.1.8.
        else:
            self.execute_cycle_actions()

        self.__cycle += 1

    def __force_initial_perception_to_actors(self) -> None:
        for actor_id in self.get_actors():
            observation: VWObservation = self.generate_perception_for_actor(actor_id=actor_id, action_type=VWAction, action_result=ActionResult(outcome=ActionOutcome.impossible))

            self.send_perception_to_actor(perception=observation, actor_id=actor_id)

    def get_ambient(self) -> VWAmbient:
        '''
        Returns the `VWAmbient` of this `VWEnvironment`.
        '''
        return super(VWEnvironment, self).get_ambient()

    def move_actor(self, from_coord: VWCoord, to_coord: VWCoord) -> None:
        '''
        Moves the `VWActor` curently at the `VWLocation` whose `VWCoord` matches `from_coord` to the `VWLocation` whose `VWCoord` matches `to_coord`, if possible.

        This method is a wrapper around the `move_actor()` method of `VWAmbient`.
        '''
        self.get_ambient().move_actor(from_coord=from_coord, to_coord=to_coord)

    def turn_actor(self, coord: VWCoord, direction: VWDirection) -> None:
        '''
        Turns the `VWActor` curently at the `VWLocation` whose `VWCoord` matches `coord` as specified by `direction`, if possible.

        This method is a wrapper around the `turn_actor()` method of `VWAmbient`.
        '''
        self.get_ambient().turn_actor(coord=coord, direction=direction)

    def remove_dirt(self, coord: VWCoord) -> None:
        '''
        Removes the dirt currently on the `VWLocation` whose `VWCoord` matches `coord`, if possible.

        Both the `VWAmbient` grid, and the collection of `VWDirt` objects are updated.

        This method assumes (via assertion) that there is a `VWDirt` on the `VWLocation` whose `VWCoord` matches `coord`.
        '''
        assert self.get_ambient().is_dirt_at(coord=coord)

        dirt_id: str = self.get_ambient().get_grid()[coord].get_dirt_appearance().get_id()

        # Removing the dirt from the list of passive bodies.
        self.remove_passive_body(passive_body_id=dirt_id)

        # Removing the dirt from the grid.
        self.get_ambient().remove_dirt(coord=coord)

    def drop_dirt(self, coord: VWCoord, dirt_colour: VWColour) -> None:
        '''
        Drops a `VWDirt` of the specified `dirt_colour` onto the `VWLocation` whose `VWCoord` matches `coord`, if possible.

        Both the `VWAmbient` grid, and the collection of `VWDirt` objects are updated.
        '''
        dirt: VWDirt = VWDirt(colour=dirt_colour)
        dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=dirt.get_id(), progressive_id=dirt.get_progressive_id(), colour=dirt.get_colour())

        # Adding the dirt to the list of passive bodies.
        self.add_passive_body(passive_body=dirt)

        # Adding the dirt to the grid.
        self.get_ambient().drop_dirt(coord=coord, dirt_appearance=dirt_appearance)

    def generate_perception_for_actor(self, actor_id: str, action_type: Type[VWAction], action_result: ActionResult) -> VWObservation:
        '''
        Generates and returns a `VWObservation` perception for the `VWActor` with the specified `actor_id` as a result of the execution of the specified `action_type` with the specified `action_result`.

        This method is a wrapper around the `generate_perception_for_actor()` method of `VWAmbient`.

        This method assumes (via assertion) that the `VWActor` with the specified `actor_id` exists in the `VWEnvironment`.
        '''
        assert actor_id in self.get_actors()

        coord: VWCoord = self.get_actor_position(actor_id=actor_id)

        return self.get_ambient().generate_perception(actor_position=coord, action_type=action_type, action_result=action_result)

    def get_actor_position(self, actor_id: str) -> VWCoord:
        '''
        Returns the `VWCoord` of the `VWLocation` containing the `VWActor` with the specified `actor_id`.

        This method assumes (via assertion) that the `VWActor` with the specified `actor_id` exists in the `VWEnvironment`.
        '''
        assert actor_id in self.get_actors()

        return self.__get_actor_position_and_location(actor_id=actor_id)[0]

    def get_actor_location(self, actor_id: str) -> VWLocation:
        '''
        Returns the `VWLocation` containing the `VWActor` with the specified `actor_id`.

        This method assumes (via assertion) that the `VWActor` with the specified `actor_id` exists in the `VWEnvironment`.
        '''
        assert actor_id in self.get_actors()

        return self.__get_actor_position_and_location(actor_id=actor_id)[1]

    def __get_actor_position_and_location(self, actor_id: str) -> Tuple[VWCoord, VWLocation]:
        assert actor_id in self.get_actors()

        for c, l in self.get_ambient().get_grid().items():
            if l.has_actor() and l.get_actor_appearance().get_id() == actor_id:
                return c, l

        raise VWInternalError("Actor {} not found: there is an inconsistency between the grid and the list of actors.".format(actor_id))

    def get_actor_orientation(self, actor_id: str) -> VWOrientation:
        '''
        Returns the `VWOrientation` of the `VWActor` with the specified `actor_id`.

        This method assumes (via assertion) that the `VWActor` with the specified `actor_id` exists in the `VWEnvironment`.
        '''
        assert actor_id in self.get_actors()

        return self.get_actor_location(actor_id=actor_id).get_actor_appearance().get_orientation()

    def get_actor_previous_orientation(self, actor_id: str) -> VWOrientation:
        '''
        Returns the backed-up (before a turn left/right) `VWOrientation` of the `VWActor` with the specified `actor_id`.

        If the `VWActor` with the specified `actor_id` has never turned left/right, then the returned `VWOrientation` should match the current `VWOrientation`.

        This method assumes (via assertion) that the `VWActor` with the specified `actor_id` exists in the `VWEnvironment`.
        '''
        assert actor_id in self.get_actors()

        return self.get_actor_location(actor_id=actor_id).get_actor_appearance().get_previous_orientation()

    def get_actor_colour(self, actor_id: str) -> VWColour:
        '''
        Returns the `VWColour` of the `VWActor` with the specified `actor_id`.

        This method assumes (via assertion) that the `VWActor` with the specified `actor_id` exists in the `VWEnvironment`.
        '''
        assert actor_id in self.get_actors()

        return self.get_actor_location(actor_id=actor_id).get_actor_appearance().get_colour()

    def __get_actor_surrogate_mind_file(self, actor_id: str) -> str:
        assert actor_id in self.get_actors()

        return getsourcefile(self.get_actor(actor_id=actor_id).get_mind().get_surrogate().__class__)

    # Note that the actor IDs, progressive IDs, and the user difficulty level are not stored.
    # Therefore, on load the actors will have fresh IDs and progressive IDs, and the user will be in easy mode.
    def to_json(self) -> Dict[str, List[Dict[str, Dict[str, str | int]]]]:
        '''
        Returns a JSON representation of the `VWEnvironment`.

        No `VWActor` IDs, `VWActor` progressive IDs, or `VWUserDifficulty` are stored.
        '''
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

    # This method is meant to throw an exception if something goes wrong.
    @staticmethod
    def from_json(data: Dict[str, List[Dict[str, Dict[str, str | int]]]], config: dict) -> VWEnvironment:
        '''
        Creates and returns a `VWEnvironment` from the specified JSON representation (`data`) and `config`.

        Each `VWActor` will have a fresh ID and progressive ID, each `VWUser` will be in whatever mode is the default one.
        '''
        grid: Dict[VWCoord, VWLocation] = {}
        actors: List[VWActorAppearance] = []
        dirts: List[VWDirt] = []

        if not data:
            return VWEnvironment.generate_empty_env(config=config)

        for location_data in data["locations"]:
            coord: VWCoord = VWCoord(x=location_data["coords"]["x"], y=location_data["coords"]["y"])
            actor, actor_appearance = VWEnvironment.__load_actor(location_data=location_data)
            dirt, dirt_appearance = VWEnvironment.__load_dirt(location_data=location_data)

            assert actor and actor_appearance or not actor and not actor_appearance
            assert dirt and dirt_appearance or not dirt and not dirt_appearance

            actors = actors + [actor] if actor else actors
            dirts = dirts + [dirt] if dirt else dirts
            wall: Dict[VWOrientation, bool] = {o: location_data["wall"][str(o)] for o in VWOrientation}

            grid[coord] = VWLocation(coord=coord, actor_appearance=actor_appearance, dirt_appearance=dirt_appearance, wall=wall)

        VWEnvironment.__validate_grid(grid=grid, config=config)

        return VWEnvironment(config=config, ambient=VWAmbient(grid=grid), initial_actors=actors, initial_dirts=dirts)

    @staticmethod
    def __load_actor(location_data: Dict[str, Dict[str, Union[str, int]]]) -> Tuple[Optional[VWActor], Optional[VWActorAppearance]]:
        if "actor" in location_data:
            return VWCleaningAgentsFactory.create_cleaning_agent_from_json_data(data=location_data["actor"]) if location_data["actor"]["colour"] != str(VWColour.user) else VWUsersFactory.create_user_from_json_data(data=location_data["actor"])
        else:
            return None, None

    @staticmethod
    def __load_dirt(location_data: Dict[str, Dict[str, Union[str, int]]]) -> Tuple[Optional[VWDirt], Optional[VWDirtAppearance]]:
        if "dirt" in location_data:
            dirt = VWDirt(colour=VWColour(location_data["dirt"]["colour"]))
            dirt_appearance = VWDirtAppearance(dirt_id=dirt.get_id(), progressive_id=dirt.get_progressive_id(), colour=dirt.get_colour())

            return dirt, dirt_appearance
        else:
            return None, None

    @staticmethod
    def generate_empty_env(config: dict, forced_line_dim: int=-1) -> VWEnvironment:
        '''
        Generates and returns an empty `VWEnvironment` from the specified `config`.
        '''
        try:
            line_dim: int = config["initial_environment_dim"]

            if forced_line_dim != -1:
                assert forced_line_dim >= config["min_environment_dim"] and forced_line_dim <= config["max_environment_dim"]

                line_dim = forced_line_dim

            grid: Dict[VWCoord, VWLocation] = {VWCoord(x=x, y=y): VWLocation(coord=VWCoord(x=x, y=y), actor_appearance=None, dirt_appearance=None, wall=VWEnvironment.generate_wall_from_coordinates(coord=VWCoord(x=x, y=y), grid_size=line_dim)) for x, y in product(range(line_dim), range(line_dim))}

            VWEnvironment.__validate_grid(grid=grid, config=config, candidate_grid_line_dim=line_dim)

            return VWEnvironment(config=config, ambient=VWAmbient(grid=grid), initial_actors=[], initial_dirts=[])
        except AssertionError as e:
            raise e
        except Exception:
            raise IOError("Could not construct the environment from the given config.")

    @staticmethod
    def generate_wall_from_coordinates(coord: VWCoord, grid_size: int) -> Dict[VWOrientation, bool]:
        '''
        Generates and returns a `Dict[Orientation, bool]` wall for the specified `coord`, given `grid_size`.
        '''
        default_wall: Dict[VWOrientation, bool] = {VWOrientation.north: False, VWOrientation.south: False, VWOrientation.west: False, VWOrientation.east: False}

        if coord.get_x() == 0:
            default_wall[VWOrientation.west] = True
        if coord.get_x() == grid_size - 1:
            default_wall[VWOrientation.east] = True
        if coord.get_y() == 0:
            default_wall[VWOrientation.north] = True
        if coord.get_y() == grid_size - 1:
            default_wall[VWOrientation.south] = True

        return default_wall

    @staticmethod
    def __validate_grid(grid: Dict[VWCoord, VWLocation], config: dict, candidate_grid_line_dim: int=-1) -> None:
        assert grid is not None and type(grid) == dict

        grid_line_dim: int = sqrt(len(grid))

        assert floor(grid_line_dim) == grid_line_dim

        if candidate_grid_line_dim != -1:
            assert candidate_grid_line_dim >= config["min_environment_dim"] and candidate_grid_line_dim <= config["max_environment_dim"]
            assert candidate_grid_line_dim == grid_line_dim

    def __str__(self) -> str:
        return str(self.get_ambient())

    @staticmethod
    def generate_random_env_for_testing(config: dict, custom_grid_size: bool) -> Tuple[VWEnvironment, int]:
        '''
        Generates and returns a random `VWEnvironment` for testing purposes, given `config`.

        If `custom_grid_size` is `True`, the grid size will be randomly generated between `config["min_environment_dim"]` and `config["max_environment_dim"]` (both inclusive).
        '''
        green_agent_orientation: VWOrientation = VWOrientation.random()
        orange_agent_orientation: VWOrientation = VWOrientation.random()
        white_agent_orientation: VWOrientation = VWOrientation.random()
        user_orientation: VWOrientation = VWOrientation.random()
        difficutly_level: VWUserDifficulty = VWUserDifficulty.random()

        green_agent, green_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=VWColour.green, orientation=green_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        orange_agent, orange_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=VWColour.orange, orientation=orange_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        white_agent, white_agent_appearance = VWCleaningAgentsFactory.create_cleaning_agent(colour=VWColour.white, orientation=white_agent_orientation, mind_surrogate=VWHystereticMindSurrogate())
        user, user_appearance = VWUsersFactory.create_user(difficulty_level=difficutly_level, orientation=user_orientation)

        green_dirt: VWDirt = VWDirt(colour=VWColour.green)
        green_dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=green_dirt.get_id(), progressive_id=green_dirt.get_progressive_id(), colour=VWColour.green)

        orange_dirt: VWDirt = VWDirt(colour=VWColour.orange)
        orange_dirt_appearance: VWDirtAppearance = VWDirtAppearance(dirt_id=orange_dirt.get_id(), progressive_id=orange_dirt.get_progressive_id(), colour=VWColour.orange)

        env, grid_size = VWEnvironment.generate_empty_env_for_testing(custom_grid_size=custom_grid_size, config=config)

        env.add_actor(actor=green_agent)
        env.add_actor(actor=orange_agent)
        env.add_actor(actor=white_agent)
        env.add_actor(actor=user)
        env.add_passive_body(passive_body=green_dirt)
        env.add_passive_body(passive_body=orange_dirt)

        green_agent_coord, orange_agent_coord, white_agent_coord, user_coord = VWEnvironment.generate_mutually_exclusive_coordinates_for_testing(amount=4, grid_size=grid_size)
        green_dirt_coord, orange_dirt_coord = VWEnvironment.generate_mutually_exclusive_coordinates_for_testing(amount=2, grid_size=grid_size)

        env.get_ambient().get_grid()[green_agent_coord] = VWLocation(coord=green_agent_coord, actor_appearance=green_agent_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=green_agent_coord, grid_size=grid_size))
        env.get_ambient().get_grid()[orange_agent_coord] = VWLocation(coord=orange_agent_coord, actor_appearance=orange_agent_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=orange_agent_coord, grid_size=grid_size))
        env.get_ambient().get_grid()[white_agent_coord] = VWLocation(coord=white_agent_coord, actor_appearance=white_agent_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=white_agent_coord, grid_size=grid_size))
        env.get_ambient().get_grid()[user_coord] = VWLocation(coord=user_coord, actor_appearance=user_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=user_coord, grid_size=grid_size))

        if green_dirt_coord in env.get_ambient().get_grid():
            env.get_ambient().get_grid()[green_dirt_coord].add_dirt(dirt_appearance=green_dirt_appearance)
        else:
            env.get_ambient().get_grid()[green_dirt_coord] = VWLocation(coord=green_dirt_coord, dirt_appearance=green_dirt_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=green_dirt_coord, grid_size=grid_size))

        if orange_dirt_coord in env.get_ambient().get_grid():
            env.get_ambient().get_grid()[orange_dirt_coord].add_dirt(dirt_appearance=orange_dirt_appearance)
        else:
            env.get_ambient().get_grid()[orange_dirt_coord] = VWLocation(coord=orange_dirt_coord, dirt_appearance=orange_dirt_appearance, wall=VWEnvironment.generate_wall_from_coordinates(coord=orange_dirt_coord, grid_size=grid_size))

        return env, grid_size

    @staticmethod
    def generate_empty_env_for_testing(custom_grid_size: bool, config: dict) -> Tuple[VWEnvironment, int]:
        '''
        Generates and returns an empty `VWEnvironment` for testing purposes, given `config`.

        If `custom_grid_size` is `True`, the grid size will be randomly generated between `config["min_environment_dim"]` and `config["max_environment_dim"]` (both inclusive).
        '''
        default_grid_size: int = config["initial_environment_dim"]
        min_grid_size: int = config["min_environment_dim"]
        max_grid_size: int = config["max_environment_dim"]

        if custom_grid_size:
            grid_size: int = randint(min_grid_size, max_grid_size)
            return VWEnvironment.generate_empty_env(config=config, forced_line_dim=grid_size), grid_size
        else:
            grid_size: int = default_grid_size
            return VWEnvironment.generate_empty_env(config=config), grid_size

    @staticmethod
    def generate_mutually_exclusive_coordinates_for_testing(amount: int, grid_size: int) -> List[VWCoord]:
        '''
        Generates and returns a list of `amount` mutually exclusive `VWCoord` for testing purposes, all compatible with `grid_size`.
        '''
        assert amount > 1

        coords: List[VWCoord] = [VWCoord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1))]

        for _ in range(amount - 1):
            tmp: VWCoord = VWCoord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1))

            while tmp in coords:
                tmp = VWCoord(x=randint(0, grid_size - 1), y=randint(0, grid_size - 1))

            coords.append(tmp)

        return coords
