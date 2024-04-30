import re
from typing import List, Tuple

import attr
from attr.validators import deep_iterable, instance_of

ITERABLES = ["list", "set", "tuple"]
MAPPINGS = ["dict"]


@attr.define
class AttrMap:
    attr_name: str = attr.ib(validator=[instance_of(str)])
    attr_type: str = attr.ib(validator=[instance_of(str)])
    attr_init: bool = attr.ib(validator=[instance_of(bool)])


@attr.define
class AttrGenerator:
    class_name: str = attr.ib(validator=[instance_of(str)])
    attributes: list = attr.ib(
        validator=[
            deep_iterable(
                member_validator=instance_of((dict, AttrMap)),
                iterable_validator=instance_of(list),
            )
        ]
    )

    def contains_square_brackets(self, attr_type: str) -> bool:
        if not all([isinstance(attr_type, str)]):
            raise TypeError(
                "contains_square_brackets() expects args of types [str]"
                f"recieved type: {type(attr_type).__name__}"
            )
        return bool(re.search(r"\[.*?\]", attr_type))

    def is_outer_type_in_list(
        self, attr_type: str, deep_list: List[str]
    ) -> bool:
        if not all([isinstance(attr_type, str), isinstance(deep_list, list)]):
            raise TypeError(
                "is_outer_type_in_list expects arg types: [str, List], "
                f"received: [{type(attr_type).__name__}, {type(deep_list).__name__}]"
            )
        _, outer_type = self.get_inner_outer_types(attr_type)
        return outer_type in deep_list

    def is_deep_iterable(self, attr_type: str) -> bool:
        if not all([isinstance(attr_type, str)]):
            raise TypeError(
                "is_deep_iterable expects arg types: [str], received: "
                f"[{type(attr_type).__name__}]"
            )
        return self.contains_square_brackets(
            attr_type
        ) and self.is_outer_type_in_list(attr_type, ITERABLES)

    def is_deep_mapping(self, attr_type: str) -> bool:
        if not all([isinstance(attr_type, str)]):
            raise TypeError(
                "is_deep_mapping expects arg types: [str], "
                f"received: [{type(attr_type).__name__}]"
            )
        return self.contains_square_brackets(
            attr_type
        ) and self.is_outer_type_in_list(attr_type, MAPPINGS)

    def get_inner_outer_types(self, attr_type: str) -> Tuple[str, str]:
        if not all([isinstance(attr_type, str)]):
            raise TypeError(
                "get_inner_outer_types expects arg types: [str], "
                f"received: [{type(attr_type).__name__}]"
            )
        s = re.search(r"\[(.*?)\]", attr_type)
        if s:
            outer_type = attr_type.replace(s.group(), "").lower()
            inner_type = s.group(1)
            return inner_type, outer_type
        raise AttributeError(f"{s} does not have method group()")

    def get_deep_iterable(self, attr_type: str) -> str:
        if not all([isinstance(attr_type, str)]):
            raise TypeError(
                "get_deep_iterable expects arg types: [str], "
                f"received: [{type(attr_type).__name__}]"
            )
        inner_type, outer_type = self.get_inner_outer_types(attr_type)
        return (
            f"deep_iterable(member_validator=instance_of({inner_type}),"
            f" iterable_validator=instance_of({outer_type}))"
        )

    def get_deep_mapping(self, attr_type: str) -> str:
        if not all([isinstance(attr_type, str)]):
            raise TypeError(
                "get_deep_mapping expects arg types: [str], "
                f"received: [{type(attr_type).__name__}]"
            )
        inner_type, outer_type = self.get_inner_outer_types(attr_type)
        k_, v_ = inner_type.split(", ")
        return (
            f"deep_mapping(key_validator=instance_of({k_}), "
            f"value_validator=instance_of({v_}), "
            f"mapping_validator=instance_of({outer_type}))"
        )

    def get_validator(self, attr_type: str) -> str:
        if not all([isinstance(attr_type, str)]):
            raise TypeError(
                "get_validator expects arg types: [str], "
                f"received: [{type(attr_type).__name__}]"
            )
        if not self.contains_square_brackets(attr_type):
            return f"instance_of({attr_type})"
        if self.is_deep_iterable(attr_type):
            return self.get_deep_iterable(attr_type)
        if self.is_deep_mapping(attr_type):
            return self.get_deep_mapping(attr_type)
        raise NotImplementedError(f"{attr_type} is not implemented")

    def get_type_hint(self, attr_type: str):
        if not all([isinstance(attr_type, str)]):
            raise TypeError(
                "get_type_hint expects arg types: [str], "
                f"received: [{type(attr_type).__name__}]"
            )
        if not self.contains_square_brackets(attr_type):
            return attr_type
        if self.is_deep_iterable(attr_type) or self.is_deep_mapping(attr_type):
            _, outer_type = self.get_inner_outer_types(attr_type)
            return outer_type

    def get_init_bool(self, attr_init: bool) -> str:
        if not all([isinstance(attr_init, bool)]):
            raise TypeError(
                "get_type_hint expects arg types: [str], "
                f"received: [{type(attr_init).__name__}]"
            )
        if attr_init:
            return ""
        return f", init={attr_init}"

    def get_imports(self) -> str:
        return (
            "import attr\nfrom attr.validators "
            "import instance_of, deep_iterable, deep_mapping\n\n"
        )

    def get_class_sig(self) -> str:
        return f"@attr.define\nclass {self.class_name}:"

    def get_attrib(
        self, attr_name: str, attr_type: str, attr_init: bool
    ) -> str:
        if not all(
            [
                isinstance(attr_name, str),
                isinstance(attr_type, str),
                isinstance(attr_init, bool),
            ]
        ):
            raise TypeError(
                "get_attrib expects arg types: [str, str, bool], "
                f"received: [{type(attr_name).__name__}, "
                f"{type(attr_type).__name__}, {type(attr_init).__name__}]"
            )

        init_true = self.get_init_bool(attr_init)
        return (
            f"    {attr_name}: {self.get_type_hint(attr_type)} = "
            f"attr.ib(validator=[{self.get_validator(attr_type)}]{init_true})"
        )

    def get_attr_class(self) -> str:
        class_str = []
        class_str.append(self.get_imports())
        class_str.append(self.get_class_sig())
        for at_dict in self.attributes:
            if isinstance(at_dict, dict):
                at = AttrMap(**at_dict)
            elif isinstance(at_dict, AttrMap):
                at = at_dict
            class_str.append(
                self.get_attrib(at.attr_name, at.attr_type, at.attr_init)
            )
        return "\n".join(class_str)
