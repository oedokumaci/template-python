from collections.abc import Generator
from pathlib import Path

import pytest

from template_python.path import CONFIG_DIR, DATA_DIR, LOGS_DIR, OUTPUTS_DIR, ROOT_DIR


# Fixture for paths
@pytest.fixture(
    params=[ROOT_DIR, CONFIG_DIR, LOGS_DIR, OUTPUTS_DIR, DATA_DIR],
    ids=["root_dir", "config_dir", "logs_dir", "outputs_dir", "data_dir"],
)
def path(request: pytest.FixtureRequest) -> Generator[Path]:
    """A fixture that provides a path for testing.

    This fixture takes a request parameter, which is used to parametrize the fixture
    with different paths. The fixture yields the path corresponding to the request
    parameter. The fixture is used to provide paths to the test functions.
    """
    yield request.param
