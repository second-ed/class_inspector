from typing import Optional


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
