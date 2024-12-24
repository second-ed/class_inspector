from contextlib import nullcontext as does_not_raise

import pytest

import class_inspector.create_tests as ct
from class_inspector.data_structures import FuncDetails, ParamDetails
from class_inspector.utils import format_code_str


@pytest.mark.parametrize(
    "funcs, expected_result, expected_context",
    [
        pytest.param(
            {
                "mock_function": FuncDetails(
                    name="mock_constant",
                    params={},
                    return_annot="bool",
                    raises=[],
                    class_name="",
                ),
                "mock_method": FuncDetails(
                    name="mock_method",
                    params={
                        "a": ParamDetails(name="a", annot="int", default=None),
                        "b": ParamDetails(name="b", annot="float", default="3.14"),
                    },
                    return_annot="list",
                    raises=["TypeError"],
                    class_name="MockClass",
                ),
            },
            'from contextlib import nullcontext as does_not_raise\n\nimport pytest\n\n\n@pytest.mark.parametrize(\n    "a, b, expected_result, expected_context",\n    [\n        pytest.param(\n            a, b, expected_result, does_not_raise(), id="Ensure x when `a` is y"\n        ),\n        pytest.param(\n            a, b, expected_result, does_not_raise(), id="Ensure x when `b` is y"\n        ),\n        pytest.param(a, b, None, pytest.raises(TypeError), id="Ensure raises `TypeError` if..."),\n    ],\n)\ndef test_mock_method(a, b, expected_result, expected_context):\n    with expected_context:\n        mock_class = MockClass()\n        assert mock_class.mock_method(a, b) == expected_result\n',
            does_not_raise(),
            id="Ensure returns tests for funcs with parameters when `funcs` is a mix of methods, functions and constants",
        )
    ],
)
def test_get_tests(funcs, expected_result, expected_context):
    with expected_context:
        assert format_code_str(ct.get_tests(funcs)) == format_code_str(expected_result)


@pytest.mark.parametrize(
    "func_details, test_raises, raises_arg_types, expected_result, expected_context",
    [
        pytest.param(
            FuncDetails(
                name="mock_function",
                params={
                    "a": ParamDetails(name="a", annot="int", default=None),
                    "b": ParamDetails(name="b", annot="float", default="3.14"),
                },
                return_annot="bool",
                raises=["ValueError"],
                class_name="",
            ),
            True,
            True,
            "@pytest.mark.parametrize(\n'a, b, expected_result, expected_context',\n[pytest.param(a, b, expected_result, does_not_raise(), id='Ensure x when `a` is y'),pytest.param(a, b, expected_result, does_not_raise(), id='Ensure x when `b` is y'),pytest.param(a, b, None, pytest.raises(ValueError), id='Ensure raises `ValueError` if...'),pytest.param(a, b, None, pytest.raises(TypeError), id='Ensure raises `TypeError` if given wrong type for `a`'),pytest.param(a, b, None, pytest.raises(TypeError), id='Ensure raises `TypeError` if given wrong type for `b`')])\ndef test_mock_function(a, b, expected_result, expected_context):\n    with expected_context:\n        assert mock_function(a, b) == expected_result\n\n",
            does_not_raise(),
            id="Ensure returns all raises cases when `func_details` is a function and raises options are True",
        ),
        pytest.param(
            FuncDetails(
                name="mock_method",
                params={
                    "a": ParamDetails(name="a", annot="int", default=None),
                    "b": ParamDetails(name="b", annot="float", default="3.14"),
                },
                return_annot="list",
                raises=["TypeError"],
                class_name="MockClass",
            ),
            False,
            False,
            "@pytest.mark.parametrize(\n'a, b, expected_result, expected_context',\n[pytest.param(a, b, expected_result, does_not_raise(), id='Ensure x when `a` is y'),pytest.param(a, b, expected_result, does_not_raise(), id='Ensure x when `b` is y')])\ndef test_mock_method(a, b, expected_result, expected_context):\n    with expected_context:\n        mock_class = MockClass()\n        assert mock_class.mock_method(a, b) == expected_result\n\n",
            does_not_raise(),
            id="Ensure returns simple cases when `func_details` is a method and raises options are False",
        ),
    ],
)
def test_get_test(
    func_details, test_raises, raises_arg_types, expected_result, expected_context
):
    with expected_context:
        assert format_code_str(
            ct._get_test(func_details, test_raises, raises_arg_types)
        ) == format_code_str(expected_result)


@pytest.mark.parametrize(
    "args, test_arg, raises_error, raises_arg_types, expected_result, expected_context",
    [
        pytest.param(
            "a, b",
            "a",
            "",
            False,
            "pytest.param(a, b, expected_result, does_not_raise(), id='Ensure x when `a` is y')",
            does_not_raise(),
            id="Ensure returns standard param",
        ),
        pytest.param(
            "a, b",
            "b",
            "",
            False,
            "pytest.param(a, b, expected_result, does_not_raise(), id='Ensure x when `b` is y')",
            does_not_raise(),
            id="Ensure id changes when `test_arg` is `b`",
        ),
        pytest.param(
            "a, b",
            "b",
            "ValueError",
            False,
            "pytest.param(a, b, None, pytest.raises(ValueError), id='Ensure raises `ValueError` if...')",
            does_not_raise(),
            id="Ensure returns raises error when `raises_error` is `ValueError`",
        ),
        pytest.param(
            "a, b",
            "a",
            "ValueError",
            True,
            "pytest.param(a, b, None, pytest.raises(TypeError), id='Ensure raises `TypeError` if given wrong type for `a`')",
            does_not_raise(),
            id="Ensure returns type check error when `raises_arg_types` is True",
        ),
    ],
)
def test_get_test_case(
    args, test_arg, raises_error, raises_arg_types, expected_result, expected_context
):
    with expected_context:
        assert (
            ct._get_test_case(args, test_arg, raises_error, raises_arg_types)
            == expected_result
        )
