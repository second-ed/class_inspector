from contextlib import nullcontext as does_not_raise

import pytest

import class_inspector.guard_conditions as gc


@pytest.mark.parametrize(
    "attr_type, expected_result, expected_context",
    [
        pytest.param(
            "int",
            "int",
            does_not_raise(),
            id="Ensure returns simple type when `attr_type` is simple type",
        ),
        pytest.param(
            "List[int]",
            ("int", "List"),
            does_not_raise(),
            id="Ensure returns inner and outer when `attr_type` is `List[int]`",
        ),
        pytest.param(
            "Dict[str, int]",
            ("str, int", "Dict"),
            does_not_raise(),
            id="Ensure returns compound inners and outer when `attr_type` is `Dict[str, int]`",
        ),
        pytest.param(
            "Optional[float]",
            ("float", "Optional"),
            does_not_raise(),
            id="Ensure returns inner and outer when `attr_type` contains `Optional`",
        ),
        pytest.param(
            0,
            None,
            pytest.raises(TypeError),
            id="Ensure raises `TypeError` if given wrong type",
        ),
    ],
)
def test_get_inner_outer_types(attr_type, expected_result, expected_context):
    with expected_context:
        assert gc.get_inner_outer_types(attr_type) == expected_result


@pytest.mark.parametrize(
    "attr_type, expected_result, expected_context",
    [
        pytest.param(
            "int",
            "int",
            does_not_raise(),
            id="Ensure x when `attr_type` is y",
        ),
        pytest.param(
            "List[int]",
            "List",
            does_not_raise(),
            id="Ensure x when `attr_type` is y",
        ),
        pytest.param(
            "Dict[str, int]",
            "Dict",
            does_not_raise(),
            id="Ensure x when `attr_type` is y",
        ),
        pytest.param(
            "Optional[float]",
            "(float, NoneType)",
            does_not_raise(),
            id="Ensure x when `attr_type` is y",
        ),
    ],
)
def test_get_isinstance_type(attr_type, expected_result, expected_context):
    with expected_context:
        assert gc.get_isinstance_type(attr_type) == expected_result


# @pytest.mark.parametrize(
#     "func_details, expected_result, expected_context",
#     [
#         pytest.param(
#             func_details,
#             expected_result,
#             does_not_raise(),
#             id="Ensure x when `func_details` is y",
#         )
#     ],
# )
# def test_get_guard_conditions(func_details, expected_result, expected_context):
#     with expected_context:
#         assert gc.get_guard_conditions(func_details) == expected_result
