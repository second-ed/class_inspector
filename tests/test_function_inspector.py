from contextlib import nullcontext as does_not_raise
from typing import Callable, Optional

import pytest
from class_inspector.function_inspector import FunctionInspector

from tests.mock_package.mock_module import (
    MockClass,
    mock_function,
    mock_function_with_optional,
)


@pytest.fixture
def get_mock_function() -> Callable:
    return mock_function


@pytest.fixture
def get_mock_function_with_optional() -> Callable:
    return mock_function_with_optional


@pytest.fixture
def get_mock_method() -> Callable:
    return MockClass().mock_method


@pytest.fixture
def get_instance() -> FunctionInspector:
    return FunctionInspector()


@pytest.mark.parametrize(
    "fixture_name, func_name, params, return_annot, is_method",
    [
        (
            "get_mock_function",
            "mock_function",
            {
                "param1": float,
                "param2": int,
                "param3": bool,
                "param4": str,
            },
            ["float"],
            0,
        ),
        (
            "get_mock_method",
            "mock_method",
            {
                "a": int,
                "b": str,
            },
            ["str"],
            1,
        ),
        (
            "get_mock_function_with_optional",
            "mock_function_with_optional",
            {
                "param1": bool,
                "param2": Optional[int],
            },
            ["Optional[int]", "Union[int, NoneType]"],
            0,
        ),
    ],
)
def test_analyse(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    func_name,
    params,
    return_annot,
    is_method,
) -> None:
    func = request.getfixturevalue(fixture_name)
    get_instance.analyse(func)
    assert get_instance.obj == func
    assert get_instance.name == func_name
    assert get_instance.parameters == params
    assert get_instance.return_annotation in return_annot
    assert get_instance.is_method == is_method


@pytest.mark.parametrize(
    "fixture_name, expected_result, expected_context",
    [
        ("get_mock_function", "mock_function", does_not_raise()),
        ("get_mock_method", "MockClass", does_not_raise()),
        (
            "get_mock_function_with_optional",
            "mock_function_with_optional",
            does_not_raise(),
        ),
    ],
)
def test_get_class_name(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert get_instance._get_class_name() == expected_result


@pytest.mark.parametrize(
    "fixture_name, expected_result, expected_context",
    [
        (
            "get_mock_function",
            (
                "    if not all([isinstance(param1, float), isinstance(param2, int), isinstance(param3, bool), isinstance(param4, str)]):\n"
                "        raise TypeError(\n"
                '            "mock_function expects arg types: [float, int, bool, str], "\n'
                '            f"received: [{type(param1).__name__}, {type(param2).__name__}, {type(param3).__name__}, {type(param4).__name__}]"\n'
                "        )\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_method",
            (
                "        if not all([isinstance(a, int), isinstance(b, str)]):\n"
                "            raise TypeError(\n"
                '                "mock_method expects arg types: [int, str], "\n'
                '                f"received: [{type(a).__name__}, {type(b).__name__}]"\n'
                "            )\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_function_with_optional",
            (
                "    if not all([isinstance(param1, bool), isinstance(param2, (int, NoneType))]):\n"
                "        raise TypeError(\n"
                '            "mock_function_with_optional expects arg types: [bool, (int, NoneType)], "\n'
                '            f"received: [{type(param1).__name__}, {type(param2).__name__}]"\n'
                "        )\n"
            ),
            does_not_raise(),
        ),
    ],
)
def test_get_guards(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert get_instance._get_guards() == expected_result


@pytest.mark.parametrize(
    "fixture_name, expected_result, expected_context",
    [
        (
            "get_mock_function",
            "mock_function(param1, param2, param3, param4) ",
            does_not_raise(),
        ),
        (
            "get_mock_method",
            "get_mock_class.mock_method(a, b) ",
            does_not_raise(),
        ),
        (
            "get_mock_function_with_optional",
            "mock_function_with_optional(param1, param2) ",
            does_not_raise(),
        ),
    ],
)
def test_get_instance_call(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert get_instance._get_instance_call() == expected_result


@pytest.mark.parametrize(
    "fixture_name, expected_result, expected_context",
    [
        ("get_mock_function", "", does_not_raise()),
        ("get_mock_method", "get_mock_class: MockClass, ", does_not_raise()),
    ],
)
def test_get_instance_sig(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert get_instance._get_instance_sig() == expected_result


@pytest.mark.parametrize(
    "fixture_name, check_types, match, expected_result, expected_context",
    [
        (
            "get_mock_function",
            True,
            False,
            (
                "@pytest.mark.parametrize(\n"
                '    "param1, param2, param3, param4, expected_result, expected_context",\n'
                "    [\n"
                "        (param1, param2, param3, param4, expected_result, expected_context),\n"
                "        (param1, param2, param3, param4, None, pytest.raises(TypeError)),\n"
                "        (param1, param2, param3, param4, None, pytest.raises(TypeError)),\n"
                "        (param1, param2, param3, param4, None, pytest.raises(TypeError)),\n"
                "        (param1, param2, param3, param4, None, pytest.raises(TypeError)),\n"
                "    ]\n)\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_function",
            True,
            True,
            (
                "@pytest.mark.parametrize(\n"
                '    "param1, param2, param3, param4, expected_result, expected_context",\n'
                "    [\n"
                "        (param1, param2, param3, param4, expected_result, expected_context),\n"
                '        (param1, param2, param3, param4, None, pytest.raises(TypeError, match=r"")),\n'
                '        (param1, param2, param3, param4, None, pytest.raises(TypeError, match=r"")),\n'
                '        (param1, param2, param3, param4, None, pytest.raises(TypeError, match=r"")),\n'
                '        (param1, param2, param3, param4, None, pytest.raises(TypeError, match=r"")),\n'
                "    ]\n)\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_function",
            False,
            True,
            (
                "@pytest.mark.parametrize(\n"
                '    "param1, param2, param3, param4, expected_result, expected_context",\n'
                "    [\n"
                "        (param1, param2, param3, param4, expected_result, expected_context),\n"
                "    ]\n)\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_method",
            True,
            False,
            (
                "@pytest.mark.parametrize(\n"
                '    "a, b, expected_result, expected_context",\n    [\n'
                "        (a, b, expected_result, expected_context),\n"
                "        (a, b, None, pytest.raises(TypeError)),\n"
                "        (a, b, None, pytest.raises(TypeError)),\n"
                "    ]\n)\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_method",
            False,
            False,
            (
                "@pytest.mark.parametrize(\n"
                '    "a, b, expected_result, expected_context",\n    [\n'
                "        (a, b, expected_result, expected_context),\n"
                "    ]\n)\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_function_with_optional",
            True,
            False,
            (
                "@pytest.mark.parametrize(\n"
                '    "param1, param2, expected_result, expected_context",\n    [\n'
                "        (param1, param2, expected_result, expected_context),\n"
                "        (param1, param2, None, pytest.raises(TypeError)),\n"
                "        (param1, param2, None, pytest.raises(TypeError)),\n"
                "    ]\n)\n"
            ),
            does_not_raise(),
        ),
    ],
)
def test_get_parametrize_decorator(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    check_types,
    match,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert (
            get_instance._get_parametrize_decorator(check_types, match)
            == expected_result
        )


@pytest.mark.parametrize(
    "fixture_name, expected_result, expected_context",
    [
        (
            "get_mock_function",
            "param1, param2, param3, param4",
            does_not_raise(),
        ),
        (
            "get_mock_method",
            "a, b",
            does_not_raise(),
        ),
        (
            "get_mock_function_with_optional",
            "param1, param2",
            does_not_raise(),
        ),
    ],
)
def test_get_params_str(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert get_instance._get_params_str() == expected_result


@pytest.mark.parametrize(
    "fixture_name, expected_result, expected_context",
    [
        ("get_mock_function", "float", does_not_raise()),
        ("get_mock_method", "str", does_not_raise()),
    ],
)
def test_get_return_annotations(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert get_instance._get_return_annotations() == expected_result


@pytest.mark.parametrize(
    "fixture_name, check_types, match, expected_result, expected_context",
    [
        (
            "get_mock_function",
            True,
            False,
            (
                "@pytest.mark.parametrize(\n"
                '    "param1, param2, param3, param4, expected_result, expected_context",\n'
                "    [\n"
                "        (param1, param2, param3, param4, expected_result, expected_context),\n"
                "        (param1, param2, param3, param4, None, pytest.raises(TypeError)),\n"
                "        (param1, param2, param3, param4, None, pytest.raises(TypeError)),\n"
                "        (param1, param2, param3, param4, None, pytest.raises(TypeError)),\n"
                "        (param1, param2, param3, param4, None, pytest.raises(TypeError)),\n"
                "    ]\n)\n"
                "def test_mock_function(param1, param2, param3, param4, expected_result, expected_context) -> None:\n"
                "    with expected_context:\n"
                "        assert mock_function(param1, param2, param3, param4) == expected_result\n\n\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_function",
            True,
            True,
            (
                "@pytest.mark.parametrize(\n"
                '    "param1, param2, param3, param4, expected_result, expected_context",\n'
                "    [\n"
                "        (param1, param2, param3, param4, expected_result, expected_context),\n"
                '        (param1, param2, param3, param4, None, pytest.raises(TypeError, match=r"")),\n'
                '        (param1, param2, param3, param4, None, pytest.raises(TypeError, match=r"")),\n'
                '        (param1, param2, param3, param4, None, pytest.raises(TypeError, match=r"")),\n'
                '        (param1, param2, param3, param4, None, pytest.raises(TypeError, match=r"")),\n'
                "    ]\n)\n"
                "def test_mock_function(param1, param2, param3, param4, expected_result, expected_context) -> None:\n"
                "    with expected_context:\n"
                "        assert mock_function(param1, param2, param3, param4) == expected_result\n\n\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_function",
            False,
            True,
            (
                "@pytest.mark.parametrize(\n"
                '    "param1, param2, param3, param4, expected_result, expected_context",\n'
                "    [\n"
                "        (param1, param2, param3, param4, expected_result, expected_context),\n"
                "    ]\n)\n"
                "def test_mock_function(param1, param2, param3, param4, expected_result, expected_context) -> None:\n"
                "    with expected_context:\n"
                "        assert mock_function(param1, param2, param3, param4) == expected_result\n\n\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_method",
            True,
            False,
            (
                "@pytest.mark.parametrize(\n"
                '    "a, b, expected_result, expected_context",\n    [\n'
                "        (a, b, expected_result, expected_context),\n"
                "        (a, b, None, pytest.raises(TypeError)),\n"
                "        (a, b, None, pytest.raises(TypeError)),\n"
                "    ]\n)\n"
                "def test_mock_method(get_mock_class: MockClass, a, b, expected_result, expected_context) -> None:\n"
                "    with expected_context:\n"
                "        assert get_mock_class.mock_method(a, b) == expected_result\n\n\n"
            ),
            does_not_raise(),
        ),
    ],
)
def test_get_test(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    check_types,
    match,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert get_instance.get_test(check_types, match) == expected_result


@pytest.mark.parametrize(
    "fixture_name, expected_result, expected_context",
    [
        (
            "get_mock_function",
            "    with expected_context:\n"
            "        assert mock_function(param1, param2, param3, param4) == expected_result\n",
            does_not_raise(),
        ),
        (
            "get_mock_method",
            "    with expected_context:\n"
            "        assert get_mock_class.mock_method(a, b) == expected_result\n",
            does_not_raise(),
        ),
    ],
)
def test_get_test_body(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert get_instance._get_test_body() == expected_result


@pytest.mark.parametrize(
    "fixture_name, expected_result, expected_context",
    [
        (
            "get_mock_function",
            "def test_mock_function(param1, param2, param3, param4, expected_result, expected_context) -> None:\n",
            does_not_raise(),
        ),
        (
            "get_mock_method",
            "def test_mock_method(get_mock_class: MockClass, a, b, expected_result, expected_context) -> None:\n",
            does_not_raise(),
        ),
    ],
)
def test_get_test_sig(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert get_instance._get_test_sig() == expected_result


@pytest.mark.parametrize(
    "fixture_name, expected_result, expected_context",
    [
        (
            "get_mock_function",
            [
                "def mock_function(param1: float, param2: int, param3: bool, param4: str = 'test') -> float:"
            ],
            does_not_raise(),
        ),
        (
            "get_mock_method",
            ["    def mock_method(self, a: int, b: str) -> str:"],
            does_not_raise(),
        ),
        (
            "get_mock_function_with_optional",
            [
                "def mock_function_with_optional(param1: bool, param2: Optional[int]) -> Optional[int]:",
                "def mock_function_with_optional(param1: bool, param2: Union[int, NoneType]) -> Union[int, NoneType]:",
            ],
            does_not_raise(),
        ),
    ],
)
def test_get_func_sig(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert get_instance._get_func_sig() in expected_result


@pytest.mark.parametrize(
    "fixture_name, add_guards, add_debugs, expected_result, expected_context",
    [
        (
            "get_mock_function",
            True,
            True,
            (
                "def mock_function(param1: float, param2: int, param3: bool, param4: str = 'test') -> float:\n"
                "    for key, val in locals().items():\n"
                '        logger.debug(f"{key} = {val}")\n'
                "    if not all([isinstance(param1, float), isinstance(param2, int), isinstance(param3, bool), isinstance(param4, str)]):\n"
                "        raise TypeError(\n"
                '            "mock_function expects arg types: [float, int, bool, str], "\n'
                '            f"received: [{type(param1).__name__}, {type(param2).__name__}, {type(param3).__name__}, {type(param4).__name__}]"\n'
                "        )\n"
                "    if param3:\n"
                "        return param1 - param2\n"
                "    else:\n"
                "        return param1 + param2\n\n\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_function",
            False,
            True,
            (
                "def mock_function(param1: float, param2: int, param3: bool, param4: str = 'test') -> float:\n"
                "    for key, val in locals().items():\n"
                '        logger.debug(f"{key} = {val}")\n'
                "    if param3:\n"
                "        return param1 - param2\n"
                "    else:\n"
                "        return param1 + param2\n\n\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_function",
            True,
            False,
            (
                "def mock_function(param1: float, param2: int, param3: bool, param4: str = 'test') -> float:\n"
                "    if not all([isinstance(param1, float), isinstance(param2, int), isinstance(param3, bool), isinstance(param4, str)]):\n"
                "        raise TypeError(\n"
                '            "mock_function expects arg types: [float, int, bool, str], "\n'
                '            f"received: [{type(param1).__name__}, {type(param2).__name__}, {type(param3).__name__}, {type(param4).__name__}]"\n'
                "        )\n"
                "    if param3:\n"
                "        return param1 - param2\n"
                "    else:\n"
                "        return param1 + param2\n\n\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_method",
            False,
            False,
            (
                "    def mock_method(self, a: int, b: str) -> str:\n        return str(a) + b\n\n\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_method",
            True,
            False,
            (
                "    def mock_method(self, a: int, b: str) -> str:\n"
                "        if not all([isinstance(a, int), isinstance(b, str)]):\n"
                "            raise TypeError(\n"
                '                "mock_method expects arg types: [int, str], "\n'
                '                f"received: [{type(a).__name__}, {type(b).__name__}]"\n'
                "            )\n"
                "        return str(a) + b\n\n\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_method",
            True,
            True,
            (
                "    def mock_method(self, a: int, b: str) -> str:\n"
                "        for key, val in locals().items():\n"
                '            logger.debug(f"{key} = {val}")\n'
                "        if not all([isinstance(a, int), isinstance(b, str)]):\n"
                "            raise TypeError(\n"
                '                "mock_method expects arg types: [int, str], "\n'
                '                f"received: [{type(a).__name__}, {type(b).__name__}]"\n'
                "            )\n"
                "        return str(a) + b\n\n\n"
            ),
            does_not_raise(),
        ),
        (
            "get_mock_function_with_optional",
            True,
            True,
            (
                "def mock_function_with_optional(param1: bool, param2: Optional[int]) -> Optional[int]:\n"
                "    '''mock function with optional\n\n"
                "    Args:\n"
                "        param1 (bool)\n"
                "        param2 (Optional[int])\n\n"
                "    Returns:\n"
                "        Optional[int]\n"
                "    '''\n"
                "    for key, val in locals().items():\n"
                '        logger.debug(f"{key} = {val}")\n'
                "    if not all([isinstance(param1, bool), isinstance(param2, (int, NoneType))]):\n"
                "        raise TypeError(\n"
                '            "mock_function_with_optional expects arg types: [bool, (int, NoneType)], "\n'
                '            f"received: [{type(param1).__name__}, {type(param2).__name__}]"\n'
                "        )\n"
                "    if param1:\n"
                "        return param2\n"
                "    return None\n\n\n"
            ),
            does_not_raise(),
        ),
    ],
)
def test_add_boilerplate(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    add_guards,
    add_debugs,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert (
            get_instance.add_boilerplate(add_guards, add_debugs)
            == expected_result
        )
