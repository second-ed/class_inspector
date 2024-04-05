import inspect


class FunctionInspector:
    def analyse(self, object_) -> None:
        self._object = object_
        self._name = self._object.__name__
        self._parameters = {
            v.name: v.annotation
            for k, v in inspect.signature(self._object).parameters.items()
        }
        self._return_annotations = self.get_return_annotations()

    def get_return_annotations(self):
        annot = inspect.signature(self._object).return_annotation
        if annot is not inspect._empty:
            return annot
        return None

    def get_params_str(self) -> str:
        return ", ".join(list(self._parameters.keys()))

    def get_params_types(self):
        return ", ".join([t.__qualname__ for t in self._parameters.values()])

    def get_pytest_imports(self) -> str:
        return "import pytest\n\n"

    def get_parametrize_decorator_values(self) -> str:
        args = self.get_params_str()
        return f'@pytest.mark.parametrize(\n    "{args}, expected_result",\n    [\n        ({args}, expected_result),\n    ]\n)\n'

    def get_test_values(self) -> str:
        sig: str = self.get_params_str()
        if self._parameters:
            return (
                self.get_parametrize_decorator_values()
                + f"def test_{self._name}({sig}, expected_result) -> None:\n"
                + f"    actual_result = {self._name}({sig})\n"
                + "    assert actual_result == expected_result\n"
                + f"    assert isinstance(actual_result, {self.get_return_annotations().__qualname__})\n\n"
            )
        return ""

    def get_parametrize_decorator_types(self) -> str:
        args: str = self.get_params_str()
        types: str = self.get_params_types()
        return f'@pytest.mark.parametrize(\n    "{args}",\n    [\n        ({types}),\n    ]\n)\n'

    def get_test_types(self) -> str:
        sig: str = self.get_params_str()
        if self._parameters:
            return (
                self.get_parametrize_decorator_types()
                + f"def test_{self._name}_types({sig}) -> None:\n"
                + "    with pytest.raises(TypeError):\n"
                + f"        {self._name}({sig})\n\n"
            )
        return ""

    def get_tests(self) -> str:
        if self._parameters:
            return self.get_test_values() + "\n" + self.get_test_types()
        return ""
