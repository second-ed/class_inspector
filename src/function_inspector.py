import inspect


class FunctionInspector:
    def analyse(self, object_) -> None:
        self._object = object_
        self._name = self._object.__name__
        self._parameters = {
            v.name: v.annotation
            for k, v in inspect.signature(self._object).parameters.items()
        }
        self._return_annotations = self.get_return_annotations()
        self._t: str = "    "

    def get_return_annotations(self) -> str:
        annot = inspect.signature(self._object).return_annotation
        if annot is not inspect._empty:
            return str(annot)
        return "None"

    def get_params_str(self) -> str:
        return ", ".join(list(self._parameters.keys()))

    def get_params_types(self) -> str:
        return ", ".join(
            [
                t.__name__ if hasattr(t, "__name__") else "no_type"
                for t in self._parameters.values()
            ]
        )

    def get_class_name(self) -> str:
        return self._object.__self__.__class__.__name__

    def strip_underscores(self, item: str) -> str:
        return item.strip("_")

    def get_instance_sig(self) -> str:
        if inspect.ismethod(self._object):
            return f"get_instance: {self.get_class_name()}, "
        elif inspect.isfunction(self._object):
            return ""
        return ""

    def get_test_values_sig(self) -> str:
        sig = self.get_instance_sig() + self.get_params_str()
        return f"def test_values_{self.strip_underscores(self._name)}({sig}, expected_result) -> None:\n"

    def get_test_types_sig(self) -> str:
        sig = self.get_instance_sig() + self.get_params_str()
        return f"def test_types_{self.strip_underscores(self._name)}({sig}) -> None:\n"

    def get_parametrize_decorator_values(self) -> str:
        args = self.get_params_str()
        return (
            "@pytest.mark.parametrize(\n"
            + f'{self._t}"{args}, expected_result",\n'
            + f"{self._t}[\n{self._t * 2}({args}, expected_result),"
            + f"\n{self._t}]\n)\n"
        )

    def get_parametrize_decorator_types(self) -> str:
        args: str = self.get_params_str()
        types: str = self.get_params_types()
        types_parametrized = f"{self._t * 2}({types}),\n" * len(self._parameters)
        return (
            f'@pytest.mark.parametrize(\n{self._t}"{args}",\n'
            + f'{self._t}[\n{types_parametrized}{self._t}]\n)\n'
        )

    def get_instance_call(self) -> str:
        sig: str = self.get_params_str()
        if inspect.ismethod(self._object):
            return f"get_instance.{self._name}({sig}) "
        elif inspect.isfunction(self._object):
            return f"{self._name}({sig}) "
        return f"{self._name}({sig}) "

    def get_test_body(self) -> str:
        test_body = f"{self._t}"
        test_body += self.get_instance_call()
        if self._return_annotations != "None":
            test_body += "== expected_result\n"
        else:
            test_body += "is None\n"
        return test_body

    def get_test_values(self) -> str:
        return (
            self.get_parametrize_decorator_values()
            + self.get_test_values_sig()
            + self.get_test_body()
            + "\n\n"
        )

    def get_test_raises_type_error(self) -> str:
        return (
            self.get_parametrize_decorator_types()
            + self.get_test_types_sig()
            + f"{self._t}with pytest.raises(TypeError):\n"
            + f"{self._t * 2}{self.get_instance_call()}\n\n\n"
        )

    def get_tests(self) -> str:
        if self._parameters:
            return self.get_test_values() + self.get_test_raises_type_error()
        return ""

