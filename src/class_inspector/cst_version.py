from __future__ import annotations

import re
from typing import Dict, Optional, Tuple

import attrs
import black
import isort
import libcst as cst
import libcst.matchers as m
from attrs.validators import instance_of, optional


def _is_dunder(item: str) -> bool:
    return item.startswith("__") and item.endswith("__")


def camel_to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


def format_code_str(code_snippet: str) -> str:
    return black.format_str(isort.code(code_snippet), mode=black.FileMode())


def str_to_cst(code: str) -> cst.Module:
    return cst.parse_module(code)


def cst_to_str(node) -> str:
    return cst.Module([]).code_for_node(node)


def _get_test_case(
    args: str,
    test_arg: str = "",
    raises_error: str = "",
    raises_arg_types: bool = False,
) -> str:
    if raises_arg_types:
        return f"pytest.param({args}, expected_result, pytest.raises(TypeError), id='Ensure raises `TypeError` if given wrong type for `{test_arg}`')"
    elif raises_error:
        return f"pytest.param({args}, expected_result, pytest.raises({raises_error}), id='Ensure raises `{raises_error}` if...')"
    return f"pytest.param({args}, expected_result, does_not_raise(), id='Ensure x when `{test_arg}` is y')"


def _get_test(
    func_details: FuncDetails, test_raises: bool = True, raises_arg_types: bool = False
) -> str:
    args_str = ", ".join(func_details.params.keys())
    test_cases = [
        _get_test_case(args_str, test_arg) for test_arg in func_details.params.keys()
    ]
    if test_raises:
        test_cases.extend(
            [
                _get_test_case(args_str, raises_error=raises)
                for raises in func_details.raises
            ]
        )

    if raises_arg_types:
        test_cases.extend(
            [
                _get_test_case(args_str, test_arg, raises_arg_types=True)
                for test_arg in func_details.params.keys()
            ],
        )

    std_name = func_details.name.strip("_")
    class_instance = (
        ""
        if not func_details.class_name
        else f"{camel_to_snake(func_details.class_name)} = {func_details.class_name}()"
    )
    func_call = (
        func_details.name
        if not func_details.class_name
        else f"{camel_to_snake(func_details.class_name)}.{func_details.name}"
    )
    test_cases = ",".join(test_cases)
    test_str = [
        "@pytest.mark.parametrize(",
        f"'{args_str}, expected_result, expected_context',",
        f"[{test_cases}])",
        f"def test_{std_name}({args_str}, expected_result, expected_context):",
        "    with expected_context:",
        f"        assert {func_call}({args_str}) == expected_result\n\n",
    ]

    if class_instance:
        test_str.insert(-1, f"        {class_instance}")

    return "\n".join(test_str)


def get_tests(funcs: Dict[str, FuncDetails]) -> str:
    tests_str = [
        "from contextlib import nullcontext as does_not_raise",
        "import pytest",
    ]
    for func in funcs.values():
        if func.params:
            tests_str.append(_get_test(func))

    return format_code_str("\n".join(tests_str))


def get_inner_outer_types(attr_type: str) -> Tuple[str, str] | str:
    """
    Get the inner and outer types from the attribute type string.

    Args:
        attr_type (str): The attribute type string.

    Returns:
        Tuple[str, str]: The inner and outer types extracted from attr_type.

    Raises:
        TypeError: If the input is not a string.
        AttributeError: If the regular expression does not match.
    """
    if not all([isinstance(attr_type, str)]):
        raise TypeError(
            "get_inner_outer_types expects arg types: [str], "
            f"received: [{type(attr_type).__name__}]"
        )
    bracket_type = re.search(r"\[(.*?)\]", attr_type)
    if bracket_type:
        outer_type = attr_type.replace(bracket_type.group(), "")
        inner_type = bracket_type.group(1)
        return inner_type, outer_type
    return attr_type


ITERABLES = ["list", "set", "tuple", "dict"]


def get_isinstance_type(attr_type: str) -> str:
    if not bool(re.search(r"\[.*?\]", attr_type)):
        return attr_type

    inner_type, outer_type = get_inner_outer_types(attr_type)

    if outer_type == "Optional":
        inner_type = ", ".join([inner_type, "NoneType"])

    if outer_type.lower() in ITERABLES:
        return outer_type
    if len(inner_type.split(",")) > 1:
        return f"({inner_type})"
    return inner_type


def get_guard_conditions(func_details: FuncDetails) -> str:
    expected_types, received_types = [], []

    for param in func_details.params.values():
        if param.annot:
            expected_types.append(get_isinstance_type(param.annot))
            received_types.append(f"{{type({param.name}).__name__}}")

    expected_types = ", ".join(expected_types)
    received_types = ", ".join(received_types)

    if expected_types and received_types:
        is_instances = ", ".join(
            [
                f"isinstance({param.name}, {get_isinstance_type(param.annot)})"
                for param in func_details.params.values()
                if param.annot
            ]
        )
        guards = (
            f"if not all([{is_instances}]):\n"
            "    raise TypeError("
            f'"{func_details.name} expects arg types: [{expected_types}], "'
            f' f"received: [{received_types}]")'
        )
        return guards
    return ""


def get_annotation_type(annot_node: cst.Annotation | None) -> str:
    def parse_node(node: cst.CSTNode) -> str:
        if isinstance(node, cst.Name):
            return node.value
        elif isinstance(node, cst.Attribute):
            return f"{parse_node(node.value)}.{node.attr.value}"
        elif isinstance(node, cst.Subscript):
            base = parse_node(node.value)
            slices = ", ".join(
                parse_node(element.slice.value)
                for element in node.slice
                if isinstance(element, cst.SubscriptElement)
                and isinstance(element.slice, cst.Index)
            )
            return f"{base}[{slices}]"
        return ""

    if isinstance(annot_node, cst.Annotation):
        return parse_node(annot_node.annotation)
    return ""


@attrs.define
class ParamDetails:
    name: str = attrs.field(validator=[instance_of(str)])
    annot: str = attrs.field(default="", validator=[instance_of(str)])
    default: Optional[str] = attrs.field(
        default=None, validator=[optional(instance_of(str))]
    )


@attrs.define
class FuncDetails:
    name: str = attrs.field()
    params: dict = attrs.field(default=None)
    return_annot: str = attrs.field(default="", validator=[instance_of(str)])
    raises: list = attrs.field(default=None)
    class_name: str = attrs.field(default="")

    def __attrs_post_init__(self):
        self.params, self.raises = {}, []


@attrs.define
class FuncVisitor(cst.CSTVisitor):
    funcs: Dict[str, FuncDetails] = attrs.field(default=None)
    curr_class: str = attrs.field(default="", validator=[instance_of(str)])
    curr_func: str = attrs.field(default="", validator=[instance_of(str)])
    curr_param: str = attrs.field(default="", validator=[instance_of(str)])
    in_lambda: bool = attrs.field(default=False, validator=[instance_of(bool)])

    def __attrs_post_init__(self):
        self.funcs = {}

    def visit_ClassDef(self, node: cst.ClassDef):
        self.curr_class = node.name.value

    def leave_ClassDef(self, node: cst.ClassDef):
        self.curr_class = ""

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        self.curr_func = node.name.value
        self.funcs[self.curr_func] = FuncDetails(
            node.name.value, class_name=self.curr_class
        )
        self.funcs[self.curr_func].return_annot = get_annotation_type(node.returns)

    def leave_FunctionDef(self, node: cst.FunctionDef) -> None:
        self.curr_func = ""

    def visit_Param(self, node: cst.Param) -> None:
        if self.curr_func:
            self.curr_param = node.name.value
            if (
                not self.curr_class or self.curr_param != "self"
            ) and not self.in_lambda:
                self.funcs[self.curr_func].params[node.name.value] = ParamDetails(
                    self.curr_param,
                    get_annotation_type(node.annotation),
                    node.default.value if node.default else None,
                )

    def visit_Raise(self, node: cst.Raise) -> None:
        self.funcs[self.curr_func].raises.append(node.exc.func.value)

    def visit_Lambda(self, node: cst.Lambda):
        self.in_lambda = True

    def leave_Lambda(self, node: cst.Lambda):
        self.in_lambda = False


@attrs.define
class AddBoilerplateTransformer(cst.CSTTransformer):
    funcs: Dict[str, FuncDetails] = attrs.field()
    add_debugs: bool = attrs.field(default=False, validator=[instance_of(bool)])
    add_guards: bool = attrs.field(default=False, validator=[instance_of(bool)])

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        if any(
            [
                original_node.name.value not in self.funcs,
                _is_dunder(original_node.name.value),
                not self.funcs[original_node.name.value].params,
            ]
        ):
            return updated_node

        existing_body = list(updated_node.body.body)

        if existing_body and m.matches(
            existing_body[0],
            m.SimpleStatementLine(body=[m.Expr(value=m.SimpleString())]),
        ):
            docstring = existing_body.pop(0)
        else:
            docstring = None

        additions = []

        if self.add_debugs:
            debugs = format_code_str("logger.debug(locals())")
            additions.append(cst.parse_statement(debugs))
        if self.add_guards:
            guards = format_code_str(
                get_guard_conditions(self.funcs[original_node.name.value])
            )
            if guards:
                additions.append(cst.parse_statement(guards))

        if docstring is not None:
            additions_body = [docstring, *additions, *existing_body]
        else:
            additions_body = [*additions, *existing_body]

        new_body = cst.IndentedBlock(body=additions_body)
        return updated_node.with_changes(body=new_body)
