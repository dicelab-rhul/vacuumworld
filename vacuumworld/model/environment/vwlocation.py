from __future__ import annotations
from typing import cast, Dict

from pystarworldsturbo.environment.location_appearance import LocationAppearance

from ...common.coordinates import Coord
from ...common.colour import Colour
from ...common.orientation import Orientation
from ..dirt.dirt_appearance import VWDirtAppearance
from ..actor.vwactor_appearance import VWActorAppearance



class VWLocation(LocationAppearance):        
    def __init__(self, coord: Coord, actor_appearance: VWActorAppearance, dirt_appearance: VWDirtAppearance, wall: Dict[Orientation, bool]) -> None:
        assert coord is not None
        
        self.__coord: Coord = coord
        self.__actor_appearance: VWActorAppearance = actor_appearance
        self.__dirt_appearance: VWDirtAppearance = dirt_appearance
        self.__wall: Dict[Orientation, bool] = wall

        self.__update_quick_api()

    # For back compatibility with 4.1.8.
    def __update_quick_api(self) -> None:
        self.coordinate: Coord = self.__coord
        self.actor: VWActorAppearance = self.__actor_appearance
        self.dirt: VWDirtAppearance = self.__dirt_appearance
        self.wall_on_north: bool = self.__wall[Orientation.north]
        self.wall_on_south: bool = self.__wall[Orientation.south]
        self.wall_on_west: bool = self.__wall[Orientation.west]
        self.wall_on_east: bool = self.__wall[Orientation.east]

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
        
        self.__update_quick_api()

    def add_actor(self, actor_appearance: VWActorAppearance) -> None:
        assert self.__actor_appearance is None
        
        self.__actor_appearance = actor_appearance
        
        self.__update_quick_api()

    def has_actor(self) -> bool:
        return self.__actor_appearance is not None

    def has_cleaning_agent(self) -> bool:
        return self.__actor_appearance is not None and self.__actor_appearance.get_colour() in [Colour.white, Colour.green, Colour.orange]

    def has_user(self) -> bool:
        return self.__actor_appearance is not None and self.__actor_appearance.get_colour() == Colour.user

    def is_empty(self) -> bool:
        return not self.has_actor() and not self.has_dirt()

    def get_dirt_appearance(self) -> VWDirtAppearance:
        return self.__dirt_appearance

    def remove_dirt(self) -> None:
        assert self.__dirt_appearance is not None

        self.__dirt_appearance = None
        
        self.__update_quick_api()

    def add_dirt(self, dirt_appearance: VWDirtAppearance) -> None:
        assert self.__dirt_appearance is None
        
        self.__dirt_appearance = dirt_appearance
        
        self.__update_quick_api()

    def has_dirt(self) -> bool:
        return self.__dirt_appearance is not None
    
    def get_wall_info(self) -> Dict[Orientation, bool]:
        return self.__wall
    
    def has_wall_on_north(self) -> bool:
        return self.__wall[Orientation.north]
    
    def has_wall_on_south(self) -> bool:
        return self.__wall[Orientation.south]
    
    def has_wall_on_west(self) -> bool:
        return self.__wall[Orientation.west]
    
    def has_wall_on_east(self) -> bool:
        return self.__wall[Orientation.east]
    
    def has_wall_on(self, orientation: Orientation) -> bool:
        return self.__wall[orientation]

    def deep_copy(self) -> VWLocation:
        if not self.__actor_appearance and not self.__dirt_appearance:
            return VWLocation(coord=self.__coord, actor_appearance=None, dirt_appearance=None, wall=self.__wall)
        elif self.__actor_appearance and not self.__dirt_appearance:
            return VWLocation(coord=self.__coord, actor_appearance=self.__actor_appearance.deep_copy(), dirt_appearance=None, wall=self.__wall)
        elif not  self.__actor_appearance and self.__dirt_appearance:
            return VWLocation(coord=self.__coord, actor_appearance=None, dirt_appearance=self.__dirt_appearance.deep_copy(), wall=self.__wall)
        else:
            return VWLocation(coord=self.__coord, actor_appearance=self.__actor_appearance.deep_copy(), dirt_appearance=self.__dirt_appearance.deep_copy(), wall=self.__wall)

    def to_json(self) -> Dict[str, Dict[str, str | int]]:
        location: Dict[str, Dict[str, str | int]] = {
            "coords": self.__coord.to_json(),
            "wall": {
                str(Orientation.north): self.has_wall_on_north(),
                str(Orientation.south): self.has_wall_on_south(),
                str(Orientation.west): self.has_wall_on_west(),
                str(Orientation.east): self.has_wall_on_east()
            }
        }

        if self.has_actor():
            location["actor"] = self.__actor_appearance.to_json()

        if self.has_dirt():
            location["dirt"] = self.__dirt_appearance.to_json()

        return location

    def __str__(self) -> str:
        return "(actor: {}, dirt: {}, wall: {})".format(str(self.__actor_appearance), str(self.__dirt_appearance), str(self.__wall))

    def __eq__(self, o: object) -> bool:
        if not o or type(o) != VWLocation:
            return False
        else:
            o = cast(typ=VWLocation, val=o)

            return self.__coord == o.get_coord() and self.__actor_appearance == o.get_actor_appearance() and self.__dirt_appearance == o.get_dirt_appearance() and self.__wall == o.get_wall_info()

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
            
        if self.has_wall_on_north():
            result = prime * result + self.__wall[Orientation.north].__hash__()
        
        if self.has_wall_on_south():
            result = prime * result + self.__wall[Orientation.south].__hash__()
        
        if self.has_wall_on_west():
            result = prime * result + self.__wall[Orientation.west].__hash__()
        
        if self.has_wall_on_east():
            result = prime * result + self.__wall[Orientation.east].__hash__()

        return result

    def visualise(self) -> str:
        s: str = "#######\n#{}#\n".format(str(self.__coord).replace(" ", ""))

        if self.is_empty():
            s += "#     #\n"
        elif not self.has_actor() and self.has_dirt():
            s += "#  " + str(self.__dirt_appearance.get_colour())[0] + "  #\n"
        elif not self.has_dirt():
            s += "#  " + str(self.__actor_appearance.get_colour())[0].upper() + "  #\n"
        else:
            s += "# " + str(self.__actor_appearance.get_colour())[0].upper() + "+" + str(self.__dirt_appearance.get_colour())[0] + " #\n"

        return s + "#######"
