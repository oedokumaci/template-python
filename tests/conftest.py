from pathlib import Path
from typing import Generator

import pytest

from template_python.path import CONFIG_DIR, LOGS_DIR, OUTPUTS_DIR, ROOT_DIR


# Fixture for paths
@pytest.fixture(
    params=[ROOT_DIR, CONFIG_DIR, LOGS_DIR, OUTPUTS_DIR],
    ids=["root_dir", "config_dir", "logs_dir", "outputs_dir"],
)
def path(request: pytest.FixtureRequest) -> Generator[Path, None, None]:
    """A fixture that provides a path for testing.

    This fixture takes a request parameter, which is used to parametrize the fixture
    with different paths. The fixture yields the path corresponding to the request
    parameter. The fixture is used to provide paths to the test functions.
    """
    yield request.param
