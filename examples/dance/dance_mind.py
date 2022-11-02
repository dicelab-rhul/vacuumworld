from typing import Iterable

from pystarworldsturbo.utils.utils import ignore
from pystarworldsturbo.common.message import BccMessage

from vacuumworld.model.actor.actor_mind_surrogate import ActorMindSurrogate
from vacuumworld.model.environment.vwlocation import VWLocation
from vacuumworld.common.observation import Observation
from vacuumworld.common.colour import Colour
from vacuumworld.common.coordinates import Coord
from vacuumworld.common.orientation import Orientation


class DanceMind(ActorMindSurrogate):
    """
    This is a parent mind class which implements several basic functions.
    Most importantly keeping track of:
        - positional information; grid positions and orientation
        - agent properties; id and colour
        - the observations of the agent
        - a tick/counter value for simple time keeping/synchronisation
    """
    def __init__(self):
        super(DanceMind, self).__init__()

        self.__coord: Coord = None
        self.__id: str = ""
        self.__ori: Orientation = None
        self.__col: Colour = None
        self.__obs: Observation = None
        self.__tick: int = 0

    def get_coord(self) -> Coord:
        return self.__coord

    def get_colour(self) -> Colour:
        return self.__col

    def get_tick(self) -> int:
        return self.__tick

    def get_id(self) -> str:
        return self.__id

    def get_obs(self) -> Observation:
        return self.__obs

    def get_orientation(self) -> Orientation:
        return self.__ori

    def revise(self, observation: Observation, messages: Iterable[BccMessage]):
        """
        This is the base revise function for updating the agent state.

        It calls a sub_revise function which can be overridden by child minds. This way they
        can add their own behaviours without overwriting the base behaviours from this mind.
        """
        self.__tick += 1

        self.__revise_me(centre_ob=observation.get_center())

        self.__obs = observation

        self.sub_revise(observation=observation, messages=messages)

    def sub_revise(self, observation: Observation, messages: Iterable[BccMessage]):
        ignore(observation)

        for message in messages:
            ignore(message)

        print("This is the default sub revise. Override this in child minds.")

    def __revise_me(self, centre_ob: VWLocation):
        """
        Updates any attributes relating to the agent state.
        Some attributes need only be updated once, as they are static (id and colour).
        """

        assert centre_ob

        self.__coord = centre_ob.get_coord()
        self.__ori = centre_ob.get_actor_appearance().get_orientation()
        self.__id = centre_ob.get_actor_appearance().get_id() if not self.__id else self.__id
        self.__col = centre_ob.get_actor_appearance().get_colour() if not self.__col else self.__col
