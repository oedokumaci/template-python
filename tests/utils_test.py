import logging
from typing import Generator

import pytest
from pytest import LogCaptureFixture

from template_python.utils import LOG_PATH, timer_decorator


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
    logger_fixture: None, caplog: Generator[LogCaptureFixture, None, None], level, msg
) -> None:
    logger_fixture
    logging.log(level, msg)

    # Assert that the log file was created in the correct directory
    log_file_path = LOG_PATH / "pytest_test.log"
    assert log_file_path.is_file()

    # Assert that the correct logs were produced
    assert caplog.record_tuples[-1] == ("root", level, msg)


def test_timer_decorator(caplog: Generator[LogCaptureFixture, None, None]) -> None:
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
