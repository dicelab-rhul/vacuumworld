from enum import Enum


class VWColour(Enum):
    '''
    This `Enum` specifies the colours for different kinds of `VWActor` and `VWDirt`.

    * `green` applies to each green `VWCleaningAgent` and to each green `VWDirt`.

    * `orange` applies to each orange `VWCleaningAgent` and to each orange `VWDirt`.

    * `white` applies to each white `VWCleaningAgent`.

    * `user` applies to each `VWUser`.
    '''
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
        Returns a `str` representation of this `VWColour` with the appropriate indefinite article in front of it, and a space between the two.
        '''
        if self == VWColour.orange:
            return "an {}".format(self)
        else:
            return "a {}".format(self)
