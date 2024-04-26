from __future__ import annotations

from collections import abc
from typing import Callable, Type

__all__: list[str] = [
    "validate_sequence",
    "validate_iterable",
    "validate_collection",
    "validate_sequence_of_type",
    "validate_iterable_of_type",
    "validate_collection_of_type",
    "validate_generic",
    "validate_generic_of_type",
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
    def validate_seq_type(instance, attribute, value) -> None:
        if not isinstance(value, abc.Sequence):
            raise TypeError(
                f"{attribute.name} expecting a subclass of Sequence, received {type(value)}."
                " Must implement "
                "[__getitem__, __iter__, __contains__, __reversed__, index, count]"
            )
        else:
            for item in value:
                if not isinstance(item, allowed_type):
                    raise TypeError(
                        f"{attribute.name} expecting a sequence of {allowed_type.__name__},"
                        f" received {type(item)}."
                    )

    return validate_seq_type


def validate_iterable_of_type(allowed_type: Type) -> Callable:
    def validate_iter_type(instance, attribute, value) -> None:
        if not isinstance(value, abc.Iterable):
            raise TypeError(
                f"{attribute.name} expecting a subclass of Iterable, received {type(value)}."
                " Must implement [__iter__]"
            )
        else:
            for item in value:
                if not isinstance(item, allowed_type):
                    raise TypeError(
                        f"{attribute.name} expecting a iterable of {allowed_type.__name__},"
                        f" received {type(item)}."
                    )

    return validate_iter_type


def validate_collection_of_type(allowed_type: Type) -> Callable:
    def validate_col_type(instance, attribute, value) -> None:
        if not isinstance(value, abc.Collection):
            raise TypeError(
                f"{attribute.name} expecting a subclass of Collection, received {type(value)}."
                " Must implement "
                "[__contains__, __iter__, __len__]"
            )
        else:
            for item in value:
                if not isinstance(item, allowed_type):
                    raise TypeError(
                        f"{attribute.name} expecting a collection of {allowed_type.__name__},"
                        f" received {type(item)}."
                    )

    return validate_col_type


def validate_generic(generic_type: Type) -> Callable:
    def validate_gen_type(instance, attribute, value) -> None:
        if not isinstance(value, generic_type):
            raise TypeError(
                f"{attribute.name} expecting a subclass of {generic_type.__name__},"
                f" received {type(value)}. "
            )

    return validate_gen_type


def validate_generic_of_type(
    generic_type: Type, allowed_type: Type
) -> Callable:
    def validate_gen_type(instance, attribute, value) -> None:
        if not isinstance(value, generic_type):
            raise TypeError(
                f"{attribute.name} expecting a subclass of {generic_type.__name__},"
                f" received {type(value)}. "
            )
        else:
            for item in value:
                if not isinstance(item, allowed_type):
                    raise TypeError(
                        f"{attribute.name} expecting a collection of {allowed_type.__name__},"
                        f" received {type(item)}."
                    )

    return validate_gen_type
