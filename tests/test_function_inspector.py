from contextlib import nullcontext as does_not_raise

import pytest
from class_inspector.function_inspector import FunctionInspector


@pytest.fixture
def test_function(param1: float, param2: int, param3: bool) -> float:
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
    }
    assert get_instance.return_annotation == "float"


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        ("test_function", does_not_raise()),
    ],
)
def test_get_class_name(
    get_instance: FunctionInspector, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(test_function)
        assert get_instance.get_class_name() == expected_result


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        (
            '    if not all([isinstance(param1, float), isinstance(param2, int), isinstance(param3, bool)]):\n        raise TypeError(\n            "test_function expects arg types: [float, int, bool], "\n            f"received: [{type(param1).__name__}, {type(param2).__name__}, {type(param3).__name__}]"\n        )\n\n',
            does_not_raise(),
        )
    ],
)
def test_get_guards(
    get_instance: FunctionInspector, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(test_function)
        assert get_instance.get_guards() == expected_result


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        ("test_function(param1, param2, param3) ", does_not_raise()),
    ],
)
def test_get_instance_call(
    get_instance: FunctionInspector, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(test_function)
        assert get_instance.get_instance_call() == expected_result


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        ("", does_not_raise()),
    ],
)
def test_get_instance_sig(
    get_instance: FunctionInspector, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(test_function)
        assert get_instance.get_instance_sig() == expected_result


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        (
            '@pytest.mark.parametrize(\n    "param1, param2, param3, expected_result, expected_context",\n    [\n        (param1, param2, param3, expected_result, expected_context),\n    ]\n)\n',
            does_not_raise(),
        ),
    ],
)
def test_get_parametrize_decorator(
    get_instance: FunctionInspector, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(test_function)
        assert get_instance.get_parametrize_decorator() == expected_result


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        ("param1, param2, param3", does_not_raise()),
    ],
)
def test_get_params_str(
    get_instance: FunctionInspector, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(test_function)
        assert get_instance.get_params_str() == expected_result


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        ("float, int, bool", does_not_raise()),
    ],
)
def test_get_params_types(
    get_instance: FunctionInspector, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(test_function)
        assert get_instance.get_params_types() == expected_result


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        ("float", does_not_raise()),
    ],
)
def test_get_return_annotations(
    get_instance: FunctionInspector, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(test_function)
        assert get_instance.get_return_annotations() == expected_result


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        (
            '@pytest.mark.parametrize(\n    "param1, param2, param3, expected_result, expected_context",\n    [\n        (param1, param2, param3, expected_result, expected_context),\n    ]\n)\ndef test_test_function(param1, param2, param3, expected_result, expected_context) -> None:\n    with expected_context:\n         assert test_function(param1, param2, param3) == expected_result\n\n\n',
            does_not_raise(),
        ),
    ],
)
def test_get_test(
    get_instance: FunctionInspector, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(test_function)
        assert get_instance.get_test() == expected_result


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        (
            "    with expected_context:\n         assert test_function(param1, param2, param3) == expected_result\n",
            does_not_raise(),
        ),
    ],
)
def test_get_test_body(
    get_instance: FunctionInspector, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(test_function)
        assert get_instance.get_test_body() == expected_result


@pytest.mark.parametrize(
    "expected_result, expected_context",
    [
        (
            "def test_test_function(param1, param2, param3, expected_result, expected_context) -> None:\n",
            does_not_raise(),
        ),
    ],
)
def test_get_test_sig(
    get_instance: FunctionInspector, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(test_function)
        assert get_instance.get_test_sig() == expected_result


@pytest.mark.parametrize(
    "item, expected_result, expected_context",
    [
        ("__test__", "test", does_not_raise()),
        ("_test", "test", does_not_raise()),
        ("test_", "test", does_not_raise()),
        ("__test", "test", does_not_raise()),
        (0, "", pytest.raises(TypeError)),
    ],
)
def test_values_strip_underscores(
    get_instance: FunctionInspector, item, expected_result, expected_context
) -> None:
    with expected_context:
        get_instance.analyse(test_function)
        assert get_instance.strip_underscores(item) == expected_result
