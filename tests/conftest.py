import pytest

from class_inspector._logger import get_dir_path
from class_inspector.utils import get_src_code

collect_ignore_glob = ["**/mock_package/*"]


@pytest.fixture
def get_fixture_test_mock_module():
    return get_src_code(
        get_dir_path(__file__, 1, "mock_package/transformed/tests/test_mock_module.py")
    )
