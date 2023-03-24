"""Command line application module."""

import typer

from template_python.utils import LOG_PATH, init_logger

log_file_name_argument = typer.Argument(
    "logs.log", help="Name of the log file, default is 'logs.log'"
)
override_option = typer.Option(
    False, help="Override log file if it exists, default is False"
)


def check_log_file_name(log_file_name: str) -> None:
    user_input = (
        input(f"log_file_name {log_file_name!r} already exists, overwrite? y/n (n): ")
        or "n"
    )
    if user_input != "y":
        raise SystemExit(
            "exiting not to overwrite, please use a different log_file_name"
        )
    print("")


def main(
    log_file_name: str = log_file_name_argument, override: bool = override_option
) -> None:
    # Check if log file exists, if so ask to overwrite
    log_file = LOG_PATH / log_file_name
    if not override and log_file.exists():
        check_log_file_name(log_file_name)

    # Initialize logger
    init_logger(log_file_name)

    # Print log file path
    print("")
    print(f"logs are saved to {log_file.resolve()}")

    raise typer.Exit()
