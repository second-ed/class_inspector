from __future__ import annotations

from types import FunctionType

import pytest
from class_inspector.module_inspector import ModuleInspector

from tests.mock_package import mock_module


@pytest.fixture
def get_instance() -> ModuleInspector:
    return ModuleInspector(mock_module)


def test_init(get_instance: ModuleInspector) -> None:
    assert isinstance(get_instance, ModuleInspector)


def test_extract_custom_classes(get_instance: ModuleInspector) -> None:
    for _, v in get_instance.custom_classes.items():
        assert type(v) == type.__class__


def test_extract_custom_functions(get_instance: ModuleInspector) -> None:
    for _, v in get_instance.custom_functions.items():
        assert type(v) == FunctionType
