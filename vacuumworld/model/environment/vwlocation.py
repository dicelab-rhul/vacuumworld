from vacuumworld.model.dirt.dirt_appearance import VWDirtAppearance
from vacuumworld.model.actor.vwactor_appearance import VWActorAppearance
from pystarworldsturbo.environment.location_appearance import LocationAppearance



class VWLocation(LocationAppearance):
    def __init__(self, actor_appearance: VWActorAppearance, dirt_appearance: VWDirtAppearance) -> None:
        self.__actor_appearance: VWActorAppearance = actor_appearance
        self.__dirt_appearance: VWDirtAppearance = dirt_appearance

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

    def deep_copy(self) -> "VWLocation":
        if not self.__actor_appearance and not self.__dirt_appearance:
            return VWLocation()
        elif self.__actor_appearance and not self.__dirt_appearance:
            return VWLocation(actor_appearance=self.__actor_appearance.deep_copy(), dirt_appearance=None)
        elif not  self.__actor_appearance and self.__dirt_appearance:
            return VWLocation(actor_appearance=None, dirt_appearance=self.__dirt_appearance.deep_copy())
        else:
            return VWLocation(actor_appearance=self.__actor_appearance.deep_copy(), dirt_appearance=self.__dirt_appearance.deep_copy())
