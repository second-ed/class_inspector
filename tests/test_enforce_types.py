from contextlib import nullcontext as does_not_raise
from typing import Dict, List, Optional, Set, Union

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


@pytest.mark.parametrize(
    "args, kwargs, expected_result, expected_context",
    [
        (
            ({"test": "case"}, [1, 2, 3]),
            {"param3": {2.0, 2.1}, "param4": [1.0, 2.0]},
            [{"test": "case"}, [1, 2, 3], {2.0, 2.1}, [1.0, 2.0]],
            does_not_raise(),
        ),
        (
            ({"test": "case"}, [1, 2, 3]),
            {"param3": {0: 2.0, 1: 2.1}, "param4": None},
            [{"test": "case"}, [1, 2, 3], {0: 2.0, 1: 2.1}, None],
            does_not_raise(),
        ),
        (
            ({"test", "case"}, [1, 2, 3]),
            {"param3": {2.0, 2.1}, "param4": [1.0, 2.0]},
            None,
            pytest.raises(TypeError),
        ),
        (
            ({"test": "case"}, {1, 2, 3}),
            {"param3": {2.0, 2.1}, "param4": [1.0, 2.0]},
            None,
            pytest.raises(TypeError),
        ),
        (
            ({"test": "case"}, [1, 2, 3]),
            {"param3": 1, "param4": None},
            None,
            pytest.raises(TypeError),
        ),
        (
            ({"test": "case"}, [1, 2, 3]),
            {"param3": {0: 2.0, 1: 2.1}, "param4": 1},
            None,
            pytest.raises(TypeError),
        ),
    ],
)
def test_complex_enforce_types(
    args, kwargs, expected_result, expected_context
):
    @enforce_types
    def test_function(
        param1: Dict[str, str],
        param2: List[int],
        param3: Union[Set[float], Dict[int, float]],
        param4: Optional[List[float]],
    ):
        return [param1, param2, param3, param4]

    with expected_context:
        assert expected_result == test_function(*args, **kwargs)
