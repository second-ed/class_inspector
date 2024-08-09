from contextlib import nullcontext as does_not_raise

import pytest
from class_inspector.class_inspector import ClassInspector

from mock_package.mock_service import MockService


@pytest.mark.parametrize(
    "inp_class, expected_result_fixture_name, expected_context",
    [
        (
            MockService(),
            "get_mock_service_parametrized_tests",
            does_not_raise(),
        ),
    ],
)
def test_get_parametrized_function_tests(
    request, inp_class, expected_result_fixture_name, expected_context
) -> None:
    with expected_context:
        ci = ClassInspector(inp_class)
        expected_result = request.getfixturevalue(expected_result_fixture_name)
        assert ci.get_parametrized_function_tests() == expected_result


@pytest.mark.parametrize(
    "inp_class, add_guards, add_debugs, expected_result_fixture_name, expected_context",
    [
        (
            MockService(),
            True,
            False,
            "get_mock_service_boilerplate_add_guards",
            does_not_raise(),
        ),
    ],
)
def test_add_boilerplate(
    request,
    inp_class,
    add_guards,
    add_debugs,
    expected_result_fixture_name,
    expected_context,
) -> None:
    with expected_context:
        ci = ClassInspector(inp_class)
        expected_result = request.getfixturevalue(expected_result_fixture_name)
        assert ci.add_boilerplate(add_guards, add_debugs) == expected_result
