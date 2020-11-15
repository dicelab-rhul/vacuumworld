from uuid import uuid4



global_counter: int = 1



class Identifiable():
    def __init__(self, identifiable_id: str=None, progressive_id: str=None) -> None:
        if not identifiable_id or not progressive_id:
            identifiable_id = str(uuid4())
            progressive_id = Identifiable.new_progressive_id()

        self.__id: str = identifiable_id
        self.__progressive_id: str = progressive_id

    def get_id(self) -> str:
        return self.__id

    def get_progressive_id(self) -> str:
        return self.__progressive_id

    @staticmethod
    def new_progressive_id() -> str:
        global global_counter

        progressive_id: str = str(global_counter)
        global_counter += 1

        return progressive_id
