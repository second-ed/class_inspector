from __future__ import annotations

from typing import Dict

from class_inspector.data_structures import FuncDetails
from class_inspector.utils import camel_to_snake, format_code_str


def get_tests(
    funcs: Dict[str, FuncDetails],
    test_raises: bool = True,
    raises_arg_types: bool = False,
) -> str:
    tests_str = [
        "from contextlib import nullcontext as does_not_raise",
        "import pytest",
    ]
    for func in funcs.values():
        if func.params:
            tests_str.append(_get_test(func, test_raises, raises_arg_types))

    return format_code_str("\n".join(tests_str))


def _get_test(
    func_details: FuncDetails, test_raises: bool = True, raises_arg_types: bool = False
) -> str:
    args_str = ", ".join(func_details.params.keys())
    test_cases = [
        _get_test_case(args_str, test_arg) for test_arg in func_details.params.keys()
    ]
    if test_raises:
        test_cases.extend(
            [
                _get_test_case(args_str, raises_error=raises)
                for raises in func_details.raises
            ]
        )

    if raises_arg_types:
        test_cases.extend(
            [
                _get_test_case(args_str, test_arg, raises_arg_types=True)
                for test_arg in func_details.params.keys()
            ],
        )

    std_name = func_details.name.strip("_")
    class_instance = (
        ""
        if not func_details.class_name
        else f"{camel_to_snake(func_details.class_name)} = {func_details.class_name}()"
    )
    func_call = (
        func_details.name
        if not func_details.class_name
        else f"{camel_to_snake(func_details.class_name)}.{func_details.name}"
    )
    test_cases = ",".join(test_cases)
    test_str = [
        "@pytest.mark.parametrize(",
        f"'{args_str}, expected_result, expected_context',",
        f"[{test_cases}])",
        f"def test_{std_name}({args_str}, expected_result, expected_context):",
        "    with expected_context:",
        f"        assert {func_call}({args_str}) == expected_result\n\n",
    ]

    if class_instance:
        test_str.insert(-1, f"        {class_instance}")

    return "\n".join(test_str)


def _get_test_case(
    args: str,
    test_arg: str = "",
    raises_error: str = "",
    raises_arg_types: bool = False,
) -> str:
    if raises_arg_types:
        return f"pytest.param({args}, None, pytest.raises(TypeError), id='Ensure raises `TypeError` if given wrong type for `{test_arg}`')"
    elif raises_error:
        return f"pytest.param({args}, None, pytest.raises({raises_error}), id='Ensure raises `{raises_error}` if...')"
    return f"pytest.param({args}, expected_result, does_not_raise(), id='Ensure x when `{test_arg}` is y')"
