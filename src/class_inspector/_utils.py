import logging
import re
from typing import Any, Optional, Union

from ._logger import compress_logging_value

logger = logging.getLogger()


def _strip_underscores(item: str) -> str:
    """
    Remove underscores from the given string.

    Args:
        item (str): The string from which underscores should be removed.

    Returns:
        str: The string without underscores.

    Raises:
        TypeError: If the input is not a string.
    """
    for key, val in locals().items():
        logger.debug(f"{key} = {compress_logging_value(val)}")
    if not isinstance(item, str):
        raise TypeError(f"item must be of type str, got {type(item)}")
    return item.strip("_")


def _unpack_parameter(param: Any) -> str:
    if _is_union_origin(param):
        args = ", ".join(
            [_get_object_name(arg) for arg in param.__args__]
        ).replace("typing.", "")
        return f"({args})"
    return _get_object_name(param).replace("typing.", "")


def _is_union_origin(param: Any) -> bool:
    # Optional.__origin__ is Union so can use for both
    if hasattr(param, "__origin__"):
        if param.__origin__ is Union:
            return True
    return False


def _get_object_name(param: Any) -> str:
    if hasattr(param, "__name__"):
        return param.__name__
    return str(param)


def _get_docstring_patterns() -> str:
    """
    Generate a regex pattern to match Python docstrings enclosed in triple quotes.

    This method creates a pattern that matches docstrings enclosed in either
    triple double quotes (\"\"\"...\"\"\") or triple single quotes ('''...''').

    Returns:
        str: A regex pattern that matches docstrings enclosed in triple quotes.
    """
    double_quotes = r'""".*?"""\n'
    single_quotes = r"'''.*?'''\n"
    return f"({double_quotes}|{single_quotes})"


def _find_string_end(func_str: str, pattern: str) -> Optional[int]:
    """
    Find the end index of the first match of a pattern in a string.

    This method searches for the given regex pattern in the provided string
    and returns the end index of the first match found.

    Args:
        func_str (str): The string in which to search for the pattern.
        pattern (str): The regex pattern to search for in the string.

    Returns:
        int | None: The end index of the first match if found, otherwise None.
    """
    for key, val in locals().items():
        logger.debug(f"{key} = {compress_logging_value(val)}")
    match = re.search(pattern, func_str, re.DOTALL)
    if match:
        return match.end()
    return None


def _insert_string_at_idx(func_str: str, idx: int, to_insert: str) -> str:
    """
    Insert a string at a specified index in another string.

    This method inserts the specified string `to_insert` into the given
    string `func_str` at the specified index `idx`.

    Args:
        func_str (str): The original string where the insertion will occur.
        idx (int): The index at which to insert the new string.
        to_insert (str): The string to be inserted into the original string.

    Returns:
        str: The modified string with `to_insert` inserted at the specified index.
    """
    for key, val in locals().items():
        logger.debug(f"{key} = {compress_logging_value(val)}")
    return func_str[:idx] + to_insert + func_str[idx:]


def _camel_to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


def _clean_func(func_str: str) -> str:
    for key, val in locals().items():
        logger.debug(f"{key} = {compress_logging_value(val)}")

    def replacer(match):
        content = match.group(1)
        cleaned_content = " ".join(content.split())
        logger.debug(f"cleaned_content = {cleaned_content}")
        return f"({cleaned_content})"

    return re.sub(r"\((.*?)\)", replacer, func_str, flags=re.DOTALL)
