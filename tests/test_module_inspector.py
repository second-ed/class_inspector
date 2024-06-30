from __future__ import annotations

from types import FunctionType

import pytest
from class_inspector.module_inspector import ModuleInspector

from tests.mock_package import mock_module


@pytest.fixture
def get_instance() -> ModuleInspector:
    return ModuleInspector(mock_module)


@pytest.mark.skip()
def test_init(get_instance: ModuleInspector) -> None:
    assert isinstance(get_instance, ModuleInspector)


@pytest.mark.skip()
def test_extract_custom_classes(get_instance: ModuleInspector) -> None:
    for _, v in get_instance.custom_classes.items():
        assert type(v) == type.__class__

    assert set(c.__name__ for c in get_instance.custom_classes.values()) == {
        "TestClass",
    }


@pytest.mark.skip()
def test_extract_custom_functions(get_instance: ModuleInspector) -> None:
    for _, v in get_instance.custom_functions.items():
        assert type(v) == FunctionType

    assert set(
        func.__name__ for func in get_instance.custom_functions.values()
    ) == {
        "mock_func1",
        "mock_func2",
    }


@pytest.mark.skip()
def test_get_parametrized_function_tests(
    get_instance: ModuleInspector,
) -> None:
    assert get_instance.get_parametrized_function_tests() == (
        "@pytest.mark.parametrize(\n"
        '    "a, b, expected_result, expected_context",\n'
        "    [\n"
        "        (a, b, expected_result, expected_context),\n"
        "        (a, b, None, pytest.raises(TypeError)),\n"
        "        (a, b, None, pytest.raises(TypeError)),\n"
        "    ]\n)\n"
        "def test_mock_func1(a, b, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert mock_func1(a, b) == expected_result\n\n\n"
        "@pytest.mark.parametrize(\n"
        '    "a, b, expected_result, expected_context",\n'
        "    [\n"
        "        (a, b, expected_result, expected_context),\n"
        "        (a, b, None, pytest.raises(TypeError)),\n"
        "        (a, b, None, pytest.raises(TypeError)),\n"
        "    ]\n)\n"
        "def test_mock_func2(a, b, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert mock_func2(a, b) == expected_result\n\n\n"
    )
