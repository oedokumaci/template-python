import pytest
from typer.testing import Result

from template_python.cli import app
from template_python.path import LOGS_DIR


def test_main_with_default_values(main_with_default_values: Result) -> None:
    result = main_with_default_values
    assert result.exit_code == 0


def test_main_with_custom_values(main_with_custom_values: Result) -> None:
    log_file_name, result = main_with_custom_values
    assert result.exit_code == 0
    log_file_path = LOGS_DIR / log_file_name
    assert log_file_path.exists()


@pytest.mark.parametrize("main_with_existing_log_file", ["existing.log"], indirect=True)
def test_main_with_existing_log_file_without_override(
    main_with_existing_log_file: Result,
) -> None:
    cli_runner, log_file_name = main_with_existing_log_file
    result = cli_runner.invoke(app, [log_file_name])
    assert result.exit_code != 0
    log_file_path = LOGS_DIR / log_file_name
    assert log_file_path.exists()


@pytest.mark.parametrize("main_with_existing_log_file", ["existing.log"], indirect=True)
def test_main_with_existing_log_file_with_override(
    main_with_existing_log_file: Result,
) -> None:
    cli_runner, log_file_name = main_with_existing_log_file
    result = cli_runner.invoke(app, [log_file_name, "--override"])
    assert result.exit_code == 0
    log_file_path = LOGS_DIR / log_file_name
    assert log_file_path.exists()


def test_main_with_help_option(main_with_help_option: Result) -> None:
    assert "Usage: " in main_with_help_option.stdout
