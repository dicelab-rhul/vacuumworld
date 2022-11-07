from typing import Iterable, Type, Union, List

from pystarworldsturbo.common.action import Action
from pystarworldsturbo.common.message import Message

from .effort import ActionEffort

from ...common.exceptions import VWMalformedActionException


class VWAction(Action):
    '''
    This class is the base class for all actions in the `VacuumWorld` universe.
    '''
    def __init__(self) -> None:
        super(VWAction, self).__init__()

    def get_effort(self) -> int:
        '''
        Returns the effort of this `VWAction` as an `int`.
        '''
        if type(self).__name__ in ActionEffort.EFFORTS:
            return ActionEffort.EFFORTS[type(self).__name__]
        else:
            return ActionEffort.DEFAULT_EFFORT_FOR_OTHER_ACTIONS


class VWPhysicalAction(VWAction):
    '''
    This class is a `VWAction` that requires the `VWActor` to do something physically in the `VWEnvironment`.
    '''
    def __init__(self) -> None:
        super(VWPhysicalAction, self).__init__()


class VWCommunicativeAction(VWAction):
    '''
    This class is a `VWAction` that requires the `VWActor` to communicate with another `VWActor` (or more) in the `VWEnvironment`.
    '''
    ALLOWED_MESSAGE_TYPES: List[Type] = [int, float, str, bytes, list, tuple, dict]
    SENDER_ID_SPOOFING_ALLOWED: bool = False

    def __init__(self, message: Union[int, float, str, bytes, list, tuple, dict], recipients: Iterable[str], sender_id: str) -> None:
        super(VWCommunicativeAction, self).__init__()

        VWCommunicativeAction.__validate_message(message=message)
        VWCommunicativeAction.__validate_recipients(recipients=recipients)

        self.__message: Message = Message(content=message, recipient_ids=[recipient for recipient in recipients], sender_id=sender_id)

    @staticmethod
    def __validate_message(message: Union[int, float, str, bytes, list, tuple, dict]) -> None:
        if not message:
            raise VWMalformedActionException("A message cannot be NoneType or empty.")
        elif type(message) not in VWCommunicativeAction.ALLOWED_MESSAGE_TYPES:
            raise VWMalformedActionException("Invalid message type: {} (allowed: {}).".format(type(message), VWCommunicativeAction.ALLOWED_MESSAGE_TYPES))

    @staticmethod
    def __validate_recipients(recipients: Iterable) -> None:
        if not isinstance(recipients, Iterable):
            raise VWMalformedActionException("`recipients` must be iterable.")

    def get_message(self) -> Message:
        '''
        Returns the `Message` of this `VWCommunicativeAction`.
        '''
        return self.__message

    def get_recipients(self) -> List[str]:
        '''
        Returns the `List[str]` of recipients of this `VWCommunicativeAction`.
        '''
        return self.__message.get_recipients_ids()
