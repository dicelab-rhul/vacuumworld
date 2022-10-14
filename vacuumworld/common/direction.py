from enum import Enum



class Direction(Enum):
    left = "left"
    right = "right"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)
