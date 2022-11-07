from typing import Tuple, Union, Dict

from .actor_mind_surrogate import ActorMindSurrogate
from .user_mind_surrogate import UserMindSurrogate
from .vwactormind import VWMind
from .vwusermind import VWUserMind
from .vwagent import VWCleaningAgent
from .vwuser import VWUser
from .user_difficulty import UserDifficulty
from .vwactor_appearance import VWActorAppearance
from ...common.colour import Colour
from ...common.orientation import Orientation


class VWCleaningAgentsFactory():
    '''
    This class is a factory for `VWCleaningAgent` objects.
    '''
    @staticmethod
    def create_cleaning_agent(colour: Colour, orientation: Orientation, mind_surrogate: ActorMindSurrogate) -> Tuple[VWCleaningAgent, VWActorAppearance]:
        '''
        Creates a `VWCleaningAgent` with the specified `Colour`, `Orientation` and `ActorMindSurrogate`, and returns it as a `Tuple[VWCleaningAgent, VWActorAppearance]` consisting of a `VWCleaningAgent` and its `VWActorAppearance`.
        '''
        try:
            assert Colour != Colour.user
            assert isinstance(mind_surrogate, ActorMindSurrogate) and not isinstance(mind_surrogate, UserMindSurrogate)

            agent: VWCleaningAgent = VWCleaningAgent(mind=VWMind(surrogate=mind_surrogate))
            agent_appearance: VWActorAppearance = VWActorAppearance(actor_id=agent.get_id(), progressive_id=agent.get_progressive_id(), colour=colour, orientation=orientation)

            return agent, agent_appearance
        except AssertionError as e:
            raise e
        except Exception:
            raise IOError("Error while constructing the cleaning agent.")

    @staticmethod
    def create_cleaning_agent_from_json_data(data: Dict[str, str]) -> Tuple[VWCleaningAgent, VWActorAppearance]:
        '''
        Creates a `VWCleaningAgent` from JSON `data`, and returns it as a `Tuple[VWCleaningAgent, VWActorAppearance]` consisting of a `VWCleaningAgent` and its `VWActorAppearance`.
        '''
        try:
            assert type(data) == dict and "colour" in data and "orientation" in data and "surrogate_mind_file" in data

            agent_mind_surrogate: ActorMindSurrogate = ActorMindSurrogate.load_from_file(surrogate_mind_file=data["surrogate_mind_file"], surrogate_mind_class_name=data["surrogate_mind_class_name"])

            assert isinstance(agent_mind_surrogate, ActorMindSurrogate) and not isinstance(agent_mind_surrogate, UserMindSurrogate)

            colour: Colour = Colour(data["colour"])
            orientation: Orientation = Orientation(data["orientation"])

            return VWCleaningAgentsFactory.create_cleaning_agent(colour=colour, orientation=orientation, mind_surrogate=agent_mind_surrogate)
        except AssertionError as e:
            raise e
        except Exception:
            raise IOError("Could not parse a cleaning agent from the JSON data.")


class VWUsersFactory():
    '''
    This class is a factory for `VWUser` objects.
    '''
    @staticmethod
    def create_user(difficulty_level: UserDifficulty, orientation: Orientation) -> Tuple[VWUser, VWActorAppearance]:
        try:
            user: VWUser = VWUser(mind=VWUserMind(surrogate=UserMindSurrogate(difficulty_level=difficulty_level)))
            user_appearance: VWActorAppearance = VWActorAppearance(actor_id=user.get_id(), progressive_id=user.get_progressive_id(), colour=Colour.user, orientation=orientation)

            return user, user_appearance
        except AssertionError as e:
            raise e
        except Exception:
            raise IOError("Error while constructing the user.")

    @staticmethod
    def create_user_from_json_data(data: Dict[str, str], difficulty_level: UserDifficulty=UserDifficulty.easy) -> Tuple[VWUser, VWActorAppearance]:
        '''
        Creates a `VWUser` from JSON `data` and `difficulty_level`, and returns it as a `Tuple[VWUser, VWActorAppearance]` consisting of a `VWUser` and its `VWActorAppearance`.
        '''
        try:
            assert type(data) == dict and "colour" in data and "orientation" in data

            colour: Colour = Colour(data["colour"])

            assert colour == Colour.user

            orientation: Orientation = Orientation(data["orientation"])

            # We set the user difficulty to easy by default.
            return VWUsersFactory.create_user(difficulty_level=difficulty_level, orientation=orientation)
        except AssertionError as e:
            raise e
        except Exception:
            raise IOError("Could not parse a user from the JSON data.")

    @staticmethod
    def create_easy_user_from_json_data(data: dict) -> Tuple[VWUser, VWActorAppearance]:
        '''
        Creates a `VWUser` whose `UserDifficulty` is `UserDifficulty.easy` from JSON `data`, and returns it as a `Tuple[VWUser, VWActorAppearance]` consisting of a `VWUser` and its `VWActorAppearance`.
        '''
        return VWUsersFactory.create_user_from_json_data(data=data, difficulty_level=UserDifficulty.easy)

    @staticmethod
    def create_hard_user_from_json_data(data: dict) -> Tuple[VWUser, VWActorAppearance]:
        '''
        Creates a `VWUser` whose `UserDifficulty` is `UserDifficulty.hard` from JSON `data`, and returns it as a `Tuple[VWUser, VWActorAppearance]` consisting of a `VWUser` and its `VWActorAppearance`.
        '''
        return VWUsersFactory.create_user_from_json_data(data=data, difficulty_level=UserDifficulty.hard)


class VWActorsFactory():
    '''
    This class is a factory for `VWActor` objects.
    '''
    @staticmethod
    def create_actor(colour: Colour, orientation: Orientation, mind_surrogate: Union[ActorMindSurrogate, UserMindSurrogate]) -> Union[Tuple[VWCleaningAgent, VWActorAppearance], Tuple[VWUser, VWActorAppearance]]:
        '''
        Creates a `VWActor` with the specified `Colour`, `Orientation` and `ActorMindSurrogate` (or `UserMindSurrogate`), and returns it as a `Union[Tuple[VWCleaningAgent, VWActorAppearance], Tuple[VWUser, VWActorAppearance]]`,
        which is a `VWCleaningAgent` or `VWUser` together with its `VWActorAppearance` or `VWActorAppearance`.
        '''
        assert type(colour) == Colour

        if colour == Colour.user:
            assert type(mind_surrogate) == UserMindSurrogate

            difficulty_level: UserDifficulty = mind_surrogate.get_difficulty_level()

            return VWUsersFactory.create_user(difficulty_level=difficulty_level, orientation=orientation)
        else:
            assert isinstance(mind_surrogate, ActorMindSurrogate) and not isinstance(mind_surrogate, UserMindSurrogate)

            return VWCleaningAgentsFactory.create_cleaning_agent(colour=colour, orientation=orientation, mind_surrogate=mind_surrogate)
