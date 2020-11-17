from typing import Tuple, Union

from .actor_mind_surrogate import ActorMindSurrogate
from .user_mind_surrogate import UserMindSurrogate
from .vwactormind import VWMind
from .vwagent import VWCleaningAgent
from .vwuser import VWUser
from .user_difficulty import UserDifficulty
from .vwactor_appearance import VWActorAppearance

from ...common.colour import Colour
from ...common.orientation import Orientation
from ...utils.vwutils import load_surrogate_mind_from_file



class VWCleaningAgentsFactory():
    @staticmethod
    def create_cleaning_agent(colour: Colour, orientation: Orientation, mind_surrogate: ActorMindSurrogate) -> Tuple[VWCleaningAgent, VWActorAppearance]:
        assert Colour != Colour.user

        agent: VWCleaningAgent = VWCleaningAgent(mind=VWMind(surrogate=mind_surrogate))
        agent_appearance: VWActorAppearance = VWActorAppearance(actor_id=agent.get_id(), progressive_id=agent.get_progressive_id(), colour=colour, orientation=orientation)

        return agent, agent_appearance

    @staticmethod
    def create_cleaning_agent_from_json_data(data: dict) -> Tuple[VWCleaningAgent, VWActorAppearance]:
        assert type(data) == dict and "colour" in data and "orientation" in data and "surrogate_mind_file" in data

        agent_mind_surrogate: ActorMindSurrogate = load_surrogate_mind_from_file(surrogate_mind_file=data["surrogate_mind_file"], surrogate_mind_class_name=data["surrogate_mind_class_name"])

        assert isinstance(agent_mind_surrogate, ActorMindSurrogate) and not isinstance(agent_mind_surrogate, UserMindSurrogate)

        colour: Colour = Colour(data["colour"])
        orientation: Orientation = Orientation(data["orientation"])

        return VWCleaningAgentsFactory.create_cleaning_agent(colour=colour, orientation=orientation, mind_surrogate=agent_mind_surrogate)


class VWUsersFactory():
    @staticmethod
    def create_user(difficulty_level: UserDifficulty, orientation: Orientation) -> Tuple[VWUser, VWActorAppearance]:
        user: VWUser = VWUser(mind=VWMind(surrogate=UserMindSurrogate(difficulty_level=difficulty_level)))
        user_appearance: VWActorAppearance = VWActorAppearance(actor_id=user.get_id(), progressive_id=user.get_progressive_id(), colour=Colour.user, orientation=orientation)

        return user, user_appearance

    @staticmethod
    def create_user_from_json_data(data: dict) -> Tuple[VWUser, VWActorAppearance]:
        assert type(data) == dict and "colour" in data and "orientation" in data and "surrogate_mind_file" in data

        colour: Colour = Colour(data["colour"])

        assert colour == Colour.user

        orientation: Orientation = Orientation(data["orientation"])

        # We set the user difficulty to easy by default.
        return VWUsersFactory.create_user(difficulty_level=UserDifficulty.easy, orientation=orientation)


class VWActorsFactory():
    @staticmethod
    def create_actor(colour: Colour, orientation: Orientation, mind_surrogate: ActorMindSurrogate) -> Union[Tuple[VWCleaningAgent, VWActorAppearance], Tuple[VWUser, VWActorAppearance]]:
        assert type(colour) == Colour

        if colour == Colour.user:
            assert type(mind_surrogate) == UserMindSurrogate

            difficulty_level: UserDifficulty = mind_surrogate.get_difficulty_level()
            
            return VWUsersFactory.create_user(difficulty_level=difficulty_level, orientation=orientation)
        else:
            return VWCleaningAgentsFactory.create_cleaning_agent(colour=colour, orientation=orientation, mind_surrogate=mind_surrogate)
