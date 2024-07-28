from typing import List

import pytest
from class_inspector.attr_generator import AttrGenerator, AttrMap
from class_inspector.class_inspector import ClassInspector

from tests.mock_package import mock_utils_c
from tests.mock_package.mock_service import MockService


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
def get_attr_gen_attributes() -> List[AttrMap]:
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
    get_attr_gen_attributes: List[AttrMap],
) -> AttrGenerator:
    return AttrGenerator("TestClass", get_attr_gen_attributes)


@pytest.fixture
def get_fixture_sorted_callables_by_line_numbers():
    return {
        "main": mock_utils_c.main,
        "read_data": mock_utils_c.read_data,
        "check_extension": mock_utils_c.check_extension,
        "clean_data": mock_utils_c.clean_data,
        "_transform_data": mock_utils_c._transform_data,
        "rename_data": mock_utils_c.rename_data,
        "merge_data": mock_utils_c.merge_data,
        "save_data": mock_utils_c.save_data,
        "filepath_exists": mock_utils_c.filepath_exists,
    }


@pytest.fixture
def get_fixture_unsorted_callables_by_line_numbers():
    return {
        "clean_data": mock_utils_c.clean_data,
        "check_extension": mock_utils_c.check_extension,
        "main": mock_utils_c.main,
        "read_data": mock_utils_c.read_data,
        "_transform_data": mock_utils_c._transform_data,
        "filepath_exists": mock_utils_c.filepath_exists,
        "merge_data": mock_utils_c.merge_data,
        "save_data": mock_utils_c.save_data,
        "rename_data": mock_utils_c.rename_data,
    }


@pytest.fixture
def get_mock_service_instance():
    return MockService()


@pytest.fixture
def get_unsorted_mock_service_methods(get_mock_service_instance):
    return {
        "validate_data": get_mock_service_instance.validate_data,
        "process_data": get_mock_service_instance.process_data,
        "save_data": get_mock_service_instance.save_data,
        "fetch_data": get_mock_service_instance.fetch_data,
    }


@pytest.fixture
def get_sorted_mock_service_methods(get_mock_service_instance):
    return {
        "fetch_data": get_mock_service_instance.fetch_data,
        "process_data": get_mock_service_instance.process_data,
        "validate_data": get_mock_service_instance.validate_data,
        "save_data": get_mock_service_instance.save_data,
    }
