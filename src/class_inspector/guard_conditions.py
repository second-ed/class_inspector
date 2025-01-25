from __future__ import annotations

import re
from typing import Tuple

from class_inspector.data_structures import FuncDetails

ITERABLES = ["list", "set", "tuple", "dict"]


def get_inner_outer_types(attr_type: str) -> Tuple[str, str] | str:
    """
    Get the inner and outer types from the attribute type string.

    Args:
        attr_type (str): The attribute type string.

    Returns:
        Tuple[str, str]: The inner and outer types extracted from attr_type.

    Raises:
        TypeError: If the input is not a string.
    """
    if not all([isinstance(attr_type, str)]):
        raise TypeError(
            "get_inner_outer_types expects arg types: [str], "
            f"received: [{type(attr_type).__name__}]"
        )
    bracket_type = re.search(r"\[(.*?)\]", attr_type)
    if bracket_type:
        outer_type = attr_type.replace(bracket_type.group(), "")
        inner_type = bracket_type.group(1)
        return inner_type, outer_type
    return attr_type


def get_isinstance_type(attr_type: str) -> str:
    if not bool(re.search(r"\[.*?\]", attr_type)):
        return attr_type

    inner_type, outer_type = get_inner_outer_types(attr_type)

    if outer_type == "Optional":
        inner_type = ", ".join([inner_type, "NoneType"])

    if outer_type.lower() in ITERABLES:
        return outer_type
    if len(inner_type.split(",")) > 1:
        return f"({inner_type})"
    return inner_type


def get_guard_conditions(func_details: FuncDetails) -> str:
    expected_types, received_types = [], []

    for param in func_details.params.values():
        if param.annot:
            expected_types.append(get_isinstance_type(param.annot))
            received_types.append(f"{{type({param.name}).__name__}}")

    expected_types = ", ".join(expected_types)
    received_types = ", ".join(received_types)

    if expected_types and received_types:
        is_instances = ", ".join(
            [
                f"isinstance({param.name}, {get_isinstance_type(param.annot)})"
                for param in func_details.params.values()
                if param.annot
            ]
        )
        guards = (
            f"if not all([{is_instances}]):\n"
            "    raise TypeError("
            f'"{func_details.name} expects arg types: [{expected_types}], "'
            f' f"received: [{received_types}]")'
        )
        return guards
    return ""
