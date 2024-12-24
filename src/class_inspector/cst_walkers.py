from __future__ import annotations

from typing import Dict

import attrs
import libcst as cst
import libcst.matchers as m
from attrs.validators import instance_of

from class_inspector.data_structures import FuncDetails, ParamDetails
from class_inspector.guard_conditions import get_guard_conditions
from class_inspector.utils import is_dunder


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

    def visit_Lambda(self, node: cst.Lambda) -> None:
        self.in_lambda = True

    def leave_Lambda(self, node: cst.Lambda) -> None:
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
                is_dunder(original_node.name.value),
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
            debugs = "logger.debug(locals())\n"
            additions.append(cst.parse_statement(debugs))
        if self.add_guards:
            guards = get_guard_conditions(self.funcs[original_node.name.value])

            if guards:
                additions.append(cst.parse_statement(guards))

        if docstring is not None:
            additions_body = [docstring, *additions, *existing_body]
        else:
            additions_body = [*additions, *existing_body]

        new_body = cst.IndentedBlock(body=additions_body)
        return updated_node.with_changes(body=new_body)
