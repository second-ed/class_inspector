from __future__ import annotations


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


def mock_func1(a, b):
    return a + b


def mock_func2(a, b):
    return a * b
