import logging
from typing import Generator

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest import LogCaptureFixture

from template_python.path import LOGS_DIR
from template_python.utils import check_log_file_name, timer_decorator


@pytest.mark.parametrize(
    "level,msg",
    [
        (logging.INFO, "info"),
        (logging.WARNING, "warning"),
        (logging.ERROR, "error"),
        (logging.CRITICAL, "critical"),
    ],
)
def test_init_logger(
    logger_fixture: Generator[None, None, None],
    caplog: LogCaptureFixture,
    level: int,
    msg: str,
) -> None:
    """Test if the logger object is initialized and produces the correct log messages.

    Args:
        logger_fixture (Generator[None, None, None]): The logger fixture.
        caplog (LogCaptureFixture): The fixture to capture log messages.
        level (int): The logging level.
        msg (str): The log message.

    Returns:
        None: The function does not return a value.
    """
    logger_fixture
    logging.log(level, msg)

    # Assert that the log file was created in the correct directory
    log_file_path = LOGS_DIR / "pytest_test.log"
    assert log_file_path.is_file()

    # Assert that the correct logs were produced
    assert caplog.record_tuples[-1] == ("root", level, msg)


def test_check_log_file_name_overwrite_yes(monkeypatch: MonkeyPatch) -> None:
    """Test if the function allows overwriting when user inputs y.

    Args:
        monkeypatch (MonkeyPatch): The monkeypatch fixture.

    Returns:
        None: The function does not return a value.
    """
    log_file_name = "test.log"
    monkeypatch.setattr("builtins.input", lambda _: "y")
    check_log_file_name(log_file_name)
    monkeypatch.undo()


def test_check_log_file_name_overwrite_no(monkeypatch: MonkeyPatch) -> None:
    """Test if the function raises SystemExit when user inputs n.

    Args:
        monkeypatch (MonkeyPatch): The monkeypatch fixture.

    Returns:
        None: The function does not return a value.
    """
    log_file_name = "test.log"
    monkeypatch.setattr("builtins.input", lambda _: "n")
    with pytest.raises(SystemExit):
        check_log_file_name(log_file_name)
    monkeypatch.undo()


def test_timer_decorator(caplog: LogCaptureFixture) -> None:
    """Test if the timer_decorator function correctly times the execution of a function.

    Args:
        caplog (LogCaptureFixture): The fixture to capture log messages.

    Returns:
        None: The function does not return a value.
    """

    # Define a test function that takes some time to execute
    @timer_decorator
    def test_function() -> str:
        for _ in range(1000000):
            pass
        return "done"

    # Call the function and check that the correct logs were produced
    result = test_function()
    assert result == "done"
    assert caplog.record_tuples[0][2].startswith(
        "Method 'test_function' of module 'tests.utils_test' executed in "
    )
