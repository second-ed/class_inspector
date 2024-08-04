from typing import List

import pytest
from class_inspector.attr_generator import AttrGenerator, AttrMap
from class_inspector.class_inspector import ClassInspector

from tests.mock_package import mock_utils_c
from tests.mock_package.mock_service import MockService


class TestClass:
    def __init__(self, x: int, y: float) -> None:
        self._x: int = x
        self.y: float = y
        self.z_: bool = x > y

    def do_something(self) -> bool:
        return self.z_

    def _do_something_internally(self) -> float:
        return self._x - self.y

    def do_something_derived_(self) -> bool:
        return self._x != self.z_

    def do_something_with_args(self, a, b):
        return a + b


@pytest.fixture
def get_test_class() -> TestClass:
    return TestClass(20, 3.14)


@pytest.fixture
def get_instance(get_test_class: TestClass) -> ClassInspector:
    return ClassInspector(get_test_class)


@pytest.fixture
def get_attr_gen_attributes() -> List[AttrMap]:
    return [
        AttrMap("test1", "int", True),
        AttrMap("test2", "float", False),
        AttrMap("test3", "bool", True),
        AttrMap("test4", "str", False),
        AttrMap("test5", "List[int]", True),
        AttrMap("test6", "Dict[str, float]", False),
    ]


@pytest.fixture
def get_attr_gen_instance(
    get_attr_gen_attributes: List[AttrMap],
) -> AttrGenerator:
    return AttrGenerator("TestClass", get_attr_gen_attributes)


@pytest.fixture
def get_fixture_sorted_callables_by_line_numbers():
    return {
        "main": mock_utils_c.main,
        "read_data": mock_utils_c.read_data,
        "check_extension": mock_utils_c.check_extension,
        "clean_data": mock_utils_c.clean_data,
        "_transform_data": mock_utils_c._transform_data,
        "rename_data": mock_utils_c.rename_data,
        "merge_data": mock_utils_c.merge_data,
        "save_data": mock_utils_c.save_data,
        "filepath_exists": mock_utils_c.filepath_exists,
    }


@pytest.fixture
def get_fixture_unsorted_callables_by_line_numbers():
    return {
        "clean_data": mock_utils_c.clean_data,
        "check_extension": mock_utils_c.check_extension,
        "main": mock_utils_c.main,
        "read_data": mock_utils_c.read_data,
        "_transform_data": mock_utils_c._transform_data,
        "filepath_exists": mock_utils_c.filepath_exists,
        "merge_data": mock_utils_c.merge_data,
        "save_data": mock_utils_c.save_data,
        "rename_data": mock_utils_c.rename_data,
    }


@pytest.fixture
def get_mock_service_instance():
    return MockService()


@pytest.fixture
def get_unsorted_mock_service_methods(get_mock_service_instance):
    return {
        "validate_data": get_mock_service_instance.validate_data,
        "process_data": get_mock_service_instance.process_data,
        "save_data": get_mock_service_instance.save_data,
        "fetch_data": get_mock_service_instance.fetch_data,
    }


@pytest.fixture
def get_sorted_mock_service_methods(get_mock_service_instance):
    return {
        "fetch_data": get_mock_service_instance.fetch_data,
        "process_data": get_mock_service_instance.process_data,
        "validate_data": get_mock_service_instance.validate_data,
        "save_data": get_mock_service_instance.save_data,
    }


@pytest.fixture
def get_mock_utils_c_with_guards():
    return (
        "def main(filepath: str) -> bool:\n"
        "    if not all([isinstance(filepath, str)]):\n"
        "        raise TypeError(\n"
        '            "main expects arg types: [str], "\n'
        '            f"received: [{type(filepath).__name__}]"\n'
        "        )\n"
        "    data = read_data(filepath)\n"
        "    data = clean_data(data)\n"
        "    data_dict = _transform_data(data)\n"
        "\n"
        "    for key, value in data_dict.items():\n"
        "        data_dict[key] = rename_data(value)\n"
        "\n"
        "    merged_data = merge_data(data_dict)\n"
        "\n"
        "    return save_data(merged_data, filepath)\n"
        "\n"
        "\n"
        "def read_data(filepath: str):\n"
        "    if not all([isinstance(filepath, str)]):\n"
        "        raise TypeError(\n"
        '            "read_data expects arg types: [str], "\n'
        '            f"received: [{type(filepath).__name__}]"\n'
        "        )\n"
        "    if check_extension(filepath):\n"
        "        return pd.DataFrame({})\n"
        "    raise FileNotFoundError\n"
        "\n"
        "\n"
        "def check_extension(filepath: str) -> bool:\n"
        "    '''this is a docstring\n"
        "\n"
        "    Args:\n"
        "        filepath (str): the filepath to check\n"
        "\n"
        "    Returns:\n"
        "        bool: if the extension is valid\n"
        "    '''\n"
        "    if not all([isinstance(filepath, str)]):\n"
        "        raise TypeError(\n"
        '            "check_extension expects arg types: [str], "\n'
        '            f"received: [{type(filepath).__name__}]"\n'
        "        )\n"
        "    return bool(filepath)\n"
        "\n"
        "\n"
        "def clean_data(data):\n"
        "    return data\n"
        "\n"
        "\n"
        "def _transform_data(data) -> dict:\n"
        "    def transform() -> dict:\n"
        "        return {'data': data}\n"
        "\n"
        "    return transform()\n"
        "\n"
        "\n"
        "def rename_data(value) -> str:\n"
        "    def replacer(match) -> str:\n"
        "        content = match.group(1)\n"
        "        cleaned_content = ' '.join(content.split())\n"
        "        return f'({cleaned_content})'\n"
        "\n"
        "    return re.sub(r'\\((.*?)\\)', replacer, str(value.iloc[0, 0]), flags=re.DOTALL\n"
        "    )\n"
        "\n"
        "\n"
        "def merge_data(data_dict: Dict):\n"
        "    if not all([isinstance(data_dict, dict)]):\n"
        "        raise TypeError(\n"
        '            "merge_data expects arg types: [dict], "\n'
        '            f"received: [{type(data_dict).__name__}]"\n'
        "        )\n"
        "    # this is an inline comment that hopefully will stay\n"
        "    data = pd.concat([v for v in data_dict.values()])\n"
        "    return data\n"
        "\n"
        "\n"
        "def save_data(data, filepath: str) -> bool:\n"
        "    if not all([isinstance(filepath, str)]):\n"
        "        raise TypeError(\n"
        '            "save_data expects arg types: [str], "\n'
        '            f"received: [{type(filepath).__name__}]"\n'
        "        )\n"
        "    if filepath_exists(filepath):\n"
        "        return True\n"
        "    return False\n"
        "\n"
        "\n"
        "def filepath_exists(filepath: str) -> bool:\n"
        "    if not all([isinstance(filepath, str)]):\n"
        "        raise TypeError(\n"
        '            "filepath_exists expects arg types: [str], "\n'
        '            f"received: [{type(filepath).__name__}]"\n'
        "        )\n"
        "    return bool(filepath)\n"
        "\n"
        "\n"
    )


@pytest.fixture
def get_mock_utils_c_with_debugs():
    return (
        "def main(filepath: str) -> bool:\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    data = read_data(filepath)\n"
        "    data = clean_data(data)\n"
        "    data_dict = _transform_data(data)\n"
        "\n"
        "    for key, value in data_dict.items():\n"
        "        data_dict[key] = rename_data(value)\n"
        "\n"
        "    merged_data = merge_data(data_dict)\n"
        "\n"
        "    return save_data(merged_data, filepath)\n"
        "\n"
        "\n"
        "def read_data(filepath: str):\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    if check_extension(filepath):\n"
        "        return pd.DataFrame({})\n"
        "    raise FileNotFoundError\n"
        "\n"
        "\n"
        "def check_extension(filepath: str) -> bool:\n"
        "    '''this is a docstring\n"
        "\n"
        "    Args:\n"
        "        filepath (str): the filepath to check\n"
        "\n"
        "    Returns:\n"
        "        bool: if the extension is valid\n"
        "    '''\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    return bool(filepath)\n"
        "\n"
        "\n"
        "def clean_data(data):\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    return data\n"
        "\n"
        "\n"
        "def _transform_data(data) -> dict:\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    def transform() -> dict:\n"
        "        return {'data': data}\n"
        "\n"
        "    return transform()\n"
        "\n"
        "\n"
        "def rename_data(value) -> str:\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    def replacer(match) -> str:\n"
        "        content = match.group(1)\n"
        "        cleaned_content = ' '.join(content.split())\n"
        "        return f'({cleaned_content})'\n"
        "\n"
        "    return re.sub(r'\\((.*?)\\)', replacer, str(value.iloc[0, 0]), flags=re.DOTALL\n"
        "    )\n"
        "\n"
        "\n"
        "def merge_data(data_dict: Dict):\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    # this is an inline comment that hopefully will stay\n"
        "    data = pd.concat([v for v in data_dict.values()])\n"
        "    return data\n"
        "\n"
        "\n"
        "def save_data(data, filepath: str) -> bool:\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    if filepath_exists(filepath):\n"
        "        return True\n"
        "    return False\n"
        "\n"
        "\n"
        "def filepath_exists(filepath: str) -> bool:\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    return bool(filepath)\n"
        "\n"
        "\n"
    )


@pytest.fixture
def get_mock_utils_c_with_guards_and_debugs():
    return (
        "def main(filepath: str) -> bool:\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    if not all([isinstance(filepath, str)]):\n"
        "        raise TypeError(\n"
        '            "main expects arg types: [str], "\n'
        '            f"received: [{type(filepath).__name__}]"\n'
        "        )\n"
        "    data = read_data(filepath)\n"
        "    data = clean_data(data)\n"
        "    data_dict = _transform_data(data)\n"
        "\n"
        "    for key, value in data_dict.items():\n"
        "        data_dict[key] = rename_data(value)\n"
        "\n"
        "    merged_data = merge_data(data_dict)\n"
        "\n"
        "    return save_data(merged_data, filepath)\n"
        "\n"
        "\n"
        "def read_data(filepath: str):\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    if not all([isinstance(filepath, str)]):\n"
        "        raise TypeError(\n"
        '            "read_data expects arg types: [str], "\n'
        '            f"received: [{type(filepath).__name__}]"\n'
        "        )\n"
        "    if check_extension(filepath):\n"
        "        return pd.DataFrame({})\n"
        "    raise FileNotFoundError\n"
        "\n"
        "\n"
        "def check_extension(filepath: str) -> bool:\n"
        "    '''this is a docstring\n"
        "\n"
        "    Args:\n"
        "        filepath (str): the filepath to check\n"
        "\n"
        "    Returns:\n"
        "        bool: if the extension is valid\n"
        "    '''\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    if not all([isinstance(filepath, str)]):\n"
        "        raise TypeError(\n"
        '            "check_extension expects arg types: [str], "\n'
        '            f"received: [{type(filepath).__name__}]"\n'
        "        )\n"
        "    return bool(filepath)\n"
        "\n"
        "\n"
        "def clean_data(data):\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    return data\n"
        "\n"
        "\n"
        "def _transform_data(data) -> dict:\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    def transform() -> dict:\n"
        "        return {'data': data}\n"
        "\n"
        "    return transform()\n"
        "\n"
        "\n"
        "def rename_data(value) -> str:\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    def replacer(match) -> str:\n"
        "        content = match.group(1)\n"
        "        cleaned_content = ' '.join(content.split())\n"
        "        return f'({cleaned_content})'\n"
        "\n"
        "    return re.sub(r'\\((.*?)\\)', replacer, str(value.iloc[0, 0]), flags=re.DOTALL\n"
        "    )\n"
        "\n"
        "\n"
        "def merge_data(data_dict: Dict):\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    if not all([isinstance(data_dict, dict)]):\n"
        "        raise TypeError(\n"
        '            "merge_data expects arg types: [dict], "\n'
        '            f"received: [{type(data_dict).__name__}]"\n'
        "        )\n"
        "    # this is an inline comment that hopefully will stay\n"
        "    data = pd.concat([v for v in data_dict.values()])\n"
        "    return data\n"
        "\n"
        "\n"
        "def save_data(data, filepath: str) -> bool:\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    if not all([isinstance(filepath, str)]):\n"
        "        raise TypeError(\n"
        '            "save_data expects arg types: [str], "\n'
        '            f"received: [{type(filepath).__name__}]"\n'
        "        )\n"
        "    if filepath_exists(filepath):\n"
        "        return True\n"
        "    return False\n"
        "\n"
        "\n"
        "def filepath_exists(filepath: str) -> bool:\n"
        "    for key, val in locals().items():\n"
        '        logger.debug(f"{key} = {val}")\n'
        "    if not all([isinstance(filepath, str)]):\n"
        "        raise TypeError(\n"
        '            "filepath_exists expects arg types: [str], "\n'
        '            f"received: [{type(filepath).__name__}]"\n'
        "        )\n"
        "    return bool(filepath)\n"
        "\n"
        "\n"
    )


@pytest.fixture
def get_mock_utils_c_parametrized_tests():
    return (
        "import pytest\n\n\n"
        "@pytest.mark.parametrize(\n"
        '    "filepath, expected_result, expected_context",\n'
        "    [\n"
        "        (filepath, expected_result, expected_context),\n"
        "        (filepath, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_main(filepath, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert main(filepath) == expected_result\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "filepath, expected_result, expected_context",\n'
        "    [\n"
        "        (filepath, expected_result, expected_context),\n"
        "        (filepath, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_read_data(filepath, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert read_data(filepath) is None\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "filepath, expected_result, expected_context",\n'
        "    [\n"
        "        (filepath, expected_result, expected_context),\n"
        "        (filepath, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_check_extension(filepath, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert check_extension(filepath) == expected_result\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "data, expected_result, expected_context",\n'
        "    [\n"
        "        (data, expected_result, expected_context),\n"
        "        (data, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_clean_data(data, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert clean_data(data) is None\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "data, expected_result, expected_context",\n'
        "    [\n"
        "        (data, expected_result, expected_context),\n"
        "        (data, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_transform_data(data, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert _transform_data(data) == expected_result\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "value, expected_result, expected_context",\n'
        "    [\n"
        "        (value, expected_result, expected_context),\n"
        "        (value, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_rename_data(value, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert rename_data(value) == expected_result\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "data_dict, expected_result, expected_context",\n'
        "    [\n"
        "        (data_dict, expected_result, expected_context),\n"
        "        (data_dict, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_merge_data(data_dict, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert merge_data(data_dict) is None\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "data, filepath, expected_result, expected_context",\n'
        "    [\n"
        "        (data, filepath, expected_result, expected_context),\n"
        "        (data, filepath, None, pytest.raises(TypeError)),\n"
        "        (data, filepath, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_save_data(data, filepath, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert save_data(data, filepath) == expected_result\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "filepath, expected_result, expected_context",\n'
        "    [\n"
        "        (filepath, expected_result, expected_context),\n"
        "        (filepath, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_filepath_exists(filepath, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert filepath_exists(filepath) == expected_result\n"
        "\n"
        "\n"
    )


@pytest.fixture
def get_mock_service_parametrized_tests():
    return (
        "import pytest\n"
        "\n"
        "\n"
        "@pytest.fixture\n"
        "def get_mock_service_instance() -> MockService:\n"
        "    return MockService()\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "param, expected_result, expected_context",\n'
        "    [\n"
        "        (param, expected_result, expected_context),\n"
        "        (param, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_fetch_data(get_mock_service_instance: MockService, param, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert get_mock_service_instance.fetch_data(param) == expected_result\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "data, expected_result, expected_context",\n'
        "    [\n"
        "        (data, expected_result, expected_context),\n"
        "        (data, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_process_data(get_mock_service_instance: MockService, data, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert get_mock_service_instance.process_data(data) == expected_result\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "data, expected_result, expected_context",\n'
        "    [\n"
        "        (data, expected_result, expected_context),\n"
        "        (data, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_validate_data(get_mock_service_instance: MockService, data, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert get_mock_service_instance.validate_data(data) == expected_result\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "data, expected_result, expected_context",\n'
        "    [\n"
        "        (data, expected_result, expected_context),\n"
        "        (data, None, pytest.raises(TypeError)),\n"
        "    ]\n"
        ")\n"
        "def test_save_data(get_mock_service_instance: MockService, data, expected_result, expected_context) -> None:\n"
        "    with expected_context:\n"
        "        assert get_mock_service_instance.save_data(data) == expected_result\n"
        "\n"
        "\n"
    )


@pytest.fixture
def get_mock_service_boilerplate_add_guards():
    return (
        "    def fetch_data(self, param: str) -> List[Dict[str, Any]]:\n"
        "        '''\n"
        "        Mock method to fetch data based on a parameter.\n"
        "\n"
        "        Args:\n"
        "            param (str): The parameter to fetch data for.\n"
        "\n"
        "        Returns:\n"
        "            List[Dict[str, Any]]: A list of dictionaries containing the fetched data.\n"
        "        '''\n"
        "        if not all([isinstance(param, str)]):\n"
        "            raise TypeError(\n"
        '                "fetch_data expects arg types: [str], "\n'
        '                f"received: [{type(param).__name__}]"\n'
        "            )\n"
        "        return [{'id': 1, 'value': 'data1'}, {'id': 2, 'value': 'data2'}]\n"
        "\n"
        "\n"
        "    def process_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:\n"
        "        '''\n"
        "        Mock method to process data.\n"
        "\n"
        "        Args:\n"
        "            data (List[Dict[str, Any]]): A list of dictionaries containing the data to be processed.\n"
        "\n"
        "        Returns:\n"
        "            Dict[str, Any]: A dictionary containing the processed data.\n"
        "        '''\n"
        "        if not all([isinstance(data, list)]):\n"
        "            raise TypeError(\n"
        '                "process_data expects arg types: [list], "\n'
        '                f"received: [{type(data).__name__}]"\n'
        "            )\n"
        "        processed_data = {'summary': 'Processed Data', 'count': len(data)}\n"
        "        return processed_data\n"
        "\n"
        "\n"
        "    def validate_data(self, data: List[Dict[str, Any]]) -> bool:\n"
        "        '''\n"
        "        Mock method to validate data.\n"
        "\n"
        "        Args:\n"
        "            data (List[Dict[str, Any]]): A list of dictionaries containing the data to be validated.\n"
        "\n"
        "        Returns:\n"
        "            bool: True if the data is valid, False otherwise.\n"
        "        '''\n"
        "        if not all([isinstance(data, list)]):\n"
        "            raise TypeError(\n"
        '                "validate_data expects arg types: [list], "\n'
        '                f"received: [{type(data).__name__}]"\n'
        "            )\n"
        "        for item in data:\n"
        "            if 'id' not in item or 'value' not in item:\n"
        "                return False\n"
        "        return True\n"
        "\n"
        "\n"
        "    def save_data(self, data: Dict[str, Any]) -> bool:\n"
        "        '''\n"
        "        Mock method to save data.\n"
        "\n"
        "        Args:\n"
        "            data (Dict[str, Any]): A dictionary containing the data to be saved.\n"
        "\n"
        "        Returns:\n"
        "            bool: True if the data was saved successfully, False otherwise.\n"
        "        '''\n"
        "        if not all([isinstance(data, dict)]):\n"
        "            raise TypeError(\n"
        '                "save_data expects arg types: [dict], "\n'
        '                f"received: [{type(data).__name__}]"\n'
        "            )\n"
        "        return True\n"
        "\n"
        "\n"
    )
