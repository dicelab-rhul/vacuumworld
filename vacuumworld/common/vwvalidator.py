from typing import Iterable, Any, Optional, Type, cast
from pydoc import locate


class VWValidator():
    @staticmethod
    def validate_not_none(obj: Optional[Any]) -> None:
        if obj is None:
            raise ValueError("Object cannot be None.")

    @staticmethod
    def validate_all_not_none(*objs: Optional[Any]) -> None:
        if any([obj is None for obj in objs]):
            raise ValueError("One or more objects are None.")

    @staticmethod
    def validate_all_elements_not_none(iterable: Optional[Iterable[Any]]) -> None:
        if iterable is None or any([obj is None for obj in iterable]):
            raise ValueError("Either the iterable, or one or more of its elements are None.")

    @staticmethod
    def validate_type(t: Type[Any], obj: Any) -> None:
        assert t is not None and obj is not None

        if not isinstance(obj, t):
            raise ValueError(f"Expected type {t}, got type {type(obj)}.")

    @staticmethod
    def validate_type_from_string(ts: str, obj: Any) -> None:
        assert ts is not None and obj is not None

        t: Type[Any] = cast(Type[Any], locate(ts))

        if not isinstance(obj, t):
            raise ValueError(f"Expected type {t}, got type {type(obj)}.")

    @staticmethod
    def does_type_match(t: type, obj: Any) -> bool:
        assert t is not None and obj is not None

        return isinstance(obj, t)

    @staticmethod
    def validate_type_for_all(t: type, *objs: Any) -> None:
        assert t is not None and isinstance(objs, Iterable)

        for obj in objs:
            if not isinstance(obj, t):
                raise ValueError(f"Expected type {t}, got type {type(obj)}.")

    @staticmethod
    def does_type_match_for_all(t: type, *objs: Any) -> bool:
        assert t is not None and isinstance(objs, Iterable)

        return all([isinstance(obj, t) for obj in objs])

    @staticmethod
    def validate_type_for_all_elements(t: type, iterable: Iterable[Any]) -> None:
        assert t is not None and isinstance(iterable, Iterable)

        for elm in iterable:
            if not isinstance(elm, t):
                raise ValueError(f"Expected type {t}, got type {type(elm)}.")

    @staticmethod
    def does_type_match_for_all_elements(t: type, iterable: Iterable[Any]) -> bool:
        assert t is not None and isinstance(iterable, Iterable)

        return all([isinstance(elm, t) for elm in iterable])
