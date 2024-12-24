import inspect
from contextlib import nullcontext as does_not_raise

import pytest

import class_inspector.transform as tf
import mock_package.original.mock_module as mock_module
import mock_package.transformed.src.mock_module_debugs_guards as mock_module_debugs_guards
import mock_package.transformed.src.mock_module_guards as mock_module_guards
from class_inspector.utils import format_code_str


@pytest.mark.parametrize(
    "obj, add_debugs, add_guards, expected_result, expected_context",
    [
        pytest.param(
            mock_module,
            True,
            True,
            inspect.getsource(mock_module_debugs_guards),
            does_not_raise(),
            id="Ensure x when `obj` is y",
        ),
        pytest.param(
            mock_module,
            False,
            True,
            inspect.getsource(mock_module_guards),
            does_not_raise(),
            id="Ensure x when `obj` is y",
        ),
    ],
)
def test_add_boilerplate(
    obj, add_debugs, add_guards, expected_result, expected_context
):
    with expected_context:
        assert format_code_str(
            tf.add_boilerplate(obj, add_debugs, add_guards)
        ) == format_code_str(expected_result)


@pytest.mark.parametrize(
    "obj, test_raises, raises_arg_types, expected_result_fixture_name, expected_context",
    [
        pytest.param(
            mock_module,
            True,
            False,
            "get_fixture_test_mock_module",
            does_not_raise(),
            id="Ensure x when `obj` is y",
        ),
    ],
)
def test_get_parametrized_tests(
    request,
    obj,
    test_raises,
    raises_arg_types,
    expected_result_fixture_name,
    expected_context,
):
    with expected_context:
        expected_result = request.getfixturevalue(expected_result_fixture_name)
        assert format_code_str(
            tf.get_parametrized_tests(obj, test_raises, raises_arg_types)
        ) == format_code_str(expected_result)
