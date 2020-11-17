from os import devnull
from typing import Any



def ignore(obj: Any) -> None:
    if not obj:
        return

    with open(devnull, "w") as f:
        f.write(str(obj))
        f.flush()
