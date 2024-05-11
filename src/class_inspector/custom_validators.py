from collections import abc
from typing import Callable, List, Type

__all__: List[str] = [
    "validate_bool_func",
    "validate_collection",
    "validate_collection_of_type",
    "validate_generic",
    "validate_generic_bool_func",
    "validate_generic_of_type",
    "validate_iterable",
    "validate_iterable_of_type",
    "validate_sequence",
    "validate_sequence_of_type",
]


def validate_sequence(instance, attribute, value) -> None:
    if not isinstance(value, abc.Sequence):
        raise TypeError(
            f"{attribute.name} expecting a subclass of Sequence, received {type(value)}."
            " Must implement "
            "[__getitem__, __iter__, __contains__, __reversed__, index, count]"
        )


def validate_iterable(instance, attribute, value) -> None:
    if not isinstance(value, abc.Iterable):
        raise TypeError(
            f"{attribute.name} expecting a subclass of Iterable, received {type(value)}."
            " Must implement [__iter__]"
        )


def validate_collection(instance, attribute, value) -> None:
    if not isinstance(value, abc.Collection):
        raise TypeError(
            f"{attribute.name} expecting a subclass of Collection, "
            "received {type(value)}. Must implement [__contains__, __iter__, __len__]"
        )


def validate_sequence_of_type(allowed_type: Type) -> Callable:
    def _(instance, attribute, value) -> None:
        if not isinstance(value, abc.Sequence):
            raise TypeError(
                f"{attribute.name} expecting a subclass of Sequence, received {type(value)}."
                " Must implement "
                "[__getitem__, __iter__, __contains__, __reversed__, index, count]"
            )
        for item in value:
            if not isinstance(item, allowed_type):
                raise TypeError(
                    f"{attribute.name} expecting a sequence of {allowed_type.__name__},"
                    f" received {type(item)}."
                )

    return _


def validate_iterable_of_type(allowed_type: Type) -> Callable:
    def _(instance, attribute, value) -> None:
        if not isinstance(value, abc.Iterable):
            raise TypeError(
                f"{attribute.name} expecting a subclass of Iterable, received {type(value)}."
                " Must implement [__iter__]"
            )
        for item in value:
            if not isinstance(item, allowed_type):
                raise TypeError(
                    f"{attribute.name} expecting a iterable of {allowed_type.__name__},"
                    f" received {type(item)}."
                )

    return _


def validate_collection_of_type(allowed_type: Type) -> Callable:
    def _(instance, attribute, value) -> None:
        if not isinstance(value, abc.Collection):
            raise TypeError(
                f"{attribute.name} expecting a subclass of Collection, received {type(value)}."
                " Must implement "
                "[__contains__, __iter__, __len__]"
            )
        for item in value:
            if not isinstance(item, allowed_type):
                raise TypeError(
                    f"{attribute.name} expecting a collection of {allowed_type.__name__},"
                    f" received {type(item)}."
                )

    return _


def validate_generic(generic_type: Type) -> Callable:
    def _(instance, attribute, value) -> None:
        if not isinstance(value, generic_type):
            raise TypeError(
                f"{attribute.name} expecting a subclass of {generic_type.__name__},"
                f" received {type(value)}. "
            )

    return _


def validate_generic_of_type(
    generic_type: Type, allowed_type: Type
) -> Callable:
    def _(instance, attribute, value) -> None:
        if not isinstance(value, generic_type):
            raise TypeError(
                f"{attribute.name} expecting a subclass of {generic_type.__name__},"
                f" received {type(value)}. "
            )
        for item in value:
            if not isinstance(item, allowed_type):
                raise TypeError(
                    f"{attribute.name} expecting a collection of {allowed_type.__name__},"
                    f" received {type(item)}."
                )

    return _


def validate_bool_func(bool_func):
    if not isinstance(bool_func, Callable):
        raise TypeError("provided boolean function must be callable")

    def _(instance, attribute, value) -> None:
        if not bool_func(value):
            raise ValueError(
                f"{attribute.name} does not pass {bool_func.__name__},"
                f" received {value}. "
            )

    return _


def validate_generic_bool_func(
    generic_type: Type, bool_func: Callable
) -> Callable:
    if not isinstance(bool_func, Callable):
        raise TypeError("provided boolean function must be callable")

    def _(instance, attribute, value) -> None:
        if not isinstance(value, generic_type):
            raise TypeError(
                f"{attribute.name} expecting a subclass of {generic_type.__name__},"
                f" received {type(value)}. "
            )
        for item in value:
            if not bool_func(item):
                raise ValueError(
                    f"{attribute.name} does not pass {bool_func.__name__},"
                    f" received {value}. "
                )

    return _
