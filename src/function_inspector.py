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

    def get_pytest_imports(self) -> str:
        return "import pytest\n\n"

    def get_parametrize_decorator(self) -> str:
        args = self.get_params_str()
        return f'@pytest.mark.parametrize(\n    "{args}, expected_result",\n    [\n        ({args}, expected_result),\n    ]\n)\n'

    def get_test(self) -> str:
        sig: str = self.get_params_str()
        return (
            self.get_parametrize_decorator()
            + f"def test_{self._name}({sig}, expected_result) -> None:\n"
            + f"    assert {self._name}({sig}) == expected_result\n\n"
        )

