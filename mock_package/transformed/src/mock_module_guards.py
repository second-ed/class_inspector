from typing import Optional

import pandas as pd


class MockClass:
    def mock_method(self, a: int, b: str) -> str:
        if not all([isinstance(a, int), isinstance(b, str)]):
            raise TypeError(
                "mock_method expects arg types: [int, str], "
                f"received: [{type(a).__name__}, {type(b).__name__}]"
            )
        return str(a) + b


def mock_function(
    param1: float, param2: int, param3: bool, param4: str = "test"
) -> float:
    if not all(
        [
            isinstance(param1, float),
            isinstance(param2, int),
            isinstance(param3, bool),
            isinstance(param4, str),
        ]
    ):
        raise TypeError(
            "mock_function expects arg types: [float, int, bool, str], "
            f"received: [{type(param1).__name__}, {type(param2).__name__}, {type(param3).__name__}, {type(param4).__name__}]"
        )
    if param3:
        return param1 - param2
    else:
        return param1 + param2


def mock_function_with_optional(param1: bool, param2: Optional[int]) -> Optional[int]:
    """mock function with optional

    Args:
        param1 (bool)
        param2 (Optional[int])

    Returns:
        Optional[int]
    """
    if not all([isinstance(param1, bool), isinstance(param2, (int, NoneType))]):
        raise TypeError(
            "mock_function_with_optional expects arg types: [bool, (int, NoneType)], "
            f"received: [{type(param1).__name__}, {type(param2).__name__}]"
        )
    if param1:
        return param2
    return None


def mock_constant_literal():
    return "blah_blah_blah"


def mock_func_with_alias_typehint(data: pd.DataFrame) -> pd.DataFrame:
    if not all([isinstance(data, pd.DataFrame)]):
        raise TypeError(
            "mock_func_with_alias_typehint expects arg types: [pd.DataFrame], "
            f"received: [{type(data).__name__}]"
        )
    return data


def mock_func_with_lambda_and_raises(a: int, b: bool):
    if not all([isinstance(a, int), isinstance(b, bool)]):
        raise TypeError(
            "mock_func_with_lambda_and_raises expects arg types: [int, bool], "
            f"received: [{type(a).__name__}, {type(b).__name__}]"
        )
    double = lambda x: x * 2
    if b:
        raise ValueError()
    return double(a)
