import pytest
from function_inspector import FunctionInspector


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
    assert get_instance._object == test_function
    assert get_instance._name == "test_function"
    assert get_instance._parameters == {
        "param1": float,
        "param2": int,
        "param3": bool,
    }
    assert get_instance._return_annotations == float


def test_get_parametrize_decorator(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert (
        get_instance.get_parametrize_decorator()
        == '@pytest.mark.parametrize(\n    "param1, param2, param3, expected_result",\n    [\n        (param1, param2, param3, expected_result),\n    ]\n)\n'
    )


def test_get_params_str(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert get_instance.get_params_str() == "param1, param2, param3"


def test_get_pytest_imports(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert get_instance.get_pytest_imports() == "import pytest\n\n"


def test_get_return_annotations(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert get_instance.get_return_annotations() == float


def test_get_test(get_instance: FunctionInspector) -> None:
    get_instance.analyse(test_function)
    assert (
        get_instance.get_test()
        == '@pytest.mark.parametrize(\n    "param1, param2, param3, expected_result",\n    [\n        (param1, param2, param3, expected_result),\n    ]\n)\ndef test_test_function(param1, param2, param3, expected_result) -> None:\n    assert test_function(param1, param2, param3) == expected_result\n\n'
    )
