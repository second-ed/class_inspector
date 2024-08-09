import inspect
import logging
import re
from typing import Callable, Optional

from class_inspector._logger import compress_logging_value

logger = logging.getLogger()


def get_class_methods(obj):
    meths = {
        name: func
        for name, func in inspect.getmembers(obj, inspect.ismethod)
        if func.__self__.__class__ == obj.__class__ and _is_not_dunder(name)
    }
    return _sort_callables_by_line_numbers(meths)


def get_module_classes(inp_module):
    return _get_module_classes_or_functions(inp_module, inspect.isclass)


def get_module_functions(inp_module):
    return _get_module_classes_or_functions(inp_module, inspect.isfunction)


def camel_to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


def clean_func(func_str: str) -> str:
    for key, val in locals().items():
        logger.debug(f"{key} = {compress_logging_value(val)}")

    def _replacer(match):
        content = match.group(1)
        cleaned_content = " ".join(content.split())
        logger.debug(f"cleaned_content = {cleaned_content}")
        return f"({cleaned_content})"

    return re.sub(r"\((.*?)\)", _replacer, func_str, flags=re.DOTALL)


def find_string_end(func_str: str, pattern: str) -> Optional[int]:
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


def get_docstring_patterns() -> str:
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


def insert_string_at_idx(func_str: str, idx: int, to_insert: str) -> str:
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


def strip_underscores(item: str) -> str:
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


def _is_not_dunder(item: str) -> bool:
    return not item.startswith("__") and not item.endswith("__")


def _get_module_classes_or_functions(inp_module, is_type: Callable):
    members = {
        name: member
        for name, member in inspect.getmembers(inp_module, is_type)
        if member.__module__ == inp_module.__name__
    }
    return _sort_callables_by_line_numbers(members)


def _sort_callables_by_line_numbers(callables: dict) -> dict:
    return dict(
        sorted(
            callables.items(),
            key=lambda item: inspect.getsourcelines(item[1])[1],
        )
    )
