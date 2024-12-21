from __future__ import annotations

from typing import Dict, Optional

import attrs
import libcst as cst
from attrs.validators import instance_of, optional

from class_inspector._utils import format_code_str


def str_to_cst(code: str) -> cst.Module:
    return cst.parse_module(code)


def cst_to_str(node) -> str:
    return cst.Module([]).code_for_node(node)


def get_test_case(args: str, test_arg: str, raises: bool = False) -> str:
    print(locals())
    if not raises:
        return f"pytest.param({args}, expected_result, does_not_raise(), id='Ensure behaviour x when {test_arg} is y')"
    return f"pytest.param({args}, expected_result, pytest.raises(TypeError), id='Ensure raises TypeError if given wrong type for `{test_arg}`')"


def get_test(func_details: FuncDetails, test_raises: bool = False) -> str:
    args_str = ", ".join(func_details.params.keys())
    test_cases = [
        get_test_case(args_str, test_arg) for test_arg in func_details.params.keys()
    ]
    if test_raises:
        test_cases = [
            test_cases,
            *[
                get_test_case(args_str, test_arg, True)
                for test_arg in func_details.params.keys()
            ],
        ]

    return (
        "from contextlib import nullcontext as does_not_raise\n"
        "import pytest\n"
        "@pytest.mark.parametrize("
        f"'{args_str}, expected_result, expected_context',"
        f"[{','.join(test_cases)}]"
        ")\n"
        f"def test_{func_details.name}({args_str}, expected_result, expected_context):\n"
        "    with expected_context:"
        f"        assert {func_details.name}({args_str}) == expected_result"
    )


def get_guard_conditions(func_details: FuncDetails) -> str:
    expected_types, received_types = [], []

    for param in func_details.params.values():
        if param.annot:
            expected_types.append(param.annot)
            received_types.append(f"{{type({param.name}).__name__}}")

    expected_types = ", ".join(expected_types)
    received_types = ", ".join(received_types)

    if expected_types and received_types:
        is_instances = ", ".join(
            [
                f"isinstance({param.name}, {param.annot})"
                for param in func_details.params.values()
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

    def __attrs_post_init__(self):
        self.params = {}


@attrs.define
class FuncVisitor(cst.CSTVisitor):
    funcs: Dict[str, FuncDetails] = attrs.field(default=None)
    curr_func: str = attrs.field(default="", validator=[instance_of(str)])
    curr_param: str = attrs.field(default="", validator=[instance_of(str)])

    def __attrs_post_init__(self):
        self.funcs = {}

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        self.curr_func = node.name.value
        self.funcs[self.curr_func] = FuncDetails(node.name.value)
        self.funcs[self.curr_func].return_annot = get_annotation_type(node.returns)

    def leave_FunctionDef(self, node: cst.FunctionDef) -> None:
        self.curr_func = ""

    def visit_Param(self, node: cst.Param) -> None:
        if self.curr_func:
            self.curr_param = node.name.value
            self.funcs[self.curr_func].params[node.name.value] = ParamDetails(
                self.curr_param,
                get_annotation_type(node.annotation),
                node.default.value if node.default else None,
            )


@attrs.define
class AddBoilerplateTransformer(cst.CSTTransformer):
    funcs: Dict[str, FuncDetails] = attrs.field()
    add_debugs: bool = attrs.field(default=False, validator=[instance_of(bool)])
    add_guards: bool = attrs.field(default=False, validator=[instance_of(bool)])

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        if original_node.name.value not in self.funcs:
            return updated_node

        existing_body = list(updated_node.body.body)
        if (
            len(existing_body) > 0
            and isinstance(existing_body[0], cst.SimpleStatementLine)
            and isinstance(existing_body[0].body[0], cst.Expr)
            and isinstance(existing_body[0].body[0].value, cst.SimpleString)
        ):
            docstring = existing_body[0]
            existing_body = existing_body[1:]
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
