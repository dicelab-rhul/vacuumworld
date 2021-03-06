from typing import Iterable, Type, Union, List

from pystarworldsturbo.common.action import Action
from pystarworldsturbo.common.message import Message

from ...common.exceptions import VWMalformedActionException



class VWAction(Action):
    def __init__(self) -> None:
        super(VWAction, self).__init__()

class VWPhysicalAction(VWAction):
    def __init__(self) -> None:
        super(VWPhysicalAction, self).__init__()


class VWCommunicativeAction(VWAction):
    ALLOWED_MESSAGE_TYPES: List[Type] = [int, float, str, list, tuple, dict]

    def __init__(self, message: Union[int, float, str, list, tuple, dict], recipients: Iterable, sender_id: str) -> None:
        super(VWCommunicativeAction, self).__init__()

        VWCommunicativeAction.__validate_message(message=message)
        VWCommunicativeAction.__validate_recipients(recipients=recipients)

        self.__message: Message = Message(content=message, recipient_ids=recipients, sender_id=sender_id)

    @staticmethod
    def __validate_message(message: Union[int, float, str, list, tuple, dict]) -> None:
        if not message:
            raise VWMalformedActionException("A message cannot be NoneType or empty.")
        elif type(message) not in VWCommunicativeAction.ALLOWED_MESSAGE_TYPES:
            raise VWMalformedActionException("Invalid message type: {} (allowed: {}).".format(type(message), VWCommunicativeAction.ALLOWED_MESSAGE_TYPES))

    @staticmethod
    def __validate_recipients(recipients: Iterable) -> None:
        if not isinstance(recipients, Iterable):
            raise VWMalformedActionException("`recipients` must be iterable.")

    def get_message(self) -> Message:
        return self.__message
