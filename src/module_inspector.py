import inspect
from types import ModuleType


class ModuleInspector:
    def __init__(self, inp_module: ModuleType) -> None:
        self._module = inp_module
        self._module_vars = vars(inp_module)
        self._module_name = inp_module.__name__
        self.extract_custom_classes()
        self.extract_custom_functions()

    @property
    def module(self) -> ModuleType:
        return self._module

    @module.setter
    def module(self, module: ModuleType) -> None:
        self._module: ModuleType = module

    @property
    def module_name(self) -> str:
        return self._module_name

    @module_name.setter
    def module_name(self, module_name: str) -> None:
        self._module_name: str = module_name

    @property
    def module_vars(self) -> dict:
        return self._module_vars

    @module_vars.setter
    def module_vars(self, module_vars: dict) -> None:
        self._module_vars: dict = module_vars

    @property
    def custom_classes(self) -> dict:
        return self.custom_classes_

    @property
    def custom_functions(self) -> dict:
        return self.custom_functions_

    def extract_custom_functions(self) -> None:
        self.custom_functions_ = {
            k: v for k, v in self._module_vars.items() if inspect.isfunction(v)
        }

    def extract_custom_classes(self) -> None:
        self.custom_classes_ = {
            k: v for k, v in self._module_vars.items() if inspect.isclass(v)
        }

    def get_params_str(self, func):
        return ", ".join(list(inspect.signature(func).parameters.keys()))

    def get_parametrize_decorator(self, func):
        args = self.get_params_str(func)
        return f'@pytest.mark.parametrize(\n    "{args}, expected_result",\n    [\n        ({args}, expected_result),\n    ]\n)'

    def get_function_test(self, func_name, func):
        sig = self.get_params_str(func)
        return f"def test_{func_name}({sig}, expected_result) -> None:\n    assert {func_name}({sig}) == expected_result\n\n"

    def print_function_tests(self):
        for k, v in self.custom_functions_.items():
            sig = self.get_params_str(v)
            print(
                f"def test_{k}({sig}, expected_result) -> None:\n    assert {k}({sig}) == expected_result\n\n"
            )

    def print_parametrized_function_tests(self):
        for k, v in self.custom_functions_.items():
            print(self.get_parametrize_decorator(v))
            print(self.get_function_test(k, v))
