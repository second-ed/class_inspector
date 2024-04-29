import pytest
from class_inspector.attr_generator import ITERABLES, MAPPINGS, AttrGenerator


@pytest.mark.parametrize(
    "attr_type, expected_result",
    [
        ("List[str]", True),
        ("str", False),
    ],
)
def test_values_contains_square_brackets(
    get_attr_gen_instance: AttrGenerator, attr_type, expected_result
) -> None:
    assert (
        get_attr_gen_instance.contains_square_brackets(attr_type)
        == expected_result
    )


# @pytest.mark.parametrize(
#     "attr_type",
#     [
#         (3.25),
#     ]
# )
# def test_types_contains_square_brackets(get_attr_gen_instance: AttrGenerator, attr_type) -> None:
#     with pytest.raises(TypeError):
#         get_attr_gen_instance.contains_square_brackets(attr_type)


def test_values_get_attr_class(get_attr_gen_instance: AttrGenerator) -> None:
    assert get_attr_gen_instance.get_attr_class() == (
        "import attr\nfrom attr.validators import instance_of, "
        "deep_iterable, deep_mapping\n\n\n@attr.define\nclass TestClass:\n    "
        "test1: int = attr.ib(validator=[instance_of(int)])\n    "
        "test2: float = attr.ib(validator=[instance_of(float)], init=False)\n    "
        "test3: bool = attr.ib(validator=[instance_of(bool)])\n    "
        "test4: str = attr.ib(validator=[instance_of(str)], init=False)\n    "
        "test5: list = attr.ib(validator=[deep_iterable(member_validator=instance_of(int), "
        "iterable_validator=instance_of(list))])\n    "
        "test6: dict = attr.ib(validator=[deep_mapping(key_validator=instance_of(str), "
        "value_validator=instance_of(float), mapping_validator=instance_of(dict))], init=False)"
    )


@pytest.mark.parametrize(
    "attr_name, attr_type, attr_init, expected_result",
    [
        (
            "test1",
            "int",
            True,
            "    test1: int = attr.ib(validator=[instance_of(int)])",
        ),
        (
            "test5",
            "List[int]",
            True,
            "    test5: list = attr.ib(validator=[deep_iterable(member_validator=instance_of(int), iterable_validator=instance_of(list))])",
        ),
        (
            "test6",
            "Dict[str, float]",
            False,
            "    test6: dict = attr.ib(validator=[deep_mapping(key_validator=instance_of(str), value_validator=instance_of(float), mapping_validator=instance_of(dict))], init=False)",
        ),
    ],
)
def test_values_get_attrib(
    get_attr_gen_instance: AttrGenerator,
    attr_name,
    attr_type,
    attr_init,
    expected_result,
) -> None:
    assert (
        get_attr_gen_instance.get_attrib(attr_name, attr_type, attr_init)
        == expected_result
    )


# @pytest.mark.parametrize(
#     "attr_name, attr_type, attr_init",
#     [
#         ("test", "case", []),
#         ("test", 3, True),
#         (0.0, "case", False),
#     ]
# )
# def test_types_get_attrib(get_attr_gen_instance: AttrGenerator, attr_name, attr_type, attr_init) -> None:
#     with pytest.raises(TypeError):
#         get_attr_gen_instance.get_attrib(attr_name, attr_type, attr_init)


def test_values_get_class_sig(get_attr_gen_instance: AttrGenerator) -> None:
    assert (
        get_attr_gen_instance.get_class_sig()
        == "@attr.define\nclass TestClass:"
    )


@pytest.mark.parametrize(
    "attr_type, expected_result",
    [
        (
            "List[str]",
            "deep_iterable(member_validator=instance_of(str), iterable_validator=instance_of(list))",
        ),
        (
            "Tuple[float]",
            "deep_iterable(member_validator=instance_of(float), iterable_validator=instance_of(tuple))",
        ),
        (
            "Set[int]",
            "deep_iterable(member_validator=instance_of(int), iterable_validator=instance_of(set))",
        ),
    ],
)
def test_values_get_deep_iterable(
    get_attr_gen_instance: AttrGenerator, attr_type, expected_result
) -> None:
    assert (
        get_attr_gen_instance.get_deep_iterable(attr_type) == expected_result
    )


# @pytest.mark.parametrize(
#     "attr_type",
#     [
#         (1),
#     ]
# )
# def test_types_get_deep_iterable(get_attr_gen_instance: AttrGenerator, attr_type) -> None:
#     with pytest.raises(TypeError):
#         get_attr_gen_instance.get_deep_iterable(attr_type)


@pytest.mark.parametrize(
    "attr_type, expected_result",
    [
        (
            "Dict[str, int]",
            "deep_mapping(key_validator=instance_of(str), value_validator=instance_of(int), mapping_validator=instance_of(dict))",
        ),
        (
            "Dict[int, float]",
            "deep_mapping(key_validator=instance_of(int), value_validator=instance_of(float), mapping_validator=instance_of(dict))",
        ),
    ],
)
def test_values_get_deep_mapping(
    get_attr_gen_instance: AttrGenerator, attr_type, expected_result
) -> None:
    assert get_attr_gen_instance.get_deep_mapping(attr_type) == expected_result


# @pytest.mark.parametrize(
#     "attr_type",
#     [
#         (0),
#     ]
# )
# def test_types_get_deep_mapping(get_attr_gen_instance: AttrGenerator, attr_type) -> None:
#     with pytest.raises(TypeError):
#         get_attr_gen_instance.get_deep_mapping(attr_type)


def test_values_get_imports(get_attr_gen_instance: AttrGenerator) -> None:
    assert (
        get_attr_gen_instance.get_imports()
        == "import attr\nfrom attr.validators import instance_of, deep_iterable, deep_mapping\n\n"
    )


@pytest.mark.parametrize(
    "attr_init, expected_result",
    [
        (True, ""),
        (False, ", init=False"),
    ],
)
def test_values_get_init_bool(
    get_attr_gen_instance: AttrGenerator, attr_init, expected_result
) -> None:
    assert get_attr_gen_instance.get_init_bool(attr_init) == expected_result


# @pytest.mark.parametrize(
#     "attr_init",
#     [
#         ("test"),
#     ]
# )
# def test_types_get_init_bool(get_attr_gen_instance: AttrGenerator, attr_init) -> None:
#     with pytest.raises(TypeError):
#         get_attr_gen_instance.get_init_bool(attr_init)


@pytest.mark.parametrize(
    "attr_type, expected_result",
    [
        ("List[str]", ("str", "list")),
        ("Tuple[float]", ("float", "tuple")),
    ],
)
def test_values_get_inner_outer_types(
    get_attr_gen_instance: AttrGenerator, attr_type, expected_result
) -> None:
    assert (
        get_attr_gen_instance.get_inner_outer_types(attr_type)
        == expected_result
    )


# @pytest.mark.parametrize(
#     "attr_type",
#     [
#         (0.0),
#     ]
# )
# def test_types_get_inner_outer_types(get_attr_gen_instance: AttrGenerator, attr_type) -> None:
#     with pytest.raises(TypeError):
#         get_attr_gen_instance.get_inner_outer_types(attr_type)


@pytest.mark.parametrize(
    "attr_type, expected_result",
    [
        ("int", "int"),
        ("float", "float"),
        ("List[str]", "list"),
        ("Tuple[float]", "tuple"),
    ],
)
def test_values_get_type_hint(
    get_attr_gen_instance: AttrGenerator, attr_type, expected_result
) -> None:
    assert get_attr_gen_instance.get_type_hint(attr_type) == expected_result


# @pytest.mark.parametrize(
#     "attr_type",
#     [
#         ({}),
#     ]
# )
# def test_types_get_type_hint(get_attr_gen_instance: AttrGenerator, attr_type) -> None:
#     with pytest.raises(TypeError):
#         get_attr_gen_instance.get_type_hint(attr_type)


@pytest.mark.parametrize(
    "attr_type, expected_result",
    [
        ("int", "instance_of(int)"),
        ("float", "instance_of(float)"),
        (
            "List[str]",
            "deep_iterable(member_validator=instance_of(str), iterable_validator=instance_of(list))",
        ),
        (
            "Tuple[float]",
            "deep_iterable(member_validator=instance_of(float), iterable_validator=instance_of(tuple))",
        ),
    ],
)
def test_values_get_validator(
    get_attr_gen_instance: AttrGenerator, attr_type, expected_result
) -> None:
    assert get_attr_gen_instance.get_validator(attr_type) == expected_result


# @pytest.mark.parametrize(
#     "attr_type",
#     [
#         (str),
#     ]
# )
# def test_types_get_validator(get_attr_gen_instance: AttrGenerator, attr_type) -> None:
#     with pytest.raises(TypeError):
#         get_attr_gen_instance.get_validator(attr_type)


@pytest.mark.parametrize(
    "attr_type, expected_result",
    [
        ("int", False),
        ("float", False),
        ("List[str]", True),
        ("Tuple[float]", True),
    ],
)
def test_values_is_deep_iterable(
    get_attr_gen_instance: AttrGenerator, attr_type, expected_result
) -> None:
    assert get_attr_gen_instance.is_deep_iterable(attr_type) == expected_result


# @pytest.mark.parametrize(
#     "attr_type",
#     [
#         (str),
#     ]
# )
# def test_types_is_deep_iterable(get_attr_gen_instance: AttrGenerator, attr_type) -> None:
#     with pytest.raises(TypeError):
#         get_attr_gen_instance.is_deep_iterable(attr_type)


@pytest.mark.parametrize(
    "attr_type, expected_result",
    [
        ("int", False),
        ("float", False),
        ("List[str]", False),
        ("Tuple[float]", False),
        ("Dict[str, str]", True),
    ],
)
def test_values_is_deep_mapping(
    get_attr_gen_instance: AttrGenerator, attr_type, expected_result
) -> None:
    assert get_attr_gen_instance.is_deep_mapping(attr_type) == expected_result


# @pytest.mark.parametrize(
#     "attr_type",
#     [
#         (str),
#     ]
# )
# def test_types_is_deep_mapping(get_attr_gen_instance: AttrGenerator, attr_type) -> None:
#     with pytest.raises(TypeError):
#         get_attr_gen_instance.is_deep_mapping(attr_type)


@pytest.mark.parametrize(
    "attr_type, deep_list, expected_result",
    [
        ("List[str]", ITERABLES, True),
        ("Tuple[float]", ITERABLES, True),
        ("Dict[str, str]", ITERABLES, False),
        ("List[str]", MAPPINGS, False),
        ("Tuple[float]", MAPPINGS, False),
        ("Dict[str, str]", MAPPINGS, True),
    ],
)
def test_values_is_outer_type_in_list(
    get_attr_gen_instance: AttrGenerator, attr_type, deep_list, expected_result
) -> None:
    assert (
        get_attr_gen_instance.is_outer_type_in_list(attr_type, deep_list)
        == expected_result
    )


# @pytest.mark.parametrize(
#     "attr_type, deep_list",
#     [
#         (str, List),
#         (str, List),
#     ]
# )
# def test_types_is_outer_type_in_list(get_attr_gen_instance: AttrGenerator, attr_type, deep_list) -> None:
#     with pytest.raises(TypeError):
#         get_attr_gen_instance.is_outer_type_in_list(attr_type, deep_list)
