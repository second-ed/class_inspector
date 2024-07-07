import inspect
import logging
from typing import Any, Callable, Dict

import attr
from attr.validators import instance_of

from . import _utils as utils
from ._logger import (
    compress_logging_value,
    is_logging_enabled,
    setup_logger,
)

if is_logging_enabled(__file__):
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
        self.parameters = self._get_parameters()
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
        func_str = utils._clean_func(
            str(inspect.getsource(self.obj)).replace('"', "'")
        )
        end_idx = utils._find_string_end(
            func_str, utils._get_docstring_patterns()
        )
        logger.debug(f"func_str = {func_str}")
        logger.debug(f"end_idx = {end_idx}")

        if end_idx:
            if add_guards:
                func_str = utils._insert_string_at_idx(
                    func_str, end_idx, self._get_guards()
                )
            if add_debugs:
                func_str = utils._insert_string_at_idx(
                    func_str, end_idx, self._get_debugs()
                )
        else:
            sig = self._get_func_sig() + "\n"

            if sig not in func_str:
                raise ValueError(f"sig not in function str: {sig} {func_str}")
            if add_guards:
                func_str = func_str.replace(sig, f"{sig}{self._get_guards()}")
            if add_debugs:
                func_str = func_str.replace(sig, f"{sig}{self._get_debugs()}")
            if self.doc:
                func_str = func_str.replace(sig, f"{sig}{self.doc}")

            logger.debug(f"sig = {sig}")
        logger.debug(f"func_str = {func_str}")
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
        test_full = []
        test_full.append(self._get_parametrize_decorator(check_types, match))
        test_full.append(self._get_test_sig())
        test_full.append(self._get_test_body())
        test_full.append("\n\n")
        return "".join(test_full)

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

    def _get_parameters(self) -> Dict[str, Any]:
        return {
            param.name: param.annotation
            for _, param in inspect.signature(self.obj).parameters.items()
        }

    def _get_return_annotations(self) -> str:
        """
        Get the return annotation of the analysed object.

        Returns:
            str: The return annotation of the analysed object.
        """
        annot = inspect.signature(self.obj).return_annotation
        if annot is not inspect._empty and not utils._is_union_origin(annot):
            return utils._get_object_name(annot)
        if utils._is_union_origin(annot):
            return str(annot).replace("typing.", "")
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
            f"def test_{utils._strip_underscores(self.name)}"
            f"({sig}, expected_result, expected_context) -> None:\n"
        )

    def _get_test_body(self) -> str:
        """
        Generate the body of the test function.

        Returns:
            str: The body of the test function.
        """
        test_body = [f"{self.tab}with expected_context:\n"]
        test_body.append(f"{2*self.tab}assert ")
        test_body.append(self._get_instance_call())
        if self.return_annotation != "None":
            test_body.append("== expected_result\n")
        else:
            test_body.append("is None\n")
        return "".join(test_body)

    def _get_params_str(self) -> str:
        """
        Get a string representation of the parameters of the analysed object.

        Returns:
            str: A string representation of the parameters of the analysed object.
        """
        params = ", ".join(list(self.parameters.keys()))
        if params:
            return params
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

    def _get_instance_sig(self) -> str:
        """
        Get the signature string for calling an instance method (if applicable).

        Returns:
            str: The signature string for calling an instance method.
        """
        if inspect.ismethod(self.obj):
            instance = utils._camel_to_snake(self._get_class_name())
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
            instance = utils._camel_to_snake(self._get_class_name())
            return f"get_{instance}.{self.name}({sig}) "
        if inspect.isfunction(self.obj):
            return f"{self.name}({sig}) "
        return f"{self.name}({sig}) "

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

    def _get_guards(self) -> str:
        """
        Generate guards for type checking of function arguments.

        Returns:
            str: Guards for type checking of function arguments.
        """
        if not self.parameters:
            return ""
        expected_types = ", ".join(
            [utils._unpack_parameter(arg) for arg in self.parameters.values()]
        )
        received_types = ", ".join(
            [f"{{type({arg}).__name__}}" for arg in self.parameters.keys()]
        )

        guards: str = (
            f"{self.tab*(1 + self.is_method)}if not all(["
            + ", ".join(
                [
                    f"isinstance({arg_name}, {utils._unpack_parameter(arg_type)})"
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

    def _get_debugs(self) -> str:
        if not self.parameters:
            return ""
        debugs = (
            f"{self.tab*(1 + self.is_method)}for key, val in locals().items():\n"
            f'{self.tab*(2 + self.is_method)}logger.debug(f"{{key}} = {{val}}")\n'
        )
        return debugs
