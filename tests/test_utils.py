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


@pytest.mark.parametrize(
    "args, custom_exception, catch_exceptions, msg, expected_result, expected_context",
    [
        pytest.param(
            (2, "0"),
            ValueError,
            Exception,
            "no string args allowed",
            (
                None,
                ValueError(
                    {
                        "func": "div",
                        "args": (2, "0"),
                        "kwargs": {},
                        "caught_error": TypeError(
                            "unsupported operand type(s) for /: 'int' and 'str'"
                        ),
                        "msg": "no string args allowed",
                    }
                ),
            ),
            does_not_raise(),
            id="Ensure catches and transforms exception",
        ),
        pytest.param(
            (2, 1),
            ValueError,
            ZeroDivisionError,
            "no string args allowed",
            (2, None),
            does_not_raise(),
            id="Ensure catches and transforms exception",
        ),
    ],
)
def test_catch_raise(
    args, custom_exception, catch_exceptions, msg, expected_result, expected_context
):
    @utils.ExceptionLogger.catch_raise(custom_exception, catch_exceptions, msg)
    def div(a, b):
        return a / b

    with expected_context:
        res, err = div(*args)
        exp_res, exp_err = expected_result

        assert res == exp_res

        if err and exp_err:
            assert err.args[0]["func"] == exp_err.args[0]["func"]
            assert err.args[0]["args"] == exp_err.args[0]["args"]
            assert err.args[0]["kwargs"] == exp_err.args[0]["kwargs"]
            assert isinstance(
                err.args[0]["caught_error"], type(exp_err.args[0]["caught_error"])
            )
            assert err.args[0]["msg"] == exp_err.args[0]["msg"]
