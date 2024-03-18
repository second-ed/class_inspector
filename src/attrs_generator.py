from typing import List


class AttrInspector:
    def __init__(self, obj: object) -> None:
        self.obj: object = obj
        self.dir_list: List[str] = list(vars(obj))
        self.class_name: str = type(self.obj).__name__
        self.set_attrs()

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

    def get_item_type(self, item) -> str:
        return type(getattr(self.obj, item)).__name__

    def set_attrs(self) -> None:
        self._attrs: List[str] = [
            item
            for item in self.dir_list
            if not self.is_method(item) and self.is_not_dunder(item)
        ]

    def get_imports(self) -> str:
        return "import attr\n\n"

    def get_class_signature(self) -> str:
        return f"@attr.s\nclass {self.class_name}:"

    def get_validated_attr(self, item) -> str:
        item_type: str = self.get_item_type(item)
        return f"    {self.strip_underscores(item)}: {item_type} = attr.ib(\n        validator=[attr.validators.instance_of({item_type})],\n        on_setattr = attr.setters.validate\n    )"

    def print_attrs_class(self) -> None:
        print(self.get_imports())
        print(self.get_class_signature())
        for item in self._attrs:
            print(self.get_validated_attr(item))
