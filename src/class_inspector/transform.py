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
    """Add boilerplate to the object.

    Args:
        obj (Union[ModuleType, FunctionType]): The object to add boilerplate to.
        add_debugs (bool, optional):
            Add debugs to each of the functions or methods. Defaults to True.
        add_guards (bool, optional):
            Add guard conditions to each of the functions, will check the type hints if supplied. Defaults to False.

    Returns:
        str: The class, function or module with modifications.

    Usage:
        .. code-block:: python

            from class_inspector import add_boilerplate

            def example_function(a: int, b: str = "default") -> str:
                if a > 0:
                    return str(a) + b
                return a

            print(add_boilerplate(example_function, add_debugs=True, add_guards=True))

    Output:
        .. code-block:: python

            def example_function(a: int, b: str = "default") -> str:
                logger.debug(locals())
                if not all([isinstance(a, int), isinstance(b, str)]):
                    raise TypeError(
                        "example_function expects arg types: [int, str], "
                        f"received: [{type(a).__name__}, {type(b).__name__}]"
                    )
                if a > 0:
                    return str(a) + b
                return a
    """
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
    """_summary_

    Args:
        obj (Union[ModuleType, FunctionType]): The object to get tests for.
        test_raises (bool, optional): Create tests for each of the exceptions raised in the function. Defaults to True.
        raises_arg_types (bool, optional): Create tests to check the type of each of the input arguments. Defaults to False.

    Returns:
        str: The parametrized tests for the given object, returns a test per function if given a module or per method if given classes

    Usage:
        .. code-block :: python

            from class_inspector import get_parametrized_tests

            def example_function(a: int, b: str = "default") -> str:
                if a > 0:
                    return str(a) + b
                return a

            print(get_parametrized_tests(example_function, raises_arg_types=False))

    Output:
        .. code-block:: python

            from contextlib import nullcontext as does_not_raise

            import pytest


            @pytest.mark.parametrize(
                "a, b, expected_result, expected_context",
                [
                    pytest.param(
                        a, b, expected_result, does_not_raise(), id="Ensure x when `a` is y"
                    ),
                    pytest.param(
                        a, b, expected_result, does_not_raise(), id="Ensure x when `b` is y"
                    ),
                ],
            )
            def test_example_function(a, b, expected_result, expected_context):
                with expected_context:
                    assert example_function(a, b) == expected_result

    """
    module = str_to_cst(format_code_str(inspect.getsource(obj)))
    visitor = FuncVisitor()
    module.visit(visitor)
    return get_tests(visitor.funcs, test_raises, raises_arg_types)
