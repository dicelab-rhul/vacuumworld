from __future__ import annotations

from pystarworldsturbo.environment.location_appearance import LocationAppearance

from ...common.coordinates import Coord
from ...common.colour import Colour
from ..dirt.dirt_appearance import VWDirtAppearance
from ..actor.vwactor_appearance import VWActorAppearance



class VWLocation(LocationAppearance):
    def __init__(self, coord: Coord, actor_appearance: VWActorAppearance, dirt_appearance: VWDirtAppearance) -> None:
        assert coord is not None
        
        self.__coord: Coord = coord
        self.__actor_appearance: VWActorAppearance = actor_appearance
        self.__dirt_appearance: VWDirtAppearance = dirt_appearance

        self.__create_quick_api()

    def __create_quick_api(self) -> None:
        self.coordinate: Coord = self.__coord
        self.actor: VWActorAppearance = self.__actor_appearance
        self.dirt: VWDirtAppearance = self.__dirt_appearance

        if self.has_cleaning_agent():
            self.agent: VWActorAppearance = self.__actor_appearance
            self.user: VWActorAppearance = None
        elif self.has_user():
            self.agent: VWActorAppearance = None
            self.user: VWActorAppearance = self.__actor_appearance
        else:
            self.agent: VWActorAppearance = None
            self.user: VWActorAppearance = None

    def get_coord(self) -> Coord:
        return self.__coord

    def get_actor_appearance(self) -> VWActorAppearance:
        return self.__actor_appearance

    def remove_actor(self) -> None:
        assert self.__actor_appearance is not None

        self.__actor_appearance = None

    def add_actor(self, actor_appearance: VWActorAppearance) -> None:
        assert self.__actor_appearance is None
        
        self.__actor_appearance = actor_appearance

    def has_actor(self) -> bool:
        return self.__actor_appearance is not None

    def has_cleaning_agent(self) -> bool:
        return self.__actor_appearance is not None and self.__actor_appearance.get_colour() in [Colour.white, Colour.green, Colour.orange]

    def has_user(self) -> bool:
        return self.__actor_appearance is not None and self.__actor_appearance.get_colour() == Colour.user

    def get_dirt_appearance(self) -> VWDirtAppearance:
        return self.__dirt_appearance

    def remove_dirt(self) -> None:
        assert self.__dirt_appearance is not None

        self.__dirt_appearance = None

    def add_dirt(self, dirt_appearance: VWDirtAppearance) -> None:
        assert self.__dirt_appearance is None
        
        self.__dirt_appearance = dirt_appearance

    def has_dirt(self) -> bool:
        return self.__dirt_appearance is not None

    def deep_copy(self) -> VWLocation:
        if not self.__actor_appearance and not self.__dirt_appearance:
            return VWLocation(coord=self.__coord, actor_appearance=None, dirt_appearance=None)
        elif self.__actor_appearance and not self.__dirt_appearance:
            return VWLocation(coord=self.__coord, actor_appearance=self.__actor_appearance.deep_copy(), dirt_appearance=None)
        elif not  self.__actor_appearance and self.__dirt_appearance:
            return VWLocation(coord=self.__coord, actor_appearance=None, dirt_appearance=self.__dirt_appearance.deep_copy())
        else:
            return VWLocation(coord=self.__coord, actor_appearance=self.__actor_appearance.deep_copy(), dirt_appearance=self.__dirt_appearance.deep_copy())

    def __str__(self) -> str:
        return "(actor: {}, dirt: {})".format(str(self.__actor_appearance), str(self.__dirt_appearance))

    def __eq__(self, o: object) -> bool:
        if not o or type(o) != VWLocation:
            return False
        else:
            return self.__coord == o.get_coord() and self.__actor_appearance == o.get_actor_appearance() and self.__dirt_appearance == o.get_dirt_appearance()

    def __hash__(self) -> int:
        prime: int = 31
        result: int = 1

        result = prime * result + self.__coord.__hash__()

        if self.__actor_appearance:
            result = prime * result + self.__actor_appearance.__hash__()
        else:
            result = prime * result + 0

        if self.__dirt_appearance:
            result = prime * result + self.__dirt_appearance.__hash__()
        else:
            result = prime * result + 0

        return result
