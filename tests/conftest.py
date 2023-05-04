import logging
from typing import Generator

import pytest

from template_python.config_parser import YAMLConfig
from template_python.path import LOGS_DIR
from template_python.utils import init_logger


@pytest.fixture(scope="package")
def logger_fixture() -> Generator[None, None, None]:
    log_file_path = LOGS_DIR / "pytest_test.log"
    init_logger(log_file_path.name)
    yield
    logger = logging.getLogger()
    for handler in logger.handlers:  # close all handlers, Windows fix
        handler.close()
    log_file_path.unlink()


@pytest.fixture
def yaml_config_instance() -> YAMLConfig:
    return YAMLConfig(log_file_name="valid.log")
