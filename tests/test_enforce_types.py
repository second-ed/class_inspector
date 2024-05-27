from contextlib import nullcontext as does_not_raise
from typing import List

import pytest
from class_inspector.enforce_types import enforce_types


@pytest.mark.parametrize(
    "args, kwargs, expected_result, expected_context",
    [
        (
            (1, 2.0),
            {"param3": "test", "param4": ["case"]},
            [1, 2.0, "test", ["case"]],
            does_not_raise(),
        ),
        (
            (1.0, 2.0),
            {"param3": "test", "param4": ["case"]},
            None,
            pytest.raises(TypeError),
        ),
        (
            (1, 2),
            {"param3": "test", "param4": ["case"]},
            None,
            pytest.raises(TypeError),
        ),
        (
            (1, 2.0),
            {"param3": ["test"], "param4": ["case"]},
            None,
            pytest.raises(TypeError),
        ),
        (
            (1, 2.0),
            {"param3": "test", "param4": "case"},
            None,
            pytest.raises(TypeError),
        ),
    ],
)
def test_enforce_types(args, kwargs, expected_result, expected_context):
    @enforce_types
    def test_function(param1: int, param2: float, param3: str, param4: List):
        return [param1, param2, param3, param4]

    with expected_context:
        assert expected_result == test_function(*args, **kwargs)
