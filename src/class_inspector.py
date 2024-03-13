import inspect
from typing import List


class ClassInspector:
    """ClassInspector class

    Attributes:
        attrs: list
        class_name: str
        derived_attrs: list
        derived_methods: list
        dir_list: list
        methods: list
        obj: TestClass
        private_attrs: list
        private_methods: list
        public_attrs: list
        public_methods: list

    Methods:
        get_attrs() -> List[str]
        get_attrs_docstrings() -> str
        get_derived_attrs() -> List[str]
        get_derived_methods() -> List[str]
        get_init_setter(item: str) -> str
        get_init_setters() -> str
        get_item_type(item) -> str
        get_methods() -> List[str]
        get_methods_docstrings() -> str
        get_primary_methods(item_list) -> List[str]
        get_private_attrs() -> List[str]
        get_private_methods() -> List[str]
        get_public_attrs() -> List[str]
        get_public_methods() -> List[str]
        get_setter_getter_methods(item) -> str
        is_derived(item) -> bool
        is_method(item) -> bool
        is_not_dunder(item) -> bool
        is_private(item) -> bool
        is_public(item) -> bool
        print_docstring() -> None
        print_init_setters() -> None
        print_primary_methods() -> None
        set_derived_attrs() -> None
        set_derived_methods() -> None
        set_private_attrs() -> None
        set_private_methods() -> None
        set_public_attrs() -> None
        set_public_methods() -> None
        strip_underscores(item) -> str
    """

    def __init__(self, obj: object, use_properties: bool = True) -> None:
        self.obj: object = obj
        self.dir_list: List[str] = dir(self.obj)
        self.class_name: str = type(self.obj).__name__
        self._use_properties: bool = use_properties
        self.set_private_attrs()
        self.set_derived_attrs()
        self.set_public_attrs()
        self.set_private_methods()
        self.set_derived_methods()
        self.set_public_methods()
        self.attrs: List[str] = (
            self.private_attrs + self.public_attrs + self.derived_attrs
        )
        self.methods: List[str] = (
            self.private_methods + self.public_methods + self.derived_methods
        )

    @property
    def use_properties(self) -> bool:
        return self._use_properties

    @use_properties.setter
    def use_properties(self, use_properties: bool) -> None:
        self._use_properties: bool = use_properties

    def strip_underscores(self, item) -> str:
        return item.strip("_")

    def is_not_dunder(self, item) -> bool:
        return not item.startswith("__") and not item.endswith("__")

    def is_public(self, item) -> bool:
        return not item.startswith("_") and not item.endswith("_")

    def is_private(self, item) -> bool:
        return item.startswith("_") and self.is_not_dunder(item)

    def is_derived(self, item) -> bool:
        return item.endswith("_") and self.is_not_dunder(item)

    def is_method(self, item) -> bool:
        return callable(getattr(self.obj, item))

    def set_private_attrs(self) -> None:
        self.private_attrs: List[str] = [
            item
            for item in self.dir_list
            if self.is_private(item) and not self.is_method(item)
        ]

    def set_derived_attrs(self) -> None:
        self.derived_attrs: List[str] = [
            item
            for item in self.dir_list
            if self.is_derived(item) and not self.is_method(item)
        ]

    def set_public_attrs(self) -> None:
        self.public_attrs: List[str] = [
            item
            for item in self.dir_list
            if self.is_public(item) and not self.is_method(item)
        ]

    def set_private_methods(self) -> None:
        self.private_methods: List[str] = [
            item
            for item in self.dir_list
            if self.is_private(item) and self.is_method(item)
        ]

    def set_derived_methods(self) -> None:
        self.derived_methods: List[str] = [
            item
            for item in self.dir_list
            if self.is_derived(item) and self.is_method(item)
        ]

    def set_public_methods(self) -> None:
        self.public_methods: List[str] = [
            item
            for item in self.dir_list
            if self.is_public(item) and self.is_method(item)
        ]

    def get_private_attrs(self) -> List[str]:
        return self.private_attrs

    def get_derived_attrs(self) -> List[str]:
        return self.derived_attrs

    def get_public_attrs(self) -> List[str]:
        return self.public_attrs

    def get_attrs(self) -> List[str]:
        return self.attrs

    def get_private_methods(self) -> List[str]:
        return self.private_methods

    def get_derived_methods(self) -> List[str]:
        return self.derived_methods

    def get_public_methods(self) -> List[str]:
        return self.public_methods

    def get_methods(self) -> List[str]:
        return self.methods

    def get_item_type(self, item) -> str:
        return type(getattr(self.obj, item)).__name__

    def get_setter(self, item: str) -> str:
        item_no_underscores = self.strip_underscores(item)
        item_type: str = self.get_item_type(item)
        property_method: str = (
            f"@{item_no_underscores}.setter\n"
            + f"def {item_no_underscores}(self, {item_no_underscores}: {item_type}) -> None:"
            + f"\n    self.{item}: {item_type} = {item_no_underscores}\n\n"
        )
        setter_method: str = (
            f"def set_{item_no_underscores}(self, {item_no_underscores}: {item_type}) -> None:"
            + f"\n    self.{item}: {item_type} = {item_no_underscores}\n\n"
        )
        if self.use_properties:
            return property_method
        return setter_method

    def get_getter(self, item: str) -> str:
        item_no_underscores: str = self.strip_underscores(item)
        item_type: str = self.get_item_type(item)
        property_method: str = (
            "@property\n"
            + f"def {item_no_underscores}(self) -> {item_type}:"
            + f"\n    return self.{item}\n"
        )
        getter_method: str = (
            f"def get_{item_no_underscores}(self) -> {item_type}:"
            + f"\n    return self.{item}\n"
        )
        if self.use_properties:
            return property_method
        return getter_method

    def get_setter_getter_methods(self, item) -> str:
        if self.is_derived(item):
            setter = ""
        else:
            setter: str = self.get_setter(item)
        getter: str = self.get_getter(item)
        return getter + setter

    def get_primary_methods(self, item_list) -> List[str]:
        return [self.get_setter_getter_methods(item) for item in item_list]

    def get_init_setter(self, item: str) -> str:
        item_no_underscores = self.strip_underscores(item)
        item_type: str = self.get_item_type(item)
        if self.is_derived(item):
            return ""
        if self.use_properties:
            return f"self.item: {item_type} = {item_no_underscores}"
        else:
            return f"self.set_{item_no_underscores}({item_no_underscores})"

    def get_init_setters(self) -> str:
        s = "\n    "
        init_args = f"def __init__({s}self,"
        init_setters = ""
        for attr in self.get_attrs():
            if self.is_derived(attr):
                continue
            attr_type: str = self.get_item_type(attr)
            init_args += f"{s}{self.strip_underscores(attr)}: {attr_type},"
            init_setters += f"{s}{self.get_init_setter(attr)}"
        init_args += "\n) -> None:"
        return init_args + init_setters + "\n"

    def get_attrs_docstrings(self) -> str:
        s = "\n    "
        attr_docstrings = "Attributes:"
        for attr in self.get_attrs():
            attr_docstrings += (
                f"{s}{attr}: {type(getattr(self.obj, attr)).__name__}"
            )
        return attr_docstrings + "\n"

    def get_methods_docstrings(self) -> str:
        s = "\n    "
        method_docstrings = "Methods:"
        for method_name in self.get_methods():
            method = getattr(self.obj, method_name)
            method_docstrings += f"{s}{method_name}{inspect.signature(method)}"
        return method_docstrings

    def print_docstring(self) -> None:
        print(f"{self.class_name} class\n")
        print(self.get_attrs_docstrings())
        print(self.get_methods_docstrings())

    def print_primary_methods(self) -> None:
        for i in self.get_primary_methods(self.get_attrs()):
            print(i)

    def print_init_setters(self) -> None:
        print(self.get_init_setters())
