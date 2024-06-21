import pytest
from class_inspector.attr_generator import AttrGenerator, AttrMap
from class_inspector.class_inspector import ClassInspector


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

    def do_something_with_args(self, a, b):
        return a + b


@pytest.fixture
def get_test_class() -> TestClass:
    return TestClass(20, 3.14)


@pytest.fixture
def get_instance(get_test_class: TestClass) -> ClassInspector:
    return ClassInspector(get_test_class)


@pytest.fixture
def get_attr_gen_attributes() -> list[AttrMap]:
    return [
        AttrMap("test1", "int", True),
        AttrMap("test2", "float", False),
        AttrMap("test3", "bool", True),
        AttrMap("test4", "str", False),
        AttrMap("test5", "List[int]", True),
        AttrMap("test6", "Dict[str, float]", False),
    ]


@pytest.fixture
def get_attr_gen_instance(
    get_attr_gen_attributes: list[AttrMap],
) -> AttrGenerator:
    return AttrGenerator("TestClass", get_attr_gen_attributes)
