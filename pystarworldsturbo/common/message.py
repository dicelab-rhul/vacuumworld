from typing import List, Union

from .perception import Perception



class Message(Perception):
    def __init__(self, content: Union[int, float, str, list, tuple, dict], sender_id: str, recipient_ids: List[str]=[]) -> None:
        assert type(content) in [int, float, str, list, tuple, dict]
        assert type(sender_id) == str
        assert recipient_ids is not None
        
        self.__content: Union[int, float, str, list, tuple, dict] = content
        self.__sender_id: str = sender_id
        self.__recipient_ids: List[str] = recipient_ids

    def get_content(self) -> Union[int, float, str, list, tuple, dict]:
        return self.__content

    def get_sender_id(self) -> str:
        return self.__sender_id

    def get_recipients_ids(self) -> List[str]:
        return self.__recipient_ids

    def override_recipients(self, recipient_ids: List[str]) -> None:
        self.__recipient_ids = recipient_ids


class BccMessage(Message):
    def __init__(self, content: Union[int, float, str, list, tuple, dict], sender_id: str, recipient_id: str) -> None:
        assert type(recipient_id) == str

        super(BccMessage, self).__init__(content=content, sender_id=sender_id, recipient_ids=[recipient_id])

    def __str__(self) -> str:
        return "message:(from: {}, content: {})".format(self.get_sender_id(), self.get_content())
