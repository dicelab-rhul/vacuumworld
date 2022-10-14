from enum import Enum


class Colour(Enum):
    green = "green"
    orange = "orange"
    white = "white"
    user = "user"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)

    def str_with_article(self) -> str:
        if self == Colour.orange:
            return "an {}".format(self)
        else:
            return "a {}".format(self)
