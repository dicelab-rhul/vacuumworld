from os import devnull
from typing import Any

from ..model.actor.actor_mind_surrogate import ActorMindSurrogate



def ignore(obj: Any) -> None:
    if not obj:
        return

    with open(devnull, "w") as f:
        f.write(str(obj))
        f.flush()


def load_surrogate_mind_from_file(surrogate_mind_file: str) -> ActorMindSurrogate:
    pass #TODO:
