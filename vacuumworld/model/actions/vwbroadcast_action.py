from pystarworldsturbo.common.content_type import MessageContentType

from .vwactions import VWCommunicativeAction


class VWBroadcastAction(VWCommunicativeAction):
    '''
    This class is a `VWCommunicativeAction` that broadcasts a message to each `VWActor` in the `VWEnvironment`.
    '''
    def __init__(self, message: MessageContentType, sender_id: str) -> None:
        super(VWBroadcastAction, self).__init__(message=message, recipients=[], sender_id=sender_id)
