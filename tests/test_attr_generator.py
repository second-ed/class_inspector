from contextlib import nullcontext as does_not_raise

import pytest
from class_inspector.attr_generator import ITERABLES, MAPPINGS, AttrGenerator


@pytest.mark.parametrize(
    "attr_type, expected_result, expected_context",
    [
        ("List[str]", True, does_not_raise()),
        ("str", False, does_not_raise()),
        (0, False, pytest.raises(TypeError)),
    ],
)
def test_contains_square_brackets(
    get_attr_gen_instance: AttrGenerator,
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_attr_gen_instance.contains_square_brackets(attr_type)
            == expected_result
        )


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        (
            (
                "import attr\nfrom attr.validators import instance_of, deep_iterable,"
                " deep_mapping\n\n\n@attr.define\nclass TestClass:\n    "
                "test1: int = attr.ib(validator=[instance_of(int)])\n    "
                "test2: float = attr.ib(validator=[instance_of(float)], init=False)\n    "
                "test3: bool = attr.ib(validator=[instance_of(bool)])\n    "
                "test4: str = attr.ib(validator=[instance_of(str)], init=False)\n    "
                "test5: list = attr.ib(validator=[deep_iterable(member_validator=instance_of(int), "
                "iterable_validator=instance_of(list))])\n    "
                "test6: dict = attr.ib(validator=[deep_mapping(key_validator=instance_of(str), "
                "value_validator=instance_of(float), mapping_validator=instance_of(dict))], init=False)"
            ),
            does_not_raise(),
        ),
    ],
)
def test_get_attr_class(
    get_attr_gen_instance: AttrGenerator, expected_result, expected_context
) -> None:
    with expected_context:
        assert get_attr_gen_instance.get_attr_class() == expected_result


@pytest.mark.parametrize(
    "attr_name, attr_type, attr_init, expected_result, expected_context",
    [
        (
            "test",
            "str",
            True,
            "    test: str = attr.ib(validator=[instance_of(str)])",
            does_not_raise(),
        ),
        (
            "test2",
            "int",
            False,
            "    test2: int = attr.ib(validator=[instance_of(int)], init=False)",
            does_not_raise(),
        ),
        (
            0,
            "int",
            False,
            "",
            pytest.raises(TypeError),
        ),
        (
            "test2",
            0,
            False,
            "",
            pytest.raises(TypeError),
        ),
        (
            "test2",
            "str",
            0.0,
            "",
            pytest.raises(TypeError),
        ),
    ],
)
def test_get_attrib(
    get_attr_gen_instance: AttrGenerator,
    attr_name,
    attr_type,
    attr_init,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_attr_gen_instance.get_attrib(attr_name, attr_type, attr_init)
            == expected_result
        )


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        (
            "@attr.define\nclass TestClass:",
            does_not_raise(),
        ),
    ],
)
def test_get_class_sig(
    get_attr_gen_instance: AttrGenerator, expected_result, expected_context
) -> None:
    with expected_context:
        assert get_attr_gen_instance.get_class_sig() == expected_result


@pytest.mark.parametrize(
    "attr_type, expected_result, expected_context",
    [
        (
            "List[str]",
            "deep_iterable(member_validator=instance_of(str), iterable_validator=instance_of(list))",
            does_not_raise(),
        ),
        (
            "Set[float]",
            "deep_iterable(member_validator=instance_of(float), iterable_validator=instance_of(set))",
            does_not_raise(),
        ),
        (
            "Tuple[int]",
            "deep_iterable(member_validator=instance_of(int), iterable_validator=instance_of(tuple))",
            does_not_raise(),
        ),
        (0, "", pytest.raises(TypeError)),
    ],
)
def test_get_deep_iterable(
    get_attr_gen_instance: AttrGenerator,
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_attr_gen_instance.get_deep_iterable(attr_type)
            == expected_result
        )


@pytest.mark.parametrize(
    "attr_type, expected_result, expected_context",
    [
        (
            "Dict[str, int]",
            "deep_mapping(key_validator=instance_of(str), value_validator=instance_of(int), mapping_validator=instance_of(dict))",
            does_not_raise(),
        ),
        (
            "Dict[str, str]",
            "deep_mapping(key_validator=instance_of(str), value_validator=instance_of(str), mapping_validator=instance_of(dict))",
            does_not_raise(),
        ),
        (0, "", pytest.raises(TypeError)),
    ],
)
def test_get_deep_mapping(
    get_attr_gen_instance: AttrGenerator,
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_attr_gen_instance.get_deep_mapping(attr_type)
            == expected_result
        )


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        (
            (
                "import attr\nfrom attr.validators "
                "import instance_of, deep_iterable, deep_mapping\n\n"
            ),
            does_not_raise(),
        ),
    ],
)
def test_get_imports(
    get_attr_gen_instance: AttrGenerator, expected_result, expected_context
) -> None:
    with expected_context:
        assert get_attr_gen_instance.get_imports() == expected_result


@pytest.mark.parametrize(
    "attr_init, expected_result, expected_context",
    [
        (True, "", does_not_raise()),
        (False, ", init=False", does_not_raise()),
        (0, "", pytest.raises(TypeError)),
    ],
)
def test_get_init_bool(
    get_attr_gen_instance: AttrGenerator,
    attr_init,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_attr_gen_instance.get_init_bool(attr_init) == expected_result
        )


@pytest.mark.parametrize(
    "attr_type, expected_result, expected_context",
    [
        ("List[str]", ("str", "list"), does_not_raise()),
        ("Set[float]", ("float", "set"), does_not_raise()),
        ("Dict[str, str]", ("str, str", "dict"), does_not_raise()),
        ("int", "", pytest.raises(AttributeError)),
        (0, "", pytest.raises(TypeError)),
    ],
)
def test_get_inner_outer_types(
    get_attr_gen_instance: AttrGenerator,
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_attr_gen_instance.get_inner_outer_types(attr_type)
            == expected_result
        )


@pytest.mark.parametrize(
    "attr_type, expected_result, expected_context",
    [
        ("int", "int", does_not_raise()),
        ("str", "str", does_not_raise()),
        ("List[str]", "list", does_not_raise()),
        ("Set[float]", "set", does_not_raise()),
        ("Dict[str, str]", "dict", does_not_raise()),
        (0, "", pytest.raises(TypeError)),
    ],
)
def test_get_type_hint(
    get_attr_gen_instance: AttrGenerator,
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_attr_gen_instance.get_type_hint(attr_type) == expected_result
        )


@pytest.mark.parametrize(
    "attr_type, expected_result, expected_context",
    [
        ("int", "instance_of(int)", does_not_raise()),
        ("str", "instance_of(str)", does_not_raise()),
        (
            "List[str]",
            "deep_iterable(member_validator=instance_of(str), iterable_validator=instance_of(list))",
            does_not_raise(),
        ),
        (
            "Set[float]",
            "deep_iterable(member_validator=instance_of(float), iterable_validator=instance_of(set))",
            does_not_raise(),
        ),
        (
            "Dict[str, str]",
            "deep_mapping(key_validator=instance_of(str), value_validator=instance_of(str), mapping_validator=instance_of(dict))",
            does_not_raise(),
        ),
        (0, "", pytest.raises(TypeError)),
        ("some[thing]", "", pytest.raises(NotImplementedError)),
    ],
)
def test_get_validator(
    get_attr_gen_instance: AttrGenerator,
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_attr_gen_instance.get_validator(attr_type) == expected_result
        )


@pytest.mark.parametrize(
    "attr_type, expected_result, expected_context",
    [
        ("int", False, does_not_raise()),
        ("str", False, does_not_raise()),
        ("List[str]", True, does_not_raise()),
        ("Set[float]", True, does_not_raise()),
        ("Dict[str, str]", False, does_not_raise()),
        (0, False, pytest.raises(TypeError)),
    ],
)
def test_is_deep_iterable(
    get_attr_gen_instance: AttrGenerator,
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_attr_gen_instance.is_deep_iterable(attr_type)
            == expected_result
        )


@pytest.mark.parametrize(
    "attr_type, expected_result, expected_context",
    [
        ("int", False, does_not_raise()),
        ("str", False, does_not_raise()),
        ("List[str]", False, does_not_raise()),
        ("Set[float]", False, does_not_raise()),
        ("Dict[str, str]", True, does_not_raise()),
        (0, False, pytest.raises(TypeError)),
    ],
)
def test_is_deep_mapping(
    get_attr_gen_instance: AttrGenerator,
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_attr_gen_instance.is_deep_mapping(attr_type) == expected_result
        )


@pytest.mark.parametrize(
    "attr_type, deep_list, expected_result, expected_context",
    [
        ("List[str]", MAPPINGS, False, does_not_raise()),
        ("Set[float]", MAPPINGS, False, does_not_raise()),
        ("Dict[str, str]", MAPPINGS, True, does_not_raise()),
        ("List[str]", ITERABLES, True, does_not_raise()),
        ("Set[float]", ITERABLES, True, does_not_raise()),
        ("Dict[str, str]", ITERABLES, False, does_not_raise()),
        ("int", [], False, pytest.raises(AttributeError)),
        (0, [], False, pytest.raises(TypeError)),
    ],
)
def test_is_outer_type_in_list(
    get_attr_gen_instance: AttrGenerator,
    attr_type,
    deep_list,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_attr_gen_instance.is_outer_type_in_list(attr_type, deep_list)
            == expected_result
        )
