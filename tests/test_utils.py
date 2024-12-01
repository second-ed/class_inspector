from contextlib import nullcontext as does_not_raise

import pytest

from class_inspector import _utils as utils
from mock_package import mock_module, mock_utils_c


@pytest.mark.parametrize(
    "class_instance_fixture_name, expected_result_fixture_name, expected_context",
    [
        (
            "get_mock_service_instance",
            "get_sorted_mock_service_methods",
            does_not_raise(),
        ),
    ],
)
def test_get_class_methods(
    request,
    class_instance_fixture_name,
    expected_result_fixture_name,
    expected_context,
) -> None:
    with expected_context:
        inp_class_instance = request.getfixturevalue(class_instance_fixture_name)
        expected_result = request.getfixturevalue(expected_result_fixture_name)
        assert utils.get_class_methods(inp_class_instance) == expected_result


@pytest.mark.parametrize(
    "inp_module, expected_result, expected_context",
    [
        (
            mock_module,
            {"MockClass": mock_module.MockClass},
            does_not_raise(),
        ),
    ],
)
def test_get_module_classes(
    request, inp_module, expected_result, expected_context
) -> None:
    with expected_context:
        assert utils.get_module_classes(inp_module) == expected_result


@pytest.mark.parametrize(
    "inp_module, expected_result_fixture_name, expected_context",
    [
        (
            mock_utils_c,
            "get_fixture_sorted_callables_by_line_numbers",
            does_not_raise(),
        ),
    ],
)
def test_get_module_functions(
    request, inp_module, expected_result_fixture_name, expected_context
) -> None:
    with expected_context:
        expected_result = request.getfixturevalue(expected_result_fixture_name)
        assert utils.get_module_functions(inp_module) == expected_result


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
        assert utils.camel_to_snake(item) == expected_result


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
        assert utils.find_string_end(func_str, pattern) == expected_result


def test_get_docstring_patterns() -> None:
    assert utils.get_docstring_patterns() == "(\"\"\".*?\"\"\"\\n|'''.*?'''\\n)"


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
        assert utils.insert_string_at_idx(func_str, idx, to_insert) == expected_result


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
def test_strip_underscores(
    item,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert utils.strip_underscores(item) == expected_result


@pytest.mark.parametrize(
    "item, expected_result, expected_context",
    [
        ("test", True, does_not_raise()),
        ("_test", True, does_not_raise()),
        ("test_", True, does_not_raise()),
        ("__test__", False, does_not_raise()),
    ],
)
def test_is_not_dunder(item, expected_result, expected_context) -> None:
    with expected_context:
        assert utils._is_not_dunder(item) == expected_result


@pytest.mark.parametrize(
    "callables_fixture_name, expected_result_fixture_name, expected_context",
    [
        (
            "get_fixture_unsorted_callables_by_line_numbers",
            "get_fixture_sorted_callables_by_line_numbers",
            does_not_raise(),
        ),
    ],
)
def test_sort_callables_by_line_numbers(
    request,
    callables_fixture_name,
    expected_result_fixture_name,
    expected_context,
) -> None:
    with expected_context:
        callables = request.getfixturevalue(callables_fixture_name)
        expected_result = request.getfixturevalue(expected_result_fixture_name)
        assert utils._sort_callables_by_line_numbers(callables) == expected_result
