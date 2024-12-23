import inspect

from class_inspector.cst_walkers import (
    AddBoilerplateTransformer,
    FuncVisitor,
)
from class_inspector.utils import (
    format_code_str,
    str_to_cst,
)
from mock_package.mock_module import mock_function


def test_add_boilerplate_transformer():
    module = str_to_cst(format_code_str(inspect.getsource(mock_function)))
    vistor = FuncVisitor()
    module.visit(vistor)
    transformer = AddBoilerplateTransformer(vistor.funcs, True, True)
    modified_module = module.visit(transformer)
    assert format_code_str(modified_module.code) == (
        'def mock_function(\n    param1: float, param2: int, param3: bool, param4: str = "test"\n) -> float:\n'
        "    logger.debug(locals())\n    if not all(\n"
        "        [\n"
        "            isinstance(param1, float),\n"
        "            isinstance(param2, int),\n"
        "            isinstance(param3, bool),\n"
        "            isinstance(param4, str),\n"
        "        ]\n    ):\n"
        '        raise TypeError(\n            "mock_function expects arg types: [float, int, bool, str], "\n'
        '            f"received: [{type(param1).__name__}, {type(param2).__name__}, {type(param3).__name__}, {type(param4).__name__}]"\n        )\n'
        "    if param3:\n"
        "        return param1 - param2\n"
        "    else:\n"
        "        return param1 + param2\n"
    )
