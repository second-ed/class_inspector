from contextlib import nullcontext as does_not_raise

import pytest
from class_inspector.function_inspector import FunctionInspector


@pytest.fixture
def test_function(
    param1: float, param2: int, param3: bool, param4: str = "test"
) -> float:
    if param3:
        return param1 - param2
    else:
        return param1 + param2


@pytest.fixture
def get_instance() -> FunctionInspector:
    return FunctionInspector()


def test_analyse(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert get_instance.obj == test_function
    assert get_instance.name == "test_function"
    assert get_instance.parameters == {
        "param1": float,
        "param2": int,
        "param3": bool,
        "param4": str,
    }
    assert get_instance.return_annotation == "float"


@pytest.mark.parametrize(
    "func, expected_result, expected_context",
    [
        (test_function, "test_function", does_not_raise()),
    ],
)
def test_get_class_name(
    get_instance: FunctionInspector, func, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert get_instance._get_class_name() == expected_result


@pytest.mark.parametrize(
    "func, expected_result, expected_context",
    [
        (
            test_function,
            (
                "    if not all([isinstance(param1, float), isinstance(param2, int), isinstance(param3, bool), isinstance(param4, str)]):\n"
                "        raise TypeError(\n"
                '            "test_function expects arg types: [float, int, bool, str], "\n'
                '            f"received: [{type(param1).__name__}, {type(param2).__name__}, {type(param3).__name__}, {type(param4).__name__}]"\n'
                "        )\n"
            ),
            does_not_raise(),
        )
    ],
)
def test_get_guards(
    get_instance: FunctionInspector, func, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert get_instance._get_guards() == expected_result


@pytest.mark.parametrize(
    "func, expected_result, expected_context",
    [
        (
            test_function,
            "test_function(param1, param2, param3, param4) ",
            does_not_raise(),
        ),
    ],
)
def test_get_instance_call(
    get_instance: FunctionInspector, func, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert get_instance._get_instance_call() == expected_result


@pytest.mark.parametrize(
    "func, expected_result, expected_context",
    [
        (test_function, "", does_not_raise()),
    ],
)
def test_get_instance_sig(
    get_instance: FunctionInspector, func, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert get_instance._get_instance_sig() == expected_result


@pytest.mark.parametrize(
    "func, check_types, match, expected_result, expected_context",
    [
        (
            test_function,
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
            test_function,
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
            test_function,
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
    get_instance: FunctionInspector,
    func,
    check_types,
    match,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert (
            get_instance._get_parametrize_decorator(check_types, match)
            == expected_result
        )


@pytest.mark.parametrize(
    "func, expected_result, expected_context",
    [
        (test_function, "param1, param2, param3, param4", does_not_raise()),
    ],
)
def test_get_params_str(
    get_instance: FunctionInspector, func, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert get_instance._get_params_str() == expected_result


@pytest.mark.parametrize(
    "func, expected_result, expected_context",
    [
        (test_function, "float, int, bool, str", does_not_raise()),
    ],
)
def test_get_params_types(
    get_instance: FunctionInspector, func, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert get_instance._get_params_types() == expected_result


@pytest.mark.parametrize(
    "func, expected_result, expected_context",
    [
        (test_function, "float", does_not_raise()),
    ],
)
def test_get_return_annotations(
    get_instance: FunctionInspector, func, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert get_instance._get_return_annotations() == expected_result


@pytest.mark.parametrize(
    "func, check_types, match, expected_result, expected_context",
    [
        (
            test_function,
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
                "def test_test_function(param1, param2, param3, param4, expected_result, expected_context) -> None:\n"
                "    with expected_context:\n"
                "        assert test_function(param1, param2, param3, param4) == expected_result\n\n\n"
            ),
            does_not_raise(),
        ),
        (
            test_function,
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
                "def test_test_function(param1, param2, param3, param4, expected_result, expected_context) -> None:\n"
                "    with expected_context:\n"
                "        assert test_function(param1, param2, param3, param4) == expected_result\n\n\n"
            ),
            does_not_raise(),
        ),
        (
            test_function,
            False,
            True,
            (
                "@pytest.mark.parametrize(\n"
                '    "param1, param2, param3, param4, expected_result, expected_context",\n'
                "    [\n"
                "        (param1, param2, param3, param4, expected_result, expected_context),\n"
                "    ]\n)\n"
                "def test_test_function(param1, param2, param3, param4, expected_result, expected_context) -> None:\n"
                "    with expected_context:\n"
                "        assert test_function(param1, param2, param3, param4) == expected_result\n\n\n"
            ),
            does_not_raise(),
        ),
    ],
)
def test_get_test(
    get_instance: FunctionInspector,
    func,
    check_types,
    match,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert get_instance.get_test(check_types, match) == expected_result


@pytest.mark.parametrize(
    "func, expected_result, expected_context",
    [
        (
            test_function,
            "    with expected_context:\n"
            "        assert test_function(param1, param2, param3, param4) == expected_result\n",
            does_not_raise(),
        ),
    ],
)
def test_get_test_body(
    get_instance: FunctionInspector, func, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert get_instance._get_test_body() == expected_result


@pytest.mark.parametrize(
    "func, expected_result, expected_context",
    [
        (
            test_function,
            "def test_test_function(param1, param2, param3, param4, expected_result, expected_context) -> None:\n",
            does_not_raise(),
        ),
    ],
)
def test_get_test_sig(
    get_instance: FunctionInspector, func, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert get_instance._get_test_sig() == expected_result


@pytest.mark.parametrize(
    "func, item, expected_result, expected_context",
    [
        (test_function, "__test__", "test", does_not_raise()),
        (test_function, "_test", "test", does_not_raise()),
        (test_function, "test_", "test", does_not_raise()),
        (test_function, "__test", "test", does_not_raise()),
        (test_function, 0, "", pytest.raises(TypeError)),
    ],
)
def test_values_strip_underscores(
    get_instance: FunctionInspector,
    func,
    item,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert get_instance._strip_underscores(item) == expected_result


@pytest.mark.parametrize(
    "func, expected_result, expected_context",
    [
        (
            test_function,
            "def test_function(param1: float, param2: int, param3: bool, param4: str = 'test') -> float:",
            does_not_raise(),
        ),
    ],
)
def test_get_func_sig(
    get_instance: FunctionInspector, func, expected_result, expected_context
) -> None:
    with expected_context:
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
    "func, add_guards, add_debugs, expected_result, expected_context",
    [
        (
            test_function,
            True,
            True,
            (
                "@pytest.fixture\n"
                "def test_function(param1: float, param2: int, param3: bool, param4: str = 'test') -> float:\n"
                "    for k, v in locals().items():\n"
                '        logger.debug(f"{k} = {v}")\n'
                "    if not all([isinstance(param1, float), isinstance(param2, int), isinstance(param3, bool), isinstance(param4, str)]):\n"
                "        raise TypeError(\n"
                '            "test_function expects arg types: [float, int, bool, str], "\n'
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
            test_function,
            False,
            True,
            (
                "@pytest.fixture\n"
                "def test_function(param1: float, param2: int, param3: bool, param4: str = 'test') -> float:\n"
                "    for k, v in locals().items():\n"
                '        logger.debug(f"{k} = {v}")\n'
                "    if param3:\n"
                "        return param1 - param2\n"
                "    else:\n"
                "        return param1 + param2\n\n\n"
            ),
            does_not_raise(),
        ),
        (
            test_function,
            True,
            False,
            (
                "@pytest.fixture\n"
                "def test_function(param1: float, param2: int, param3: bool, param4: str = 'test') -> float:\n"
                "    if not all([isinstance(param1, float), isinstance(param2, int), isinstance(param3, bool), isinstance(param4, str)]):\n"
                "        raise TypeError(\n"
                '            "test_function expects arg types: [float, int, bool, str], "\n'
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
    get_instance: FunctionInspector,
    func,
    add_guards,
    add_debugs,
    expected_result,
    expected_context,
) -> None:
    with expected_context:
        get_instance.analyse(func)
        assert (
            get_instance.add_boilerplate(add_guards, add_debugs)
            == expected_result
        )
