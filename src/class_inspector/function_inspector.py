import inspect
import logging
import os
import re
from typing import Callable

import attr
from attr.validators import instance_of
from dotenv import load_dotenv

from ._logger import compress_logging_value, setup_logger

load_dotenv()

if os.getenv("ENABLE_LOGGING", "false").lower() == "true":
    setup_logger(__file__, 2)

logger = logging.getLogger()


@attr.define
class FunctionInspector:
    """A function inspector class for analysing functions and methods as well as
    writing test stubs
    """

    obj: Callable = attr.ib(init=False, validator=[instance_of(Callable)])  # type: ignore
    name: str = attr.ib(init=False, validator=[instance_of(str)])
    doc: str = attr.ib(init=False, validator=[instance_of(str)])
    parameters: dict = attr.ib(init=False, validator=[instance_of(dict)])
    return_annotation: str = attr.ib(init=False, validator=[instance_of(str)])
    is_method: int = attr.ib(init=False, validator=[instance_of(int)])
    tab: str = attr.ib(default="    ", validator=instance_of(str), init=False)  # type: ignore

    def analyse(self, object_) -> None:
        """
        Analyze the given object to extract information such as name, documentation,
        parameters, and return annotation.

        Args:
            object_ (Callable): The callable object to be analysed.
        """
        for key, val in locals().items():
            logger.debug(f"{key} = {compress_logging_value(val)}")
        self.obj = object_
        self.name = self.obj.__name__
        self.doc = self._get_doc()
        self.parameters = {
            param.name: param.annotation
            for _, param in inspect.signature(self.obj).parameters.items()
        }
        self.return_annotation = self._get_return_annotations()
        self.tab: str = "    "
        # add 1 tab to the start of each line if obj is a method
        self.is_method = int(inspect.ismethod(self.obj))

    def add_boilerplate(
        self, add_guards: bool = True, add_debugs: bool = True
    ) -> str:
        """finds the last index of the doctsring if present and inserts
        the guard conditions in there

        Returns:
            str: the analysed function with added guard conditions
        """
        for key, val in locals().items():
            logger.debug(f"{key} = {compress_logging_value(val)}")
        # replace double quotes with single quotes as strings default to single quotes
        func_str = self._clean_func(
            str(inspect.getsource(self.obj)).replace('"', "'")
        )
        end_idx = self._find_string_end(
            func_str, self._get_docstring_patterns()
        )
        logger.debug(f"{func_str = }")
        logger.debug(f"{end_idx = }")

        if end_idx:
            if add_guards:
                func_str = self._insert_string_at_idx(
                    func_str, end_idx, self._get_guards()
                )
            if add_debugs:
                func_str = self._insert_string_at_idx(
                    func_str, end_idx, self._get_guards()
                )
        else:
            sig = self._get_func_sig() + "\n"

            if sig not in func_str:
                raise ValueError(f"sig not in function str: {sig} {func_str}")
            if add_guards:
                func_str = func_str.replace(sig, f"{sig}{self._get_guards()}")
            if add_debugs:
                func_str = func_str.replace(sig, f"{sig}{self._get_debugs()}")

            logger.debug(f"{sig = }")
        logger.debug(f"{func_str = }")
        return func_str + "\n\n"

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
        for key, val in locals().items():
            logger.debug(f"{key} = {compress_logging_value(val)}")
        test_full = ""
        test_full += self._get_parametrize_decorator(check_types, match)
        test_full += self._get_test_sig()
        test_full += self._get_test_body()
        test_full += "\n\n"
        return test_full

    def _get_doc(self) -> str:
        """
        Get the documentation string of the analysed object.

        Returns:
            str: The documentation string of the analysed object.
        """
        doc = inspect.getdoc(self.obj)
        if doc:
            return str(doc)
        return ""

    def _get_return_annotations(self) -> str:
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

    def _get_parametrize_decorator(
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
        for key, val in locals().items():
            logger.debug(f"{key} = {compress_logging_value(val)}")
        args = self._get_params_str()
        return (
            "@pytest.mark.parametrize(\n"
            + f'{self.tab}"{args}, expected_result, expected_context",\n'
            + f"{self.tab}[\n"
            + self._get_test_case(args)
            + (
                self._get_raises_type_error_test_case(args, check_types, match)
                * len(self.parameters)
            )
            + f"{self.tab}]\n)\n"
        )

    def _get_test_sig(self) -> str:
        """
        Get the signature string for generating a test function.

        Returns:
            str: The signature string for generating a test function.
        """
        sig = self._get_instance_sig() + self._get_params_str()
        return (
            f"def test_{self._strip_underscores(self.name)}"
            f"({sig}, expected_result, expected_context) -> None:\n"
        )

    def _get_test_body(self) -> str:
        """
        Generate the body of the test function.

        Returns:
            str: The body of the test function.
        """
        test_body = f"{self.tab}with expected_context:\n"
        test_body += f"{2*self.tab}assert "
        test_body += self._get_instance_call()
        if self.return_annotation != "None":
            test_body += "== expected_result\n"
        else:
            test_body += "is None\n"
        return test_body

    def _get_params_str(self) -> str:
        """
        Get a string representation of the parameters of the analysed object.

        Returns:
            str: A string representation of the parameters of the analysed object.
        """
        params = ", ".join(list(self.parameters.keys()))
        if params:
            return params  # + ", "
        return ""

    def _get_test_case(self, args: str) -> str:
        """
        Generate a test case for the test function.

        Args:
            args (str): The string representation of function arguments.

        Returns:
            str: The test case for the test function.
        """
        for key, val in locals().items():
            logger.debug(f"{key} = {compress_logging_value(val)}")
        return f"{self.tab * 2}({args}, expected_result, expected_context),\n"

    def _get_raises_type_error_test_case(
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
        for key, val in locals().items():
            logger.debug(f"{key} = {compress_logging_value(val)}")
        if not check_types:
            return ""
        match_stmt = ""
        if match:
            match_stmt = ', match=r""'
        return f"{self.tab * 2}({args}, None, pytest.raises(TypeError{match_stmt})),\n"

    def _strip_underscores(self, item: str) -> str:
        """
        Remove underscores from the given string.

        Args:
            item (str): The string from which underscores should be removed.

        Returns:
            str: The string without underscores.

        Raises:
            TypeError: If the input is not a string.
        """
        for key, val in locals().items():
            logger.debug(f"{key} = {compress_logging_value(val)}")
        if not isinstance(item, str):
            raise TypeError(f"item must be of type str, got {type(item)}")
        return item.strip("_")

    def _get_instance_sig(self) -> str:
        """
        Get the signature string for calling an instance method (if applicable).

        Returns:
            str: The signature string for calling an instance method.
        """
        if inspect.ismethod(self.obj):
            instance = self._camel_to_snake(self._get_class_name())
            return f"get_{instance}: {self._get_class_name()}, "
        if inspect.isfunction(self.obj):
            return ""
        return ""

    def _get_instance_call(self) -> str:
        """
        Generate a string representation for calling the analysed object.

        Returns:
            str: A string representation for calling the analysed object.
        """
        sig: str = self._get_params_str()
        if inspect.ismethod(self.obj):
            instance = self._camel_to_snake(self._get_class_name())
            return f"get_{instance}.{self.name}({sig}) "
        if inspect.isfunction(self.obj):
            return f"{self.name}({sig}) "
        return f"{self.name}({sig}) "

    def _get_params_types(self) -> str:
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

    def _camel_to_snake(self, name: str) -> str:
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    def _get_class_name(self) -> str:
        """
        Get the class name of the analysed object (if it's a method).

        Returns:
            str: The class name of the analysed object.
        """
        if inspect.ismethod(self.obj):
            return self.obj.__self__.__class__.__name__
        return self.name

    def _get_func_sig(self) -> str:
        """returns the function signature
        supports methods by inserting self as the first arg

        Returns:
            str: function signature
        """
        definition = "def "
        init_sig = str(inspect.signature(self.obj))

        if inspect.ismethod(self.obj):
            definition = definition.replace("def ", "    def ")
            init_sig = init_sig.replace("(", "(self, ").replace(", )", ")")

        sig = f"{definition}{self.name}" + init_sig + ":"
        return sig

    def _get_docstring_patterns(self) -> str:
        """
        Generate a regex pattern to match Python docstrings enclosed in triple quotes.

        This method creates a pattern that matches docstrings enclosed in either
        triple double quotes (\"\"\"...\"\"\") or triple single quotes ('''...''').

        Returns:
            str: A regex pattern that matches docstrings enclosed in triple quotes.
        """
        double_quotes = r'""".*?"""\n'
        single_quotes = r"'''.*?'''\n"
        return f"({double_quotes}|{single_quotes})"

    def _find_string_end(self, func_str: str, pattern: str) -> int | None:
        """
        Find the end index of the first match of a pattern in a string.

        This method searches for the given regex pattern in the provided string
        and returns the end index of the first match found.

        Args:
            func_str (str): The string in which to search for the pattern.
            pattern (str): The regex pattern to search for in the string.

        Returns:
            int | None: The end index of the first match if found, otherwise None.
        """
        for key, val in locals().items():
            logger.debug(f"{key} = {compress_logging_value(val)}")
        match = re.search(pattern, func_str, re.DOTALL)
        if match:
            return match.end()
        return None

    def _insert_string_at_idx(
        self, func_str: str, idx: int, to_insert: str
    ) -> str:
        """
        Insert a string at a specified index in another string.

        This method inserts the specified string `to_insert` into the given
        string `func_str` at the specified index `idx`.

        Args:
            func_str (str): The original string where the insertion will occur.
            idx (int): The index at which to insert the new string.
            to_insert (str): The string to be inserted into the original string.

        Returns:
            str: The modified string with `to_insert` inserted at the specified index.
        """
        for key, val in locals().items():
            logger.debug(f"{key} = {compress_logging_value(val)}")
        return func_str[:idx] + to_insert + func_str[idx:]

    def _get_guards(self) -> str:
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

        guards: str = (
            f"{self.tab*(1 + self.is_method)}if not all(["
            + ", ".join(
                [
                    f"isinstance({arg_name}, {arg_type.__name__})"
                    for arg_name, arg_type in self.parameters.items()
                ]
            )
            + "]):\n"
        )
        raises = (
            f"{self.tab*(2 + self.is_method)}raise TypeError(\n"
            + f'{self.tab*(3 + self.is_method)}"{self.name} '
            + f'expects arg types: [{expected_types}], "\n'
            + f'{self.tab*(3 + self.is_method)}f"received: [{received_types}]"\n'
            + f"{self.tab*(2 + self.is_method)})\n"
        )
        return guards + raises

    def _clean_func(self, func_str: str) -> str:
        for key, val in locals().items():
            logger.debug(f"{key} = {compress_logging_value(val)}")

        def replacer(match):
            content = match.group(1)
            cleaned_content = " ".join(content.split())
            logger.debug(f"{cleaned_content = }")
            return f"({cleaned_content})"

        return re.sub(r"\((.*?)\)", replacer, func_str, flags=re.DOTALL)

    def _get_debugs(self) -> str:
        if not self.parameters:
            return ""
        debugs = (
            f"{self.tab*(1 + self.is_method)}for key, val in locals().items():\n"
            f'{self.tab*(2 + self.is_method)}logger.debug(f"{{key}} = {{val}}")\n'
        )
        return debugs
