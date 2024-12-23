from contextlib import nullcontext as does_not_raise

import pytest

import class_inspector.utils as utils


@pytest.mark.parametrize(
    "input_str, expected_context",
    [
        pytest.param(
            "a == b  # a comment",
            does_not_raise(),
            id="Ensure no loss between conversions",
        )
    ],
)
def test_str_cst_conversions(input_str, expected_context):
    with expected_context:
        assert utils.cst_to_str(utils.str_to_cst(input_str)) == input_str


# @pytest.mark.parametrize(
#     "code_snippet, expected_result, expected_context",
#     [
#         pytest.param(
#             code_snippet,
#             expected_result,
#             does_not_raise(),
#             id="Ensure x when `code_snippet` is y",
#         )
#     ],
# )
# def test_format_code_str(code_snippet, expected_result, expected_context):
#     with expected_context:
#         assert utils.format_code_str(code_snippet) == expected_result


@pytest.mark.parametrize(
    "item, expected_result, expected_context",
    [
        pytest.param(
            "__init__",
            True,
            does_not_raise(),
            id="Ensure returns True when `item` is `__init__`",
        ),
        pytest.param(
            "some_method",
            False,
            does_not_raise(),
            id="Ensure returns False when `item` is `some_method`",
        ),
    ],
)
def test_is_dunder(item, expected_result, expected_context):
    with expected_context:
        assert utils.is_dunder(item) == expected_result


@pytest.mark.parametrize(
    "name, expected_result, expected_context",
    [
        pytest.param(
            "SomeClass",
            "some_class",
            does_not_raise(),
            id="Ensure returns `snake_case` when `name` is `CamelCase`",
        )
    ],
)
def test_camel_to_snake(name, expected_result, expected_context):
    with expected_context:
        assert utils.camel_to_snake(name) == expected_result
