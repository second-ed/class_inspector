from contextlib import nullcontext as does_not_raise
from typing import List, Optional, Union

import pytest
from class_inspector import _utils as utils


@pytest.mark.parametrize(
    "item, expected_result, expected_context",
    [
        ("__test__", "test", does_not_raise()),
        ("_test", "test", does_not_raise()),
        ("test_", "test", does_not_raise()),
        ("__test", "test", does_not_raise()),
        (0, "", pytest.raises(TypeError)),
    ],
)
def test_values_strip_underscores(
    item,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert utils._strip_underscores(item) == expected_result


@pytest.mark.parametrize(
    "param, expected_result, expected_context",
    [
        (int, "int", does_not_raise()),
        (float, "float", does_not_raise()),
        (List, "List", does_not_raise()),
        (Optional[List], "(List, NoneType)", does_not_raise()),
        (Union[int, float], "(int, float)", does_not_raise()),
    ],
)
def test_unpack_parameter(
    param,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert utils._unpack_parameter(param) == expected_result


def test_get_docstring_patterns() -> None:
    assert (
        utils._get_docstring_patterns() == "(\"\"\".*?\"\"\"\\n|'''.*?'''\\n)"
    )


@pytest.mark.parametrize(
    "func_str, pattern, expected_result, expected_context",
    [
        ("test (passing) case", r"\(\w+?\)", 14, does_not_raise()),
        # (func_str, pattern, None, pytest.raises(TypeError)),
        # (func_str, pattern, None, pytest.raises(TypeError)),
    ],
)
def test_find_string_end(
    func_str,
    pattern,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert utils._find_string_end(func_str, pattern) == expected_result


@pytest.mark.parametrize(
    "func_str, idx, to_insert, expected_result, expected_context",
    [
        ("test case", 5, "PASSED ", "test PASSED case", does_not_raise()),
        # (func_str, idx, to_insert, None, pytest.raises(TypeError)),
        # (func_str, idx, to_insert, None, pytest.raises(TypeError)),
        # (func_str, idx, to_insert, None, pytest.raises(TypeError)),
    ],
)
def test_insert_string_at_idx(
    func_str,
    idx,
    to_insert,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            utils._insert_string_at_idx(func_str, idx, to_insert)
            == expected_result
        )


@pytest.mark.parametrize(
    "item, expected_result, expected_context",
    [
        ("TestCase", "test_case", does_not_raise()),
    ],
)
def test_camel_to_snake(
    item,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert utils._camel_to_snake(item) == expected_result
