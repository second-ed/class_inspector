from __future__ import annotations

import inspect
from typing import Callable

import attr
from attr.validators import instance_of


@attr.define
class FunctionInspector:
    name: str = attr.ib(init=False, validator=[instance_of(str)])
    parameters: dict = attr.ib(init=False, validator=[instance_of(dict)])
    return_annotation: str = attr.ib(init=False, validator=[instance_of(str)])
    t: str = attr.ib(default="    ", validator=instance_of(str), init=False)  # type: ignore
    obj: Callable = attr.ib(init=False)

    def analyse(self, object_) -> None:
        self.obj = object_
        self.name = self.obj.__name__
        self.parameters = {
            v.name: v.annotation
            for k, v in inspect.signature(self.obj).parameters.items()
        }
        self.return_annotation = self.get_return_annotations()
        self.t: str = "    "

    def get_return_annotations(self) -> str:
        annot = inspect.signature(self.obj).return_annotation
        if annot is not inspect._empty:
            return annot.__name__
        return "None"

    def get_params_str(self) -> str:
        params = ", ".join(list(self.parameters.keys()))
        if params:
            return params  # + ", "
        return ""

    def get_params_types(self) -> str:
        return ", ".join(
            [
                t_.__name__ if hasattr(t_, "__name__") else "no_type"
                for t_ in self.parameters.values()
            ]
        )

    def get_class_name(self) -> str:
        if inspect.ismethod(self.obj):
            return self.obj.__self__.__class__.__name__
        return self.name

    def strip_underscores(self, item: str) -> str:
        if not isinstance(item, str):
            raise TypeError(f"item must be of type str, got {type(item)}")
        return item.strip("_")

    def get_instance_sig(self) -> str:
        if inspect.ismethod(self.obj):
            return f"get_instance: {self.get_class_name()}, "
        elif inspect.isfunction(self.obj):
            return ""
        return ""

    def get_test_sig(self) -> str:
        sig = self.get_instance_sig() + self.get_params_str()
        return f"def test_{self.strip_underscores(self.name)}({sig}, expected_result, expected_context) -> None:\n"

    def get_parametrize_decorator(
        self, check_types: bool = True, match: bool = False
    ) -> str:
        args = self.get_params_str()
        return (
            "@pytest.mark.parametrize(\n"
            + f'{self.t}"{args}, expected_result, expected_context",\n'
            + f"{self.t}[\n"
            + self.get_test_case(args)
            + (
                self.get_raises_type_error_test_case(args, check_types, match)
                * len(self.parameters)
            )
            + f"{self.t}]\n)\n"
        )

    def get_test_case(self, args: str) -> str:
        return f"{self.t * 2}({args}, expected_result, expected_context),\n"

    def get_raises_type_error_test_case(
        self, args: str, check_types: bool = True, match: bool = False
    ) -> str:
        if not check_types:
            return ""
        match_stmt = ""
        if match:
            match_stmt = ', match=r""'
        return f"{self.t * 2}({args}, None, pytest.raises(TypeError{match_stmt})),\n"

    def get_instance_call(self) -> str:
        sig: str = self.get_params_str()
        if inspect.ismethod(self.obj):
            return f"get_instance.{self.name}({sig}) "
        elif inspect.isfunction(self.obj):
            return f"{self.name}({sig}) "
        return f"{self.name}({sig}) "

    def get_test_body(self) -> str:
        test_body = f"{self.t}with expected_context:\n"
        test_body += f"{2*self.t}assert "
        test_body += self.get_instance_call()
        if self.return_annotation != "None":
            test_body += "== expected_result\n"
        else:
            test_body += "is None\n"
        return test_body

    def get_test(self, check_types: bool = True, match: bool = False) -> str:
        test_full = ""
        test_full += self.get_parametrize_decorator(check_types, match)
        test_full += self.get_test_sig()
        test_full += self.get_test_body()
        test_full += "\n\n"
        return test_full

    def get_guards(self) -> str:
        if not self.parameters:
            return ""
        expected_types = ", ".join(
            [arg.__name__ for arg in self.parameters.values()]
        )
        received_types = ", ".join(
            [f"{{type({arg}).__name__}}" for arg in self.parameters.keys()]
        )
        guards: str = (
            f"{self.t}if not all(["
            + ", ".join(
                [
                    f"isinstance({k}, {v.__name__})"
                    for k, v in self.parameters.items()
                ]
            )
            + "]):\n"
        )
        raises = (
            f"{self.t*2}raise TypeError(\n"
            + f'{self.t*3}"{self.name} expects arg types: [{expected_types}], "\n'
            + f'{self.t*3}f"received: [{received_types}]"\n'
            + f"{self.t*2})\n\n"
        )
        return guards + raises
