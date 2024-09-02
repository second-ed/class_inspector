import attr
from attr.validators import deep_iterable, instance_of

from class_inspector import _type_hint_utils as thu


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

    def _get_deep_iterable(self, attr_type: str) -> str:
        """
        Generate a deep iterable validator string.

        Args:
            attr_type (str): The attribute type string.

        Returns:
            str: The deep iterable validator string.

        Raises:
            TypeError: If the input is not a string.
        """
        if not all([isinstance(attr_type, str)]):
            raise TypeError(
                "get_deep_iterable expects arg types: [str], "
                f"received: [{type(attr_type).__name__}]"
            )
        inner_type, outer_type = thu.get_inner_outer_types(attr_type)
        return (
            f"deep_iterable(member_validator=instance_of({inner_type}),"
            f" iterable_validator=instance_of({outer_type}))"
        )

    def _get_deep_mapping(self, attr_type: str) -> str:
        """
        Generate a deep mapping validator string.

        Args:
            attr_type (str): The attribute type string.

        Returns:
            str: The deep mapping validator string.

        Raises:
            TypeError: If the input is not a string.
        """
        if not all([isinstance(attr_type, str)]):
            raise TypeError(
                "get_deep_mapping expects arg types: [str], "
                f"received: [{type(attr_type).__name__}]"
            )
        inner_type, outer_type = thu.get_inner_outer_types(attr_type)
        inner_k, inner_v = inner_type.split(", ")
        return (
            f"deep_mapping(key_validator=instance_of({inner_k}), "
            f"value_validator=instance_of({inner_v}), "
            f"mapping_validator=instance_of({outer_type}))"
        )

    def _get_validator(self, attr_type: str) -> str:
        """
        Get the appropriate validator string for the attribute type.

        Args:
            attr_type (str): The attribute type string.

        Returns:
            str: The validator string for the attribute type.

        Raises:
            TypeError: If the input is not a string.
            NotImplementedError: If the attribute type is not implemented.
        """
        if not all([isinstance(attr_type, str)]):
            raise TypeError(
                "get_validator expects arg types: [str], "
                f"received: [{type(attr_type).__name__}]"
            )
        if not thu.contains_square_brackets(attr_type):
            return f"instance_of({attr_type})"
        if thu.is_deep_iterable(attr_type):
            return self._get_deep_iterable(attr_type)
        if thu.is_deep_mapping(attr_type):
            return self._get_deep_mapping(attr_type)
        raise NotImplementedError(f"{attr_type} is not implemented")

    def _get_init_bool(self, attr_init: bool) -> str:
        """
        Get the init boolean string for attribute initialization.

        Args:
            attr_init (bool): The attribute initialization boolean.

        Returns:
            str: The init boolean string.

        Raises:
            TypeError: If the input is not a boolean.
        """
        if not all([isinstance(attr_init, bool)]):
            raise TypeError(
                "get_type_hint expects arg types: [str], "
                f"received: [{type(attr_init).__name__}]"
            )
        if attr_init:
            return ""
        return f", init={attr_init}"

    def _get_imports(self) -> str:
        """
        Get import statements required for generating the class.

        Returns:
            str: The import statements.
        """
        return (
            "import attr\nfrom attr.validators "
            "import instance_of, deep_iterable, deep_mapping\n\n"
        )

    def _get_class_sig(self) -> str:
        """
        Get the class signature string.

        Returns:
            str: The class signature string.
        """
        return f"@attr.define\nclass {self.class_name}:"

    def _get_attrib(
        self, attr_name: str, attr_type: str, attr_init: bool
    ) -> str:
        """
        Generate attribute string with type hint and validator.

        Args:
            attr_name (str): The attribute name.
            attr_type (str): The attribute type string.
            attr_init (bool): The attribute initialization boolean.

        Returns:
            str: The attribute string.

        Raises:
            TypeError: If the inputs are not of the correct types.
        """
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

        init_true = self._get_init_bool(attr_init)
        return (
            f"    {attr_name}: {thu.get_type_hint(attr_type)} = "
            f"attr.ib(validator=[{self._get_validator(attr_type)}]{init_true})"
        )

    def _get_attr_class(self) -> str:
        """
        Generate the entire class string with attributes and validators.

        Returns:
            str: The complete class string.
        """
        class_str = []
        class_str.append(self._get_imports())
        class_str.append(self._get_class_sig())
        for at_dict in self.attributes:
            if isinstance(at_dict, dict):
                at_map = AttrMap(**at_dict)
            elif isinstance(at_dict, AttrMap):
                at_map = at_dict
            class_str.append(
                self._get_attrib(
                    at_map.attr_name, at_map.attr_type, at_map.attr_init
                )
            )
        return "\n".join(class_str)
