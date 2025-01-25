from __future__ import annotations

import re
import threading
from functools import wraps
from typing import Callable, Tuple, Union

import black
import isort
import libcst as cst


def get_src_code(path: str) -> str:
    with open(path, "r") as f:
        src_code = f.read()
    return src_code


def str_to_cst(code: str) -> cst.Module:
    return cst.parse_module(code)


def cst_to_str(node) -> str:
    return cst.Module([]).code_for_node(node)


def format_code_str(code_snippet: str) -> str:
    return black.format_str(isort.code(code_snippet), mode=black.FileMode())


def is_dunder(item: str) -> bool:
    return item.startswith("__") and item.endswith("__")


def camel_to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ExceptionLogger(metaclass=SingletonMeta):
    _log_lock = threading.Lock()
    log = []

    @classmethod
    def catch_raise(
        cls,
        custom_exception: Exception = Exception,
        catch_exceptions: Union[Exception, Tuple[Exception]] = Exception,
        msg: str = "",
    ) -> Callable:
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    res = func(*args, **kwargs)
                    return res, None
                except catch_exceptions as e:
                    raise_exception = (
                        custom_exception
                        if custom_exception is not Exception
                        else type(e)
                    )
                    exc = raise_exception(
                        {
                            "func": func.__name__,
                            "args": args,
                            "kwargs": kwargs,
                            "caught_error": e,
                            "msg": msg or str(e),
                        }
                    )
                    with cls._log_lock:  # Ensure thread safety
                        cls.log.append(exc)
                    return None, exc

            return wrapper

        return decorator
