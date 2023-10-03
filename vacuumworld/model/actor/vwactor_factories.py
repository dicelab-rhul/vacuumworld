from typing import Union, Any

from .mind.surrogate.vwactor_mind_surrogate import VWActorMindSurrogate
from .mind.surrogate.vwuser_mind_surrogate import VWUserMindSurrogate
from .mind.vwactor_mind import VWMind
from .mind.vwuser_mind import VWUserMind
from .vwagent import VWCleaningAgent
from .vwuser import VWUser
from ...common.vwuser_difficulty import VWUserDifficulty
from .appearance.vwactor_appearance import VWActorAppearance
from ...common.vwcolour import VWColour
from ...common.vworientation import VWOrientation


class VWCleaningAgentsFactory():
    '''
    This class is a factory for `VWCleaningAgent` objects.
    '''
    @staticmethod
    def create_cleaning_agent(colour: VWColour, orientation: VWOrientation, mind_surrogate: VWActorMindSurrogate) -> tuple[VWCleaningAgent, VWActorAppearance]:
        '''
        Creates a `VWCleaningAgent` with the specified `VWColour`, `VWOrientation` and `VWActorMindSurrogate`, and returns it as a `tuple[VWCleaningAgent, VWActorAppearance]` consisting of a `VWCleaningAgent` and its `VWActorAppearance`.
        '''
        try:
            assert VWColour != VWColour.user
            assert isinstance(mind_surrogate, VWActorMindSurrogate) and not isinstance(mind_surrogate, VWUserMindSurrogate)

            agent: VWCleaningAgent = VWCleaningAgent(mind=VWMind(surrogate=mind_surrogate))
            agent_appearance: VWActorAppearance = VWActorAppearance(actor_id=agent.get_id(), progressive_id=agent.get_progressive_id(), colour=colour, orientation=orientation)

            return agent, agent_appearance
        except AssertionError as e:
            raise e
        except Exception:
            raise IOError("Error while constructing the cleaning agent.")

    @staticmethod
    def create_cleaning_agent_from_json_data(data: dict[str, str]) -> tuple[VWCleaningAgent, VWActorAppearance]:
        '''
        Creates a `VWCleaningAgent` from JSON `data`, and returns it as a `tuple[VWCleaningAgent, VWActorAppearance]` consisting of a `VWCleaningAgent` and its `VWActorAppearance`.
        '''
        try:
            assert isinstance(data, dict) and "colour" in data and "orientation" in data and "surrogate_mind_file" in data

            agent_mind_surrogate: VWActorMindSurrogate = VWActorMindSurrogate.load_from_file(surrogate_mind_file=data["surrogate_mind_file"], surrogate_mind_class_name=data["surrogate_mind_class_name"])

            assert isinstance(agent_mind_surrogate, VWActorMindSurrogate) and not isinstance(agent_mind_surrogate, VWUserMindSurrogate)

            colour: VWColour = VWColour(data["colour"])
            orientation: VWOrientation = VWOrientation(data["orientation"])

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
    def create_user(difficulty_level: VWUserDifficulty, orientation: VWOrientation) -> tuple[VWUser, VWActorAppearance]:
        try:
            user: VWUser = VWUser(mind=VWUserMind(surrogate=VWUserMindSurrogate(difficulty_level=difficulty_level)))
            user_appearance: VWActorAppearance = VWActorAppearance(actor_id=user.get_id(), progressive_id=user.get_progressive_id(), colour=VWColour.user, orientation=orientation)

            return user, user_appearance
        except AssertionError as e:
            raise e
        except Exception:
            raise IOError("Error while constructing the user.")

    @staticmethod
    def create_user_from_json_data(data: dict[str, str], difficulty_level: VWUserDifficulty=VWUserDifficulty.easy) -> tuple[VWUser, VWActorAppearance]:
        '''
        Creates a `VWUser` from JSON `data` and `difficulty_level`, and returns it as a `tuple[VWUser, VWActorAppearance]` consisting of a `VWUser` and its `VWActorAppearance`.
        '''
        try:
            assert isinstance(data, dict) and "colour" in data and "orientation" in data

            colour: VWColour = VWColour(data["colour"])

            assert colour == VWColour.user

            orientation: VWOrientation = VWOrientation(data["orientation"])

            # We set the user difficulty to easy by default.
            return VWUsersFactory.create_user(difficulty_level=difficulty_level, orientation=orientation)
        except AssertionError as e:
            raise e
        except Exception:
            raise IOError("Could not parse a user from the JSON data.")

    @staticmethod
    def create_easy_user_from_json_data(data: dict[str, Any]) -> tuple[VWUser, VWActorAppearance]:
        '''
        Creates a `VWUser` whose `VWUserDifficulty` is `VWUserDifficulty.easy` from JSON `data`, and returns it as a `tuple[VWUser, VWActorAppearance]` consisting of a `VWUser` and its `VWActorAppearance`.
        '''
        return VWUsersFactory.create_user_from_json_data(data=data, difficulty_level=VWUserDifficulty.easy)

    @staticmethod
    def create_hard_user_from_json_data(data: dict[str, Any]) -> tuple[VWUser, VWActorAppearance]:
        '''
        Creates a `VWUser` whose `VWUserDifficulty` is `VWUserDifficulty.hard` from JSON `data`, and returns it as a `tuple[VWUser, VWActorAppearance]` consisting of a `VWUser` and its `VWActorAppearance`.
        '''
        return VWUsersFactory.create_user_from_json_data(data=data, difficulty_level=VWUserDifficulty.hard)


class VWActorsFactory():
    '''
    This class is a factory for `VWActor` objects.
    '''
    @staticmethod
    def create_actor(colour: VWColour, orientation: VWOrientation, mind_surrogate: Union[VWActorMindSurrogate, VWUserMindSurrogate]) -> Union[tuple[VWCleaningAgent, VWActorAppearance], tuple[VWUser, VWActorAppearance]]:
        '''
        Creates a `VWActor` with the specified `VWColour`, `VWOrientation` and `VWActorMindSurrogate` (or `VWUserMindSurrogate`), and returns it as a `Union[tuple[VWCleaningAgent, VWActorAppearance], tuple[VWUser, VWActorAppearance]]`,
        which is a `VWCleaningAgent` or `VWUser` together with its `VWActorAppearance` or `VWActorAppearance`.
        '''
        assert isinstance(colour, VWColour)

        if colour == VWColour.user:
            assert isinstance(mind_surrogate, VWUserMindSurrogate)

            difficulty_level: VWUserDifficulty = mind_surrogate.get_difficulty_level()

            return VWUsersFactory.create_user(difficulty_level=difficulty_level, orientation=orientation)
        else:
            assert isinstance(mind_surrogate, VWActorMindSurrogate) and not isinstance(mind_surrogate, VWUserMindSurrogate)

            return VWCleaningAgentsFactory.create_cleaning_agent(colour=colour, orientation=orientation, mind_surrogate=mind_surrogate)
