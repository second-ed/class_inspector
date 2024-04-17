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


def test_init(get_instance: FunctionInspector) -> None:
    assert isinstance(get_instance, FunctionInspector)


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


def test_get_return_annotation(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert get_instance.get_return_annotations() == "float"


def test_get_params_str(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert get_instance.get_params_str() == "param1, param2, param3"


def test_get_params_types(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert get_instance.get_params_types() == "float, int, bool"


def test_get_class_name(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert get_instance.get_class_name() == "test_function"


@pytest.mark.parametrize(
    "item, expected_result",
    [
        ("__test__", "test"),
        ("_test", "test"),
        ("test_", "test"),
        ("__test", "test"),
    ],
)
def test_values_strip_underscores(
    get_instance: FunctionInspector, item, expected_result
) -> None:
    get_instance.analyse(test_function)
    assert get_instance.strip_underscores(item) == expected_result


@pytest.mark.parametrize(
    "item",
    [
        (0.0),
    ],
)
def test_types_strip_underscores(
    get_instance: FunctionInspector, item
) -> None:
    with pytest.raises(TypeError):
        get_instance.strip_underscores(item)


def test_get_instance_sig(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert get_instance.get_instance_sig() == ""


def test_get_test_values_sig(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert (
        get_instance.get_test_values_sig()
        == "def test_values_test_function(param1, param2, param3, expected_result) -> None:\n"
    )


def test_get_test_types_sig(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert (
        get_instance.get_test_types_sig()
        == "def test_types_test_function(param1, param2, param3) -> None:\n"
    )


def test_get_parametrize_decorator_values(
    get_instance: FunctionInspector,
) -> None:
    get_instance.analyse(test_function)
    assert (
        get_instance.get_parametrize_decorator_values()
        == '@pytest.mark.parametrize(\n    "param1, param2, param3, expected_result",\n    [\n        (param1, param2, param3, expected_result),\n    ]\n)\n'
    )


def test_get_parametrize_decorator_types(
    get_instance: FunctionInspector,
) -> None:
    get_instance.analyse(test_function)
    assert (
        get_instance.get_parametrize_decorator_types()
        == '@pytest.mark.parametrize(\n    "param1, param2, param3",\n    [\n        (float, int, bool),\n        (float, int, bool),\n        (float, int, bool),\n    ]\n)\n'
    )


def test_get_instance_call(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert (
        get_instance.get_instance_call()
        == "test_function(param1, param2, param3) "
    )


def test_get_test_body(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert (
        get_instance.get_test_body()
        == "    test_function(param1, param2, param3) == expected_result\n"
    )


def test_get_test_values(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert (
        get_instance.get_test_values()
        == '@pytest.mark.parametrize(\n    "param1, param2, param3, expected_result",\n    [\n        (param1, param2, param3, expected_result),\n    ]\n)\ndef test_values_test_function(param1, param2, param3, expected_result) -> None:\n    test_function(param1, param2, param3) == expected_result\n\n\n'
    )


def test_get_test_raises_type_error(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert (
        get_instance.get_test_raises_type_error()
        == '@pytest.mark.parametrize(\n    "param1, param2, param3",\n    [\n        (float, int, bool),\n        (float, int, bool),\n        (float, int, bool),\n    ]\n)\ndef test_types_test_function(param1, param2, param3) -> None:\n    with pytest.raises(TypeError):\n        test_function(param1, param2, param3) \n\n\n'
    )


def test_get_tests(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert (
        get_instance.get_tests()
        == '@pytest.mark.parametrize(\n    "param1, param2, param3, expected_result",\n    [\n        (param1, param2, param3, expected_result),\n    ]\n)\ndef test_values_test_function(param1, param2, param3, expected_result) -> None:\n    test_function(param1, param2, param3) == expected_result\n\n\n@pytest.mark.parametrize(\n    "param1, param2, param3",\n    [\n        (float, int, bool),\n        (float, int, bool),\n        (float, int, bool),\n    ]\n)\ndef test_types_test_function(param1, param2, param3) -> None:\n    with pytest.raises(TypeError):\n        test_function(param1, param2, param3) \n\n\n'
    )


def test_get_guards(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert (
        get_instance.get_guards()
        == '    if not all([isinstance(param1, float), isinstance(param2, int), isinstance(param3, bool)]):\n        raise TypeError(f"test_function expects arg types: [float, int, bool], received: [{type(param1).__name__}, {type(param2).__name__}, {type(param3).__name__}]")\n\n'
    )
