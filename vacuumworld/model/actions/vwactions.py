from typing import Iterable, List

from pystarworldsturbo.common.action import Action
from pystarworldsturbo.common.message import Message
from pystarworldsturbo.common.content_type import MessageContentType, MessageContentBaseType

from .vweffort import VWActionEffort

from ...common.vwexceptions import VWMalformedActionException
from ...common.vwvalidator import VWValidator


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
        if type(self).__name__ in VWActionEffort.EFFORTS:
            return VWActionEffort.EFFORTS[type(self).__name__]
        else:
            return VWActionEffort.DEFAULT_EFFORT_FOR_OTHER_ACTIONS


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
    SENDER_ID_SPOOFING_ALLOWED: bool = False

    def __init__(self, message: MessageContentType, recipients: Iterable[str], sender_id: str) -> None:
        super(VWCommunicativeAction, self).__init__()

        VWCommunicativeAction.__validate_message(message=message)
        VWCommunicativeAction.__validate_recipients(recipients=recipients)

        self.__message: Message = Message(content=message, recipient_ids=[recipient for recipient in recipients], sender_id=sender_id)

    @staticmethod
    def __validate_message(message: MessageContentType) -> None:
        VWValidator.validate_not_none(obj=message)

        if not isinstance(message, MessageContentBaseType):
            raise VWMalformedActionException(f"Invalid message type: {type(message)} (allowed: {MessageContentType}).")

    @staticmethod
    def __validate_recipients(recipients: Iterable[str]) -> None:
        if not VWValidator.does_type_match(t=Iterable, obj=recipients):
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
