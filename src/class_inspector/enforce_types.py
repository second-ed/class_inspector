import inspect
from typing import Any, Callable, Union, get_args, get_origin


def enforce_types(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        parameters = signature.parameters
        errors = ""

        for i, arg in enumerate(args):
            param_name = list(parameters.keys())[i]
            errors += check_type(
                arg, param_name, parameters[param_name].annotation
            )

        for param_name, kwarg in kwargs.items():
            errors += check_type(
                kwarg, param_name, parameters[param_name].annotation
            )

        if errors:
            raise TypeError("".join(errors))

        return func(*args, **kwargs)

    return wrapper


def check_type(arg: Any, param_name: str, param_type: type) -> str:
    if not isinstance(arg, simplify_annotation(param_type)):
        return (
            f"\n    arg {param_name} expects type: {param_type}, "
            f"received: {type(arg).__name__}"
        )
    return ""


def simplify_annotation(annotation: type):
    origin = get_origin(annotation)
    args = get_args(annotation)

    # is native or custom type
    if origin is None:
        return annotation

    if origin is Union:
        # is Optional type
        if type(None) in args:
            non_none_args = [arg for arg in args if arg is not type(None)]
            if len(non_none_args) == 1:
                return (simplify_annotation(non_none_args[0]), type(None))
        return tuple(simplify_annotation(arg) for arg in args)
    return origin
