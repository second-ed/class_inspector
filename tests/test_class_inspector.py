import pytest
from class_inspector.class_inspector import ClassInspector


@pytest.mark.skip
def test_init(get_instance: ClassInspector) -> None:
    assert isinstance(get_instance, ClassInspector)


@pytest.mark.parametrize(
    "item, use_properties, result",
    [
        ("_x", True, "@property\ndef x(self) -> int:\n    return self._x\n\n"),
        (
            "y",
            True,
            "@property\ndef y(self) -> float:\n    return self._y\n\n",
        ),
        (
            "z_",
            True,
            "@property\ndef z(self) -> bool:\n    return self.z_\n\n",
        ),
        ("_x", False, "def get_x(self) -> int:\n    return self._x\n\n"),
        ("y", False, "def get_y(self) -> float:\n    return self.y\n\n"),
        ("z_", False, "def get_z(self) -> bool:\n    return self.z_\n\n"),
    ],
)
def test_get_getter(
    get_instance: ClassInspector, item: str, use_properties: bool, result: str
) -> None:
    get_instance.use_properties = use_properties
    assert get_instance.get_getter(item) == result


# def test_get_init_setter(get_instance: ClassInspector) -> None:
#     assert get_instance.get_init_setter() ==


# def test_get_init_setters(get_instance: ClassInspector) -> None:
#     assert get_instance.get_init_setters() ==


@pytest.mark.parametrize(
    "item, result",
    [
        ("_x", int),
        ("y", float),
        ("z_", bool),
    ],
)
def test_get_item_type(
    get_instance: ClassInspector, item: str, result
) -> None:
    assert get_instance.get_item_type(item) == result.__name__


# def test_get_methods_docstrings(get_instance: ClassInspector) -> None:
#     assert get_instance.get_methods_docstrings() ==


# def test_get_primary_methods(get_instance: ClassInspector) -> None:
#     assert get_instance.get_primary_methods() ==


@pytest.mark.parametrize(
    "item, use_properties, result",
    [
        (
            "_x",
            True,
            "@x.setter\ndef x(self, x: int) -> None:\n    self._x: int = x\n",
        ),
        (
            "y",
            True,
            "@y.setter\ndef y(self, y: float) -> None:\n    self._y: float = y\n",
        ),
        (
            "z_",
            True,
            "@z.setter\ndef z(self, z: bool) -> None:\n    self.z_: bool = z\n",
        ),
        (
            "_x",
            False,
            "def set_x(self, x: int) -> None:\n    self._x: int = x\n",
        ),
        (
            "y",
            False,
            "def set_y(self, y: float) -> None:\n    self.y: float = y\n",
        ),
        (
            "z_",
            False,
            "def set_z(self, z: bool) -> None:\n    self.z_: bool = z\n",
        ),
    ],
)
def test_get_setter(
    get_instance: ClassInspector, item: str, use_properties: bool, result: str
) -> None:
    get_instance.use_properties = use_properties
    assert get_instance.get_setter(item) == result


# def test_get_setter_getter_methods(get_instance: ClassInspector) -> None:
#     assert get_instance.get_setter_getter_methods() ==


@pytest.mark.parametrize(
    "item, result",
    [("test", False), ("_test", False), ("test_", True), ("__test__", False)],
)
def test_is_derived(
    get_instance: ClassInspector, item: str, result: bool
) -> None:
    assert get_instance.is_derived(item) == result


@pytest.mark.parametrize(
    "item, result",
    [
        ("_x", False),
        ("y", False),
        ("z_", False),
        ("_do_something_internally", True),
        ("do_something", True),
        ("do_something_derived_", True),
    ],
)
def test_is_method(
    get_instance: ClassInspector, item: str, result: bool
) -> None:
    assert get_instance.is_method(item) == result


@pytest.mark.parametrize(
    "item, result",
    [("test", True), ("_test", True), ("test_", True), ("__test__", False)],
)
def test_is_not_dunder(
    get_instance: ClassInspector, item: str, result: bool
) -> None:
    assert get_instance.is_not_dunder(item) == result


@pytest.mark.parametrize(
    "item, result",
    [("test", False), ("_test", True), ("test_", False), ("__test__", False)],
)
def test_is_private(
    get_instance: ClassInspector, item: str, result: bool
) -> None:
    assert get_instance.is_private(item) == result


@pytest.mark.parametrize(
    "item, result",
    [("test", True), ("_test", False), ("test_", False), ("__test__", False)],
)
def test_is_public(
    get_instance: ClassInspector, item: str, result: bool
) -> None:
    assert get_instance.is_public(item) == result


@pytest.mark.parametrize(
    "item, result",
    [
        ("test", "test"),
        ("_test", "test"),
        ("test_", "test"),
        ("__test__", "test"),
    ],
)
def test_strip_underscores(
    get_instance: ClassInspector, item: str, result: str
) -> None:
    assert get_instance.strip_underscores(item) == result
