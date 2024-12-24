from contextlib import nullcontext as does_not_raise

import pytest


@pytest.mark.parametrize(
    "a, b, expected_result, expected_context",
    [
        pytest.param(
            a, b, expected_result, does_not_raise(), id="Ensure x when `a` is y"
        ),
        pytest.param(
            a, b, expected_result, does_not_raise(), id="Ensure x when `b` is y"
        ),
    ],
)
def test_mock_method(a, b, expected_result, expected_context):
    with expected_context:
        mock_class = MockClass()
        assert mock_class.mock_method(a, b) == expected_result


@pytest.mark.parametrize(
    "param1, param2, param3, param4, expected_result, expected_context",
    [
        pytest.param(
            param1,
            param2,
            param3,
            param4,
            expected_result,
            does_not_raise(),
            id="Ensure x when `param1` is y",
        ),
        pytest.param(
            param1,
            param2,
            param3,
            param4,
            expected_result,
            does_not_raise(),
            id="Ensure x when `param2` is y",
        ),
        pytest.param(
            param1,
            param2,
            param3,
            param4,
            expected_result,
            does_not_raise(),
            id="Ensure x when `param3` is y",
        ),
        pytest.param(
            param1,
            param2,
            param3,
            param4,
            expected_result,
            does_not_raise(),
            id="Ensure x when `param4` is y",
        ),
    ],
)
def test_mock_function(
    param1, param2, param3, param4, expected_result, expected_context
):
    with expected_context:
        assert mock_function(param1, param2, param3, param4) == expected_result


@pytest.mark.parametrize(
    "param1, param2, expected_result, expected_context",
    [
        pytest.param(
            param1,
            param2,
            expected_result,
            does_not_raise(),
            id="Ensure x when `param1` is y",
        ),
        pytest.param(
            param1,
            param2,
            expected_result,
            does_not_raise(),
            id="Ensure x when `param2` is y",
        ),
    ],
)
def test_mock_function_with_optional(param1, param2, expected_result, expected_context):
    with expected_context:
        assert mock_function_with_optional(param1, param2) == expected_result
