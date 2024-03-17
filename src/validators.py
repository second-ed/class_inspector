from collections import abc
from typing import Callable


def validate_int(instance, attribute, value) -> None:
    if not isinstance(value, int):
        raise TypeError(
            f"{attribute.name} expecting an integer, received {type(value)}"
        )


def validate_str(instance, attribute, value) -> None:
    if not isinstance(value, str):
        raise TypeError(
            f"{attribute.name} expecting a string, received {type(value)}"
        )


def validate_float(instance, attribute, value) -> None:
    if not isinstance(value, float):
        raise TypeError(
            f"{attribute.name} expecting a float, received {type(value)}"
        )


def validate_bool(instance, attribute, value) -> None:
    if not isinstance(value, bool):
        raise TypeError(
            f"{attribute.name} expecting a boolean, received {type(value)}"
        )


def validate_list(instance, attribute, value) -> None:
    if not isinstance(value, list):
        raise TypeError(
            f"{attribute.name} expecting a list, received {type(value)}"
        )


def validate_not_empty_list(instance, attribute, value) -> None:
    if not value:
        raise ValueError(
            f"{attribute.name} must not be an empty list, received {value}"
        )


def validate_dict(instance, attribute, value) -> None:
    if not isinstance(value, dict):
        raise TypeError(
            f"{attribute.name} expecting a dictionary, received {type(value)}"
        )


def validate_tuple(instance, attribute, value) -> None:
    if not isinstance(value, tuple):
        raise TypeError(
            f"{attribute.name} expecting a tuple, received {type(value)}"
        )


def validate_set(instance, attribute, value) -> None:
    if not isinstance(value, set):
        raise TypeError(
            f"{attribute.name} expecting a set, received {type(value)}"
        )


def validate_none(instance, attribute, value) -> None:
    if value is not None:
        raise ValueError(f"{attribute.name} must be None, received {value}")


def validate_not_none(instance, attribute, value) -> None:
    if value is None:
        raise ValueError(
            f"{attribute.name} must not be None, received {value}"
        )


def validate_non_empty_string(instance, attribute, value) -> None:
    if not isinstance(value, str) or len(value.strip()) == 0:
        raise ValueError(
            f"{attribute.name} expecting a non-empty string, received {value}"
        )


def validate_non_negative(instance, attribute, value) -> None:
    if value < 0:
        raise ValueError(
            f"{attribute.name} expecting a non-negative number, received {value}"
        )


def validate_non_positive(instance, attribute, value) -> None:
    if value > 0:
        raise ValueError(
            f"{attribute.name} expecting a non-positive number, received {value}"
        )


def validate_positive(instance, attribute, value) -> None:
    if value <= 0:
        raise ValueError(
            f"{attribute.name} expecting a positive number, received {value}"
        )


def validate_non_zero(instance, attribute, value) -> None:
    if value == 0:
        raise ValueError(
            f"{attribute.name} expecting a non-zero number, received {value}"
        )


def validate_range(min_value, max_value) -> Callable[..., None]:
    def validate_inner(instance, attribute, value) -> None:
        if not min_value <= value <= max_value:
            raise ValueError(
                f"{attribute.name} expecting value in the range [{min_value}, {max_value}], received {value}"
            )

    return validate_inner


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
