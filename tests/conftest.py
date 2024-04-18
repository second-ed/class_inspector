from __future__ import annotations

import pytest

from src.class_inspector.class_inspector import ClassInspector


class TestClass:
    def __init__(self, x: int, y: float) -> None:
        self._x: int = x
        self.y: float = y
        self.z_: bool = x > y

    def do_something(self) -> bool:
        return self.z_

    def _do_something_internally(self) -> float:
        return self._x - self.y

    def do_something_derived_(self) -> bool:
        return self._x != self.z_


@pytest.fixture
def get_test_class() -> TestClass:
    return TestClass(20, 3.14)


@pytest.fixture
def get_instance(get_test_class: TestClass) -> ClassInspector:
    return ClassInspector(get_test_class)
