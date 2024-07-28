from contextlib import nullcontext as does_not_raise

import class_inspector._type_hint_utils as thu
import pytest


@pytest.mark.parametrize(
    "attr_type, expected_result, expected_context",
    [
        ("List[str]", True, does_not_raise()),
        ("str", False, does_not_raise()),
        (0, False, pytest.raises(TypeError)),
    ],
)
def test_contains_square_brackets(
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert thu.contains_square_brackets(attr_type) == expected_result


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
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert thu.get_inner_outer_types(attr_type) == expected_result


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
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert thu.get_type_hint(attr_type) == expected_result


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
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert thu.is_deep_iterable(attr_type) == expected_result


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
    attr_type,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert thu.is_deep_mapping(attr_type) == expected_result


@pytest.mark.parametrize(
    "attr_type, deep_list, expected_result, expected_context",
    [
        ("List[str]", thu.MAPPINGS, False, does_not_raise()),
        ("Set[float]", thu.MAPPINGS, False, does_not_raise()),
        ("Dict[str, str]", thu.MAPPINGS, True, does_not_raise()),
        ("List[str]", thu.ITERABLES, True, does_not_raise()),
        ("Set[float]", thu.ITERABLES, True, does_not_raise()),
        ("Dict[str, str]", thu.ITERABLES, False, does_not_raise()),
        ("int", [], False, pytest.raises(AttributeError)),
        (0, [], False, pytest.raises(TypeError)),
    ],
)
def test_is_outer_type_in_list(
    attr_type,
    deep_list,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            thu.is_outer_type_in_list(attr_type, deep_list) == expected_result
        )
