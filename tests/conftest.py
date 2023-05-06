import logging
from typing import Generator

import pytest

from template_python.config_parser import YAMLConfig
from template_python.path import CONFIG_DIR, LOGS_DIR, OUTPUTS_DIR
from template_python.utils import init_logger


@pytest.fixture(scope="package")
def logger_fixture() -> Generator[None, None, None]:
    """A fixture that initializes the logger for testing and cleans up after testing is complete.

    Yields:
        None: The fixture does not return a value.
    """
    log_file_path = LOGS_DIR / "pytest_test.log"
    init_logger(log_file_path.name)
    yield
    logger = logging.getLogger()
    for handler in logger.handlers:  # close all handlers, Windows fix
        handler.close()
    log_file_path.unlink()


@pytest.fixture
def yaml_config_instance() -> YAMLConfig:
    """A fixture that provides a YAMLConfig instance for testing.

    Returns:
        YAMLConfig: The YAMLConfig instance to use for testing.
    """
    return YAMLConfig(log_file_name="valid.log")


@pytest.fixture(params=[CONFIG_DIR, LOGS_DIR, OUTPUTS_DIR])
def path(request: pytest.FixtureRequest) -> str:
    """A fixture that yields each of the three path variables for testing.

    Args:
        request (pytest.FixtureRequest): The request object for the fixture.

    Yields:
        str: The value of the path variable for testing.
    """
    yield request.param
