from contextlib import nullcontext as does_not_raise

import pytest
from class_inspector.module_inspector import ModuleInspector

from mock_package import mock_service, mock_utils_c


@pytest.mark.parametrize(
    "module, expected_result, expected_context",
    [
        (mock_utils_c, set(), does_not_raise()),
        (
            mock_service,
            {"MockService"},
            does_not_raise(),
        ),
    ],
)
def test_extract_custom_classes(
    module, expected_result, expected_context
) -> None:
    with expected_context:
        mi = ModuleInspector(module)
        assert (
            set(c.__name__ for c in mi.custom_classes.values())
            == expected_result
        )


@pytest.mark.parametrize(
    "module, expected_result, expected_context",
    [
        (
            mock_utils_c,
            {
                "_transform_data",
                "check_extension",
                "clean_data",
                "filepath_exists",
                "main",
                "merge_data",
                "read_data",
                "rename_data",
                "save_data",
            },
            does_not_raise(),
        ),
        (
            mock_service,
            set(),
            does_not_raise(),
        ),
    ],
)
def test_extract_custom_functions(
    module, expected_result, expected_context
) -> None:
    with expected_context:
        mi = ModuleInspector(module)
        assert (
            set(func.__name__ for func in mi.custom_functions.values())
            == expected_result
        )


@pytest.mark.parametrize(
    "module, expected_result_fixture_name, expected_context",
    [
        (
            mock_utils_c,
            "get_mock_utils_c_parametrized_tests",
            does_not_raise(),
        ),
    ],
)
def test_get_parametrized_function_tests(
    request, module, expected_result_fixture_name, expected_context
) -> None:
    with expected_context:
        mi = ModuleInspector(module)
        expected_result = request.getfixturevalue(expected_result_fixture_name)
        assert mi.get_parametrized_function_tests() == expected_result


@pytest.mark.parametrize(
    "module, add_guards, add_debugs, expected_result_fixture_name, expected_context",
    [
        (
            mock_utils_c,
            True,
            False,
            "get_mock_utils_c_with_guards",
            does_not_raise(),
        ),
        (
            mock_utils_c,
            False,
            True,
            "get_mock_utils_c_with_debugs",
            does_not_raise(),
        ),
        (
            mock_utils_c,
            True,
            True,
            "get_mock_utils_c_with_guards_and_debugs",
            does_not_raise(),
        ),
    ],
)
def test_add_boilerplate(
    request,
    module,
    add_guards,
    add_debugs,
    expected_result_fixture_name,
    expected_context,
) -> None:
    with expected_context:
        mi = ModuleInspector(module)
        expected_result = request.getfixturevalue(expected_result_fixture_name)
        assert mi.add_boilerplate(add_guards, add_debugs) == expected_result
