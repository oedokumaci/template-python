import logging
from typing import Generator

import pytest

from template_python.utils import LOG_PATH, init_logger


@pytest.fixture(scope="package")
def logger_fixture() -> Generator[None, None, None]:
    log_file_path = LOG_PATH / "pytest_test.log"
    init_logger(log_file_path.name)
    yield
    logger = logging.getLogger()
    for handler in logger.handlers:  # close all handlers, Windows fix
        handler.close()
    log_file_path.unlink()
