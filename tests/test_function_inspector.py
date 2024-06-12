from contextlib import nullcontext as does_not_raise
from typing import Callable

import pytest
from class_inspector.function_inspector import FunctionInspector


class MockClass:
    def mock_method(self, a: int, b: str) -> str:
        return str(a) + b


def mock_function(
    param1: float, param2: int, param3: bool, param4: str = "test"
) -> float:
    if param3:
        return param1 - param2
    else:
        return param1 + param2


@pytest.fixture
def get_mock_function() -> Callable:
    return mock_function


@pytest.fixture
def get_mock_method() -> Callable:
    return MockClass().mock_method


@pytest.fixture
def get_instance() -> FunctionInspector:
    return FunctionInspector()


@pytest.mark.parametrize(
    "fixture_name, func_name, params, return_annot",
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
            "float",
        )
    ],
)
def test_analyse(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    func_name,
    params,
    return_annot,
) -> None:
    func = request.getfixturevalue(fixture_name)
    get_instance.analyse(func)
    assert get_instance.obj == func
    assert get_instance.name == func_name
    assert get_instance.parameters == params
    assert get_instance.return_annotation == return_annot


@pytest.mark.parametrize(
    "fixture_name, expected_result, expected_context",
    [
        ("get_mock_function", "mock_function", does_not_raise()),
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
        )
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
        ("get_mock_function", "float, int, bool, str", does_not_raise()),
    ],
)
def test_get_params_types(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert get_instance._get_params_types() == expected_result


@pytest.mark.parametrize(
    "fixture_name, expected_result, expected_context",
    [
        ("get_mock_function", "float", does_not_raise()),
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
    "fixture_name, item, expected_result, expected_context",
    [
        ("get_mock_function", "__test__", "test", does_not_raise()),
        ("get_mock_function", "_test", "test", does_not_raise()),
        ("get_mock_function", "test_", "test", does_not_raise()),
        ("get_mock_function", "__test", "test", does_not_raise()),
        ("get_mock_function", 0, "", pytest.raises(TypeError)),
    ],
)
def test_values_strip_underscores(
    request,
    get_instance: FunctionInspector,
    fixture_name,
    item,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        func = request.getfixturevalue(fixture_name)
        get_instance.analyse(func)
        assert get_instance._strip_underscores(item) == expected_result


@pytest.mark.parametrize(
    "fixture_name, expected_result, expected_context",
    [
        (
            "get_mock_function",
            "def mock_function(param1: float, param2: int, param3: bool, param4: str = 'test') -> float:",
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
        assert get_instance._get_func_sig() == expected_result


def test_get_docstring_patterns(get_instance: FunctionInspector) -> None:
    assert (
        get_instance._get_docstring_patterns()
        == "(\"\"\".*?\"\"\"\\n|'''.*?'''\\n)"
    )


@pytest.mark.parametrize(
    "func_str, pattern, expected_result, expected_context",
    [
        ("test (passing) case", r"\(\w+?\)", 14, does_not_raise()),
        # (func_str, pattern, None, pytest.raises(TypeError)),
        # (func_str, pattern, None, pytest.raises(TypeError)),
    ],
)
def test_find_string_end(
    get_instance: FunctionInspector,
    func_str,
    pattern,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_instance._find_string_end(func_str, pattern) == expected_result
        )


@pytest.mark.parametrize(
    "func_str, idx, to_insert, expected_result, expected_context",
    [
        ("test case", 5, "PASSED ", "test PASSED case", does_not_raise()),
        # (func_str, idx, to_insert, None, pytest.raises(TypeError)),
        # (func_str, idx, to_insert, None, pytest.raises(TypeError)),
        # (func_str, idx, to_insert, None, pytest.raises(TypeError)),
    ],
)
def test_insert_string_at_idx(
    get_instance: FunctionInspector,
    func_str,
    idx,
    to_insert,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        assert (
            get_instance._insert_string_at_idx(func_str, idx, to_insert)
            == expected_result
        )


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
