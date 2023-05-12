import logging
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner, Result

from template_python.config import YAMLConfig, YAMLConfigDict
from template_python.path import CONFIG_DIR, LOGS_DIR, OUTPUTS_DIR, ROOT_DIR
from template_python.utils import init_logger

# Path to the log file to be used for testing
pytest_log_file: Path = LOGS_DIR / "pytest_test.log"


# Fixture to handle cleanup process for all fixtures
@pytest.fixture
def cleanup() -> Generator[None, None, None]:
    """A fixture that performs cleanup after each test function.

    This fixture is responsible for cleaning up all fixtures by closing all the handlers
    of the logger and deleting the log file. The fixture is used as a yield fixture
    that is called after the execution of the test function completes.
    """
    yield
    for handler in logging.getLogger().handlers:  # close all handlers, Windows fix
        handler.close()
    pytest_log_file.unlink()


# Fixture to set up logger for tests
@pytest.fixture
def logger_fixture(cleanup: Generator[None, None, None]) -> Generator[None, None, None]:
    """A fixture that sets up the logger for testing.

    This fixture sets up the logger by initializing it with the log file to be used for
    testing. The fixture is used as a yield fixture that is called before the execution
    of the test function starts.
    """
    init_logger(pytest_log_file.name)
    yield


# Fixture for YAMLConfig instance
@pytest.fixture
def yaml_config_instance() -> YAMLConfig:
    """A fixture that provides a YAMLConfig instance for testing.

    This fixture creates a YAMLConfigDict and uses it to initialize the YAMLConfig
    instance. The fixture is used to provide a YAMLConfig instance to the test functions.

    Returns:
        YAMLConfig: The YAMLConfig instance to use for testing.
    """
    config: YAMLConfigDict = {
        "log_file_name": "valid.log",
    }
    return YAMLConfig(**config)


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


# Fixture for main function with default values
@pytest.fixture
def main_with_default_values(
    cleanup: Generator[None, None, None]
) -> Generator[Result, None, None]:
    """A fixture that invokes the main function with default values.

    This fixture invokes the main function with the log file to be used for testing
    and yields the result. The fixture is used to test the main function with default
    values.
    """
    from template_python.cli import app

    result = CliRunner().invoke(app, [pytest_log_file.name])
    yield result


# Fixture for main function with existing log file
@pytest.fixture(params=["--no-override", "--override"], ids=["no_override", "override"])
def main_with_existing_log_file(
    request: pytest.FixtureRequest, cleanup: Generator[None, None, None]
) -> Generator[tuple[Result, str], None, None]:
    """A fixture that invokes the main function with an existing log file.

    This fixture creates an empty log file in the logs directory and then invokes
    the main function with the log file to be used for testing and the requested
    option (either --override or --no-override). The fixture yields a tuple containing
    the result and the option. The fixture is used to test the main function with
    an existing log file.
    """
    from template_python.cli import app

    # Create an empty log file in the logs directory
    (LOGS_DIR / pytest_log_file.name).touch()

    # Get the requested option (either --override or --no-override)
    option = request.param

    # Invoke the main function with the log file to be used for testing and the option
    result = CliRunner().invoke(app, [pytest_log_file.name, option])

    yield result, option


# Fixture for main function with help option
@pytest.fixture
def main_with_help_option(
    logger_fixture: Generator[None, None, None]
) -> Generator[Result, None, None]:
    """A fixture that invokes the main function with the help option.

    This fixture invokes the main function with the help option and yields the result.
    The fixture is used to test the main function with the help option.
    """
    from template_python.cli import app

    result = CliRunner().invoke(app, ["--help"])

    yield result
