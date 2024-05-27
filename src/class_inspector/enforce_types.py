import inspect
from typing import Callable


def enforce_types(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        parameters = signature.parameters

        errors = []

        for i, arg in enumerate(args):
            param_name = list(parameters.keys())[i]
            param_type = parameters[param_name].annotation
            if not isinstance(arg, param_type):
                errors.append(
                    f"arg {param_name} expects type {param_type.__name__}, "
                    f"recieved: {type(arg).__name__}"
                )

        for param_name, kwarg in kwargs.items():
            param_type = parameters[param_name].annotation
            if not isinstance(kwarg, param_type):
                errors.append(
                    f"kwarg {param_name} expects type {param_type.__name__}, "
                    f"recieved: {type(kwarg).__name__}"
                )

        if errors:
            raise TypeError("\n    " + "\n    ".join(errors))

        return func(*args, **kwargs)

    return wrapper
