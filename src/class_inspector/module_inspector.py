import inspect
from types import ModuleType

import attr
from attr.validators import instance_of

from class_inspector.function_inspector import FunctionInspector


@attr.define
class ModuleInspector:
    module: ModuleType = attr.ib(validator=[instance_of(ModuleType)])
    module_vars: dict = attr.ib(init=False, validator=[instance_of(dict)])
    module_name: str = attr.ib(init=False, validator=[instance_of(str)])
    function_inspector: FunctionInspector = attr.ib(
        default=FunctionInspector(),
        validator=[instance_of(FunctionInspector)],
    )
    custom_functions: dict = attr.ib(init=False, validator=[instance_of(dict)])
    custom_classes: dict = attr.ib(init=False, validator=[instance_of(dict)])

    def __attrs_post_init__(self):
        self.module_vars = vars(self.module)
        self.module_name = self.module.__name__
        self.extract_custom_classes()
        self.extract_custom_functions()

    def extract_custom_functions(self) -> None:
        self.custom_functions = {
            k: v for k, v in self.module_vars.items() if inspect.isfunction(v)
        }

    def extract_custom_classes(self) -> None:
        self.custom_classes = {
            k: v for k, v in self.module_vars.items() if inspect.isclass(v)
        }

    def get_parametrized_function_tests(
        self, check_types: bool = True, match: bool = False
    ) -> str:
        tests = []
        for _, v in self.custom_functions.items():
            self.function_inspector.analyse(v)
            tests.append(self.function_inspector.get_test(check_types, match))
        return "".join(tests)

    def add_boilerplate(
        self, add_guards: bool = False, add_debugs: bool = False
    ) -> str:
        functions = []
        for _, v in self.custom_functions.items():
            self.function_inspector.analyse(v)
            functions.append(
                self.function_inspector.add_boilerplate(add_guards, add_debugs)
            )
        return "".join(functions)
