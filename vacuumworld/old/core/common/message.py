from typing import Iterable, NamedTuple, Type, Union



class Message(NamedTuple):
    '''
        A datastructure representing a message (perception) of the agent. 
        The content of a message is limited to 100 characters and will be greedily trimmed to fit. 
        To prevent loss of data in the content you should always check the length before sending, or 
        at least have some consideration for the message length in your implementing of an agent mind. 
        ``vwc.size(message)`` can be used to properly check the length of a message.
        Attributes:
            * ``sender (str)``: The name of the sender of the message.
            * ``content (str, list, tuple, int, float, bool)``: The content of the message.
    '''
    sender : str
    content : Union[str, list, tuple, int, float, bool]

    @staticmethod
    def _size(content: Union[str, list, tuple, int, float, bool]) -> int:
        if content is None:
            return 0
        
        assert type(content) in [str, list, tuple, int, float, bool]

        if isinstance(content, Iterable):
            return sum(lambda elm: Message._size(elm), content)
        else:
            return len(str(content))

    def size(self) -> int:
        '''
            Computes the size of a message.
            
            Argument:
                * ``message (str, list, tuple, int, float, bool)``: to check the size of.
            
            Returns:
                ``(int)``: The size of the message.
                
            Example
            --------
            ::
                
                >>> size('hello')
                5
                >>> size(('size', 9))
                8
                >>> size(['hello', ('size', 9)])
                16
                
        '''

        return Message._size(self.content)

message: Type = Message
