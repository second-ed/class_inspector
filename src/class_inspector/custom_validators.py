from __future__ import annotations

from collections import abc

__all__: list[str] = [
    "validate_sequence",
    "validate_iterable",
    "validate_collection",
]


def validate_sequence(instance, attribute, value) -> None:
    if not issubclass(value, abc.Sequence):
        raise TypeError(
            f"{attribute.name} expecting a subclass of Sequence, received {type(value)}. Must implement [__getitem__, __iter__, __contains__, __reversed__, index, count]"
        )


def validate_iterable(instance, attribute, value) -> None:
    if not issubclass(value, abc.Iterable):
        raise TypeError(
            f"{attribute.name} expecting a subclass of Iterable, received {type(value)}. Must implement [__iter__]"
        )


def validate_collection(instance, attribute, value) -> None:
    if not issubclass(value, abc.Collection):
        raise TypeError(
            f"{attribute.name} expecting a subclass of Collection, received {type(value)}. Must implement [__contains__, __iter__, __len__]"
        )
