from enum import Enum



class ActionOutcome(Enum):
    impossible = "impossible"
    success = "success"
    failure = "failure"

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)
