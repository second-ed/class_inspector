import re
from typing import List, Tuple

ITERABLES = ["list", "set", "tuple"]
MAPPINGS = ["dict"]


def contains_square_brackets(attr_type: str) -> bool:
    """
    Check if the given attribute type contains square brackets.

    Args:
        attr_type (str): The attribute type to check.

    Returns:
        bool: True if square brackets are found, False otherwise.

    Raises:
        TypeError: If the input is not a string.
    """
    if not all([isinstance(attr_type, str)]):
        raise TypeError(
            "contains_square_brackets() expects args of types [str]"
            f"recieved type: {type(attr_type).__name__}"
        )
    return bool(re.search(r"\[.*?\]", attr_type))


def is_outer_type_in_list(attr_type: str, deep_list: List[str]) -> bool:
    """
    Check if the outer type of the attribute is in the given list.

    Args:
        attr_type (str): The attribute type to check.
        deep_list (List[str]): List of outer types to compare against.

    Returns:
        bool: True if the outer type is in the list, False otherwise.

    Raises:
        TypeError: If the inputs are not of the correct types.
    """
    if not all([isinstance(attr_type, str), isinstance(deep_list, list)]):
        raise TypeError(
            "is_outer_type_in_list expects arg types: [str, List], "
            f"received: [{type(attr_type).__name__}, {type(deep_list).__name__}]"
        )
    _, outer_type = get_inner_outer_types(attr_type)
    return outer_type in deep_list


def is_deep_iterable(attr_type: str) -> bool:
    """
    Check if the attribute type is a deep iterable.

    Args:
        attr_type (str): The attribute type to check.

    Returns:
        bool: True if the attribute type is a deep iterable, False otherwise.

    Raises:
        TypeError: If the input is not a string.
    """
    if not all([isinstance(attr_type, str)]):
        raise TypeError(
            "is_deep_iterable expects arg types: [str], received: "
            f"[{type(attr_type).__name__}]"
        )
    return contains_square_brackets(attr_type) and is_outer_type_in_list(
        attr_type, ITERABLES
    )


def is_deep_mapping(attr_type: str) -> bool:
    """
    Check if the attribute type is a deep mapping.

    Args:
        attr_type (str): The attribute type to check.

    Returns:
        bool: True if the attribute type is a deep mapping, False otherwise.

    Raises:
        TypeError: If the input is not a string.
    """
    if not all([isinstance(attr_type, str)]):
        raise TypeError(
            "is_deep_mapping expects arg types: [str], "
            f"received: [{type(attr_type).__name__}]"
        )
    return contains_square_brackets(attr_type) and is_outer_type_in_list(
        attr_type, MAPPINGS
    )


def get_inner_outer_types(attr_type: str) -> Tuple[str, str]:
    """
    Get the inner and outer types from the attribute type string.

    Args:
        attr_type (str): The attribute type string.

    Returns:
        Tuple[str, str]: The inner and outer types extracted from attr_type.

    Raises:
        TypeError: If the input is not a string.
        AttributeError: If the regular expression does not match.
    """
    if not all([isinstance(attr_type, str)]):
        raise TypeError(
            "get_inner_outer_types expects arg types: [str], "
            f"received: [{type(attr_type).__name__}]"
        )
    bracket_type = re.search(r"\[(.*?)\]", attr_type)
    if bracket_type:
        outer_type = attr_type.replace(bracket_type.group(), "").lower()
        inner_type = bracket_type.group(1)
        return inner_type, outer_type
    raise AttributeError(f"{bracket_type} does not have method group()")


def get_type_hint(attr_type: str) -> str:
    """
    Get the type hint for the attribute.

    Args:
        attr_type (str): The attribute type string.

    Returns:
        str: The type hint for the attribute.

    Raises:
        TypeError: If the input is not a string.
    """
    if not all([isinstance(attr_type, str)]):
        raise TypeError(
            "get_type_hint expects arg types: [str], "
            f"received: [{type(attr_type).__name__}]"
        )
    if is_deep_iterable(attr_type) or is_deep_mapping(attr_type):
        _, outer_type = get_inner_outer_types(attr_type)
        return outer_type
    return attr_type
