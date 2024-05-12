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
    """
    Validate that the value is a subclass of Sequence.

    Args:
        instance: The instance the attribute belongs to.
        attribute: The attribute being validated.
        value: The value of the attribute.

    Raises:
        TypeError: If the value is not a subclass of Sequence.
    """
    if not isinstance(value, abc.Sequence):
        raise TypeError(
            f"{attribute.name} expecting a subclass of Sequence, received {type(value)}."
            " Must implement "
            "[__getitem__, __iter__, __contains__, __reversed__, index, count]"
        )


def validate_iterable(instance, attribute, value) -> None:
    """
    Validate that the value is a subclass of Iterable.

    Args:
        instance: The instance the attribute belongs to.
        attribute: The attribute being validated.
        value: The value of the attribute.

    Raises:
        TypeError: If the value is not a subclass of Iterable.
    """
    if not isinstance(value, abc.Iterable):
        raise TypeError(
            f"{attribute.name} expecting a subclass of Iterable, received {type(value)}."
            " Must implement [__iter__]"
        )


def validate_collection(instance, attribute, value) -> None:
    """
    Validate that the value is a subclass of Collection.

    Args:
        instance: The instance the attribute belongs to.
        attribute: The attribute being validated.
        value: The value of the attribute.

    Raises:
        TypeError: If the value is not a subclass of Collection.
    """
    if not isinstance(value, abc.Collection):
        raise TypeError(
            f"{attribute.name} expecting a subclass of Collection, "
            "received {type(value)}. Must implement [__contains__, __iter__, __len__]"
        )


def validate_sequence_of_type(allowed_type: Type) -> Callable:
    """
    Validate that the value is a sequence of a specific type.

    Args:
        allowed_type (Type): The type each item in the sequence should be.

    Returns:
        Callable: A validation function.

    Raises:
        TypeError: If the value is not a subclass of Sequence.
    """

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
    """
    Validate that the value is an iterable of a specific type.

    Args:
        allowed_type (Type): The type each item in the iterable should be.

    Returns:
        Callable: A validation function.

    Raises:
        TypeError: If the value is not a subclass of Iterable.
    """

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
    """
    Validate that the value is a collection of a specific type.

    Args:
        allowed_type (Type): The type each item in the collection should be.

    Returns:
        Callable: A validation function.

    Raises:
        TypeError: If the value is not a subclass of Collection.
    """

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
    """
    Validate that the value is a subclass of a specific generic type.

    Args:
        generic_type (Type): The generic type.

    Returns:
        Callable: A validation function.
    """

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
    """
    Validate that the value is a collection of a specific generic type.

    Args:
        generic_type (Type): The generic type.
        allowed_type (Type): The type each item in the collection should be.

    Returns:
        Callable: A validation function.
    """

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


def validate_bool_func(bool_func) -> Callable:
    """
    Validate the value using a custom boolean function.

    Args:
        bool_func: The boolean function to apply to the value.

    Returns:
        Callable: A validation function.

    Raises:
        TypeError: If the provided boolean function is not callable.
    """
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
    """
    Validate that the value is a collection of a specific generic type
    using a custom boolean function.

    Args:
        generic_type (Type): The generic type.
        bool_func (Callable): The boolean function to apply to each item.

    Returns:
        Callable: A validation function.

    Raises:
        TypeError: If the provided boolean function is not callable.
    """
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
