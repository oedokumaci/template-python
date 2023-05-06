import logging
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner, Result

from template_python.config_parser import YAMLConfig
from template_python.path import CONFIG_DIR, LOGS_DIR, OUTPUTS_DIR, ROOT_DIR
from template_python.utils import init_logger

pytest_log_file: Path = LOGS_DIR / "pytest_test.log"


# Fixture to set up logger for tests
@pytest.fixture(scope="package")
def logger_fixture() -> Generator[None, None, None]:
    """Fixture to set up logger for tests."""
    init_logger(pytest_log_file.name)
    yield
    # Clean up after test
    logger = logging.getLogger()
    for handler in logger.handlers:  # close all handlers, Windows fix
        handler.close()
    pytest_log_file.unlink()


# Fixture for YAMLConfig instance
@pytest.fixture
def yaml_config_instance() -> YAMLConfig:
    """A fixture that provides a YAMLConfig instance for testing.

    Returns:
        YAMLConfig: The YAMLConfig instance to use for testing.
    """
    return YAMLConfig(log_file_name="valid.log")


# Fixture for paths
@pytest.fixture(
    params=[ROOT_DIR, CONFIG_DIR, LOGS_DIR, OUTPUTS_DIR],
    ids=["root_dir", "config_dir", "logs_dir", "outputs_dir"],
)
def path(request: pytest.FixtureRequest) -> Generator[Path, None, None]:
    """Fixture for paths."""
    yield request.param


# Fixture for main function with default values
@pytest.fixture(scope="function")
def main_with_default_values() -> Generator[Result, None, None]:
    """Fixture for main function with default values."""
    from template_python.cli import app

    result = CliRunner().invoke(app, [pytest_log_file.name])
    yield result
    # Clean up after test
    logger = logging.getLogger()
    for handler in logger.handlers:  # close all handlers, Windows fix
        handler.close()
    pytest_log_file.unlink()


# Fixture for main function with custom values
@pytest.fixture(scope="function")
def main_with_custom_values() -> (
    tuple[Generator[str, None, None], Generator[Result, None, None]]
):
    """Fixture for main function with custom values."""
    from template_python.cli import app

    result = CliRunner().invoke(app, [pytest_log_file.name, "--override"])
    yield pytest_log_file.name, result
    # Clean up after test
    logger = logging.getLogger()
    for handler in logger.handlers:  # close all handlers, Windows fix
        handler.close()
    pytest_log_file.unlink()


# Fixture for main function with existing log file
@pytest.fixture(scope="function")
def main_with_existing_log_file(
    request: pytest.FixtureRequest,
) -> tuple[Generator[CliRunner, None, None], Generator[str, None, None]]:
    """Fixture for main function with existing log file."""
    log_file_name: str = request.param
    (LOGS_DIR / log_file_name).touch()

    yield CliRunner(), log_file_name
    # Clean up after test
    logger = logging.getLogger()
    for handler in logger.handlers:  # close all handlers, Windows fix
        handler.close()
    (LOGS_DIR / log_file_name).unlink()


# Fixture for main function with help option
@pytest.fixture(scope="function")
def main_with_help_option() -> Generator[Result, None, None]:
    """Fixture for main function with help option."""
    from template_python.cli import app

    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0

    yield result
