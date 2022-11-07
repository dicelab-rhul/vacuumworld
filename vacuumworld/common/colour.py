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
        '''
        Returns a `str` representation of this `Colour` with the appropriate indefinite article in front of it, and a space between the two.
        '''
        if self == Colour.orange:
            return "an {}".format(self)
        else:
            return "a {}".format(self)
