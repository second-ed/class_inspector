import inspect
import re
from typing import Callable

import attr
from attr.validators import instance_of


@attr.define
class FunctionInspector:
    """A function inspector class for analysing functions and methods as well as
    writing test stubs
    """

    name: str = attr.ib(init=False, validator=[instance_of(str)])
    doc: str = attr.ib(init=False, validator=[instance_of(str)])
    parameters: dict = attr.ib(init=False, validator=[instance_of(dict)])
    return_annotation: str = attr.ib(init=False, validator=[instance_of(str)])
    tab: str = attr.ib(default="    ", validator=instance_of(str), init=False)  # type: ignore
    obj: Callable = attr.ib(init=False)

    def analyse(self, object_) -> None:
        """
        Analyze the given object to extract information such as name, documentation,
        parameters, and return annotation.

        Args:
            object_ (Callable): The callable object to be analysed.
        """
        self.obj = object_
        self.name = self.obj.__name__
        self.doc = self.get_doc()
        self.parameters = {
            v.name: v.annotation
            for k, v in inspect.signature(self.obj).parameters.items()
        }
        self.return_annotation = self.get_return_annotations()
        self.tab: str = "    "

    def get_doc(self) -> str:
        """
        Get the documentation string of the analysed object.

        Returns:
            str: The documentation string of the analysed object.
        """
        doc = inspect.getdoc(self.obj)
        if doc:
            return str(doc)
        return ""

    def get_return_annotations(self) -> str:
        """
        Get the return annotation of the analysed object.

        Returns:
            str: The return annotation of the analysed object.
        """
        annot = inspect.signature(self.obj).return_annotation
        if annot is not inspect._empty:
            if hasattr(annot, "__name__"):
                return annot.__name__
            return str(annot)
        return "None"

    def get_params_str(self) -> str:
        """
        Get a string representation of the parameters of the analysed object.

        Returns:
            str: A string representation of the parameters of the analysed object.
        """
        params = ", ".join(list(self.parameters.keys()))
        if params:
            return params  # + ", "
        return ""

    def get_params_types(self) -> str:
        """
        Get a string representation of the types of the parameters of the analysed
        object.

        Returns:
            str: A string representation of the types of the parameters of the
                analysed object.
        """
        return ", ".join(
            [
                t_.__name__ if hasattr(t_, "__name__") else "no_type"
                for t_ in self.parameters.values()
            ]
        )

    def get_class_name(self) -> str:
        """
        Get the class name of the analysed object (if it's a method).

        Returns:
            str: The class name of the analysed object.
        """
        if inspect.ismethod(self.obj):
            return self.obj.__self__.__class__.__name__
        return self.name

    def strip_underscores(self, item: str) -> str:
        """
        Remove underscores from the given string.

        Args:
            item (str): The string from which underscores should be removed.

        Returns:
            str: The string without underscores.

        Raises:
            TypeError: If the input is not a string.
        """
        if not isinstance(item, str):
            raise TypeError(f"item must be of type str, got {type(item)}")
        return item.strip("_")

    def get_instance_sig(self) -> str:
        """
        Get the signature string for calling an instance method (if applicable).

        Returns:
            str: The signature string for calling an instance method.
        """
        if inspect.ismethod(self.obj):
            return f"get_instance: {self.get_class_name()}, "
        if inspect.isfunction(self.obj):
            return ""
        return ""

    def get_test_sig(self) -> str:
        """
        Get the signature string for generating a test function.

        Returns:
            str: The signature string for generating a test function.
        """
        sig = self.get_instance_sig() + self.get_params_str()
        return (
            f"def test_{self.strip_underscores(self.name)}"
            f"({sig}, expected_result, expected_context) -> None:\n"
        )

    def get_parametrize_decorator(
        self, check_types: bool = True, match: bool = False
    ) -> str:
        """
        Generate a parametrize decorator for the test function.

        Args:
            check_types (bool): Whether to include type checking in the test cases.
            match (bool): Whether to include match pattern in the test cases.

        Returns:
            str: The parametrize decorator for the test function.
        """
        args = self.get_params_str()
        return (
            "@pytest.mark.parametrize(\n"
            + f'{self.tab}"{args}, expected_result, expected_context",\n'
            + f"{self.tab}[\n"
            + self.get_test_case(args)
            + (
                self.get_raises_type_error_test_case(args, check_types, match)
                * len(self.parameters)
            )
            + f"{self.tab}]\n)\n"
        )

    def get_test_case(self, args: str) -> str:
        """
        Generate a test case for the test function.

        Args:
            args (str): The string representation of function arguments.

        Returns:
            str: The test case for the test function.
        """
        return f"{self.tab * 2}({args}, expected_result, expected_context),\n"

    def get_raises_type_error_test_case(
        self, args: str, check_types: bool = True, match: bool = False
    ) -> str:
        """
        Generate a test case for raising a type error in the test function.

        Args:
            args (str): The string representation of function arguments.
            check_types (bool): Whether to include type checking in the test cases.
            match (bool): Whether to include match pattern in the test cases.

        Returns:
            str: The test case for raising a type error in the test function.
        """
        if not check_types:
            return ""
        match_stmt = ""
        if match:
            match_stmt = ', match=r""'
        return f"{self.tab * 2}({args}, None, pytest.raises(TypeError{match_stmt})),\n"

    def get_instance_call(self) -> str:
        """
        Generate a string representation for calling the analysed object.

        Returns:
            str: A string representation for calling the analysed object.
        """
        sig: str = self.get_params_str()
        if inspect.ismethod(self.obj):
            return f"get_instance.{self.name}({sig}) "
        if inspect.isfunction(self.obj):
            return f"{self.name}({sig}) "
        return f"{self.name}({sig}) "

    def get_test_body(self) -> str:
        """
        Generate the body of the test function.

        Returns:
            str: The body of the test function.
        """
        test_body = f"{self.tab}with expected_context:\n"
        test_body += f"{2*self.tab}assert "
        test_body += self.get_instance_call()
        if self.return_annotation != "None":
            test_body += "== expected_result\n"
        else:
            test_body += "is None\n"
        return test_body

    def get_test(self, check_types: bool = True, match: bool = False) -> str:
        """
        Generate the complete test function.

        Args:
            check_types (bool): Whether to include type checking in the test
                function.
            match (bool): Whether to include match pattern in the test function.

        Returns:
            str: The complete test function.
        """
        test_full = ""
        test_full += self.get_parametrize_decorator(check_types, match)
        test_full += self.get_test_sig()
        test_full += self.get_test_body()
        test_full += "\n\n"
        return test_full

    def get_func_sig(self) -> str:
        definition = "def "
        init_sig = str(inspect.signature(self.obj))

        if inspect.ismethod(self.obj):
            definition = definition.replace("def ", "    def ")
            init_sig = init_sig.replace("(", "(self, ").replace(", )", ")")

        sig = f"{definition}{self.name}" + init_sig + ":"
        return sig

    def get_docstring_patterns(self) -> str:
        double_quotes = r'""".*?"""\n'
        single_quotes = r"'''.*?'''\n"
        return f"({double_quotes}|{single_quotes})"

    def find_string_end(self, func_str: str, pattern: str) -> int | None:
        match = re.search(pattern, func_str, re.DOTALL)
        if match:
            return match.end()
        return None

    def insert_string_at_idx(
        self, func_str: str, idx: int, to_insert: str
    ) -> str:
        return func_str[:idx] + to_insert + func_str[idx:]

    def get_guards(self) -> str:
        """
        Generate guards for type checking of function arguments.

        Returns:
            str: Guards for type checking of function arguments.
        """
        if not self.parameters:
            return ""
        expected_types = ", ".join(
            [arg.__name__ for arg in self.parameters.values()]
        )
        received_types = ", ".join(
            [f"{{type({arg}).__name__}}" for arg in self.parameters.keys()]
        )

        # add 1 tab to the start of each line if obj is a method
        is_method = int(inspect.ismethod(self.obj))

        guards: str = (
            f"{self.tab*(1 + is_method)}if not all(["
            + ", ".join(
                [
                    f"isinstance({k}, {v.__name__})"
                    for k, v in self.parameters.items()
                ]
            )
            + "]):\n"
        )
        raises = (
            f"{self.tab*(2 + is_method)}raise TypeError(\n"
            + f'{self.tab*(3 + is_method)}"{self.name} expects arg types: [{expected_types}], "\n'
            + f'{self.tab*(3 + is_method)}f"received: [{received_types}]"\n'
            + f"{self.tab*(2 + is_method)})\n"
        )
        return guards + raises

    def add_guards(self) -> str:
        func_str = str(inspect.getsource(self.obj))
        end_idx = self.find_string_end(func_str, self.get_docstring_patterns())

        if end_idx:
            func_str = self.insert_string_at_idx(
                func_str, end_idx, self.get_guards()
            )
        else:
            sig = self.get_func_sig() + "\n"
            func_str = func_str.replace(sig, (sig + self.get_guards()))

        return func_str + "\n\n"
