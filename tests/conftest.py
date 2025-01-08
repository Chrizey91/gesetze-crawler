import pytest
from unittest.mock import patch, Mock

@pytest.fixture
def test_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("test-dir")
