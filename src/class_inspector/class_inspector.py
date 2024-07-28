import attr
from attr.validators import instance_of

from class_inspector import _utils as utils
from class_inspector.function_inspector import FunctionInspector


@attr.define
class ClassInspector:
    obj: object = attr.ib()
    meths: dict = attr.ib(init=False, validator=[instance_of(dict)])
    class_name: str = attr.ib(init=False, validator=[instance_of(str)])
    function_inspector: FunctionInspector = attr.ib(
        default=FunctionInspector(),
        validator=[instance_of(FunctionInspector)],
    )

    def __attrs_post_init__(self):
        self.meths = utils.get_class_methods(self.obj)
        self.class_name = type(self.obj).__name__

    def get_parametrized_function_tests(
        self, check_types: bool = True, match: bool = False
    ) -> str:
        tests = ["import pytest\n\n\n", self._get_test_instance_fixture()]
        for v in self.meths.values():
            self.function_inspector.analyse(v)
            tests.append(self.function_inspector.get_test(check_types, match))
        return "".join(tests)

    def add_boilerplate(
        self, add_guards: bool = False, add_debugs: bool = False
    ) -> str:
        methods = []
        for v in self.meths.values():
            self.function_inspector.analyse(v)
            methods.append(
                self.function_inspector.add_boilerplate(add_guards, add_debugs)
            )
        return "".join(methods)

    def _get_test_instance_fixture(self) -> str:
        return (
            f"@pytest.fixture\ndef get_{utils._camel_to_snake(self.class_name)}_instance() -> {self.class_name}:\n"
            f"    return {self.class_name}()\n\n\n"
        )
