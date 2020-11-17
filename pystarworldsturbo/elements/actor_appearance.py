from ..common.identifiable import Identifiable


class ActorAppearance(Identifiable):
    def __init__(self, actor_id: str, progressive_id: str) -> None:
        super(ActorAppearance, self).__init__(identifiable_id=actor_id, progressive_id=progressive_id)
