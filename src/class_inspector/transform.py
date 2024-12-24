import inspect
from types import FunctionType, ModuleType
from typing import Union

from class_inspector.create_tests import get_tests
from class_inspector.cst_walkers import (
    AddBoilerplateTransformer,
    FuncVisitor,
)
from class_inspector.utils import (
    format_code_str,
    str_to_cst,
)


def add_boilerplate(
    obj: Union[ModuleType, FunctionType],
    /,
    add_debugs: bool = True,
    add_guards: bool = False,
) -> str:
    module = str_to_cst(format_code_str(inspect.getsource(obj)))
    visitor = FuncVisitor()
    module.visit(visitor)
    transformer = AddBoilerplateTransformer(visitor.funcs, add_debugs, add_guards)
    modified_module = module.visit(transformer)
    return format_code_str(modified_module.code)


def get_parametrized_tests(
    obj: Union[ModuleType, FunctionType],
    /,
    test_raises: bool = True,
    raises_arg_types: bool = False,
) -> str:
    module = str_to_cst(format_code_str(inspect.getsource(obj)))
    visitor = FuncVisitor()
    module.visit(visitor)
    return get_tests(visitor.funcs, test_raises, raises_arg_types)
