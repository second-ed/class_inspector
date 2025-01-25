from typing import Optional

import pandas as pd


class MockClass:
    def mock_method(self, a: int, b: str) -> str:
        return str(a) + b


def mock_function(
    param1: float, param2: int, param3: bool, param4: str = "test"
) -> float:
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
    if param1:
        return param2
    return None


def mock_constant_literal():
    return "blah_blah_blah"


def mock_func_with_alias_typehint(data: pd.DataFrame) -> pd.DataFrame:
    return data


def mock_func_with_lambda_and_raises(a: int, b: bool):
    double = lambda x: x * 2
    if b:
        raise ValueError()
    return double(a)
