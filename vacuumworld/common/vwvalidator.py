from typing import Iterable, Any, Optional, Type, cast
from pydoc import locate


class VWValidator():
    @staticmethod
    def validate_not_none(obj: Optional[Any]) -> None:
        '''
        Raises a ValueError if the given object is None.
        '''
        if obj is None:
            raise ValueError("Object cannot be None.")

    @staticmethod
    def validate_all_not_none(*objs: Optional[Any]) -> None:
        '''
        Raises a ValueError if any of the given objects are None.
        '''
        if any(obj is None for obj in objs):
            raise ValueError("One or more objects are None.")

    @staticmethod
    def validate_all_elements_not_none(iterable: Optional[Iterable[Any]]) -> None:
        '''
        Raises a ValueError if the given iterable is None, or if any of its elements are None.
        '''
        if iterable is None or any(obj is None for obj in iterable):
            raise ValueError("Either the iterable, or one or more of its elements are None.")

    @staticmethod
    def validate_type(t: Type[Any], obj: Any) -> None:
        '''
        Raises a ValueError if the given object is not of the given type.
        '''
        assert t is not None and obj is not None

        if not isinstance(obj, t):
            raise ValueError(f"Expected type {t}, got type {type(obj)}.")

    @staticmethod
    def validate_type_from_string(ts: str, obj: Any) -> None:
        '''
        Raises a ValueError if the given object is not of the given type (given as a `str`).
        '''
        assert ts is not None and obj is not None

        t: Type[Any] = cast(Type[Any], locate(ts))

        if not isinstance(obj, t):
            raise ValueError(f"Expected type {t}, got type {type(obj)}.")

    @staticmethod
    def does_type_match(t: type, obj: Any) -> bool:
        '''
        Returns True if the given object is of the given type, False otherwise.
        '''
        assert t is not None and obj is not None

        return isinstance(obj, t)

    @staticmethod
    def validate_type_for_all(t: type, *objs: Any) -> None:
        '''
        Raises a ValueError if any of the given objects are not of the given type.
        '''
        assert t is not None and isinstance(objs, Iterable)

        for obj in objs:
            if not isinstance(obj, t):
                raise ValueError(f"Expected type {t}, got type {type(obj)}.")

    @staticmethod
    def does_type_match_for_all(t: type, *objs: Any) -> bool:
        '''
        Returns True if all of the given objects are of the given type, False otherwise.
        '''
        assert t is not None and isinstance(objs, Iterable)

        return all(isinstance(obj, t) for obj in objs)

    @staticmethod
    def validate_type_for_all_elements(t: type, iterable: Iterable[Any]) -> None:
        '''
        Raises a ValueError if any of the given elements are not of the given type.
        '''
        assert t is not None and isinstance(iterable, Iterable)

        for elm in iterable:
            if not isinstance(elm, t):
                raise ValueError(f"Expected type {t}, got type {type(elm)}.")

    @staticmethod
    def does_type_match_for_all_elements(t: type, iterable: Iterable[Any]) -> bool:
        '''
        Returns True if all of the given elements are of the given type, False otherwise.
        '''
        assert t is not None and isinstance(iterable, Iterable)

        return all(isinstance(elm, t) for elm in iterable)
