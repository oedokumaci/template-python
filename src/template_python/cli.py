"""Command line application module."""

import typer

from template_python.utils import init_logger

app = typer.Typer()

# Define command line arguments and options
log_to_file_option = typer.Option(True, help="Whether to enable saving logs to a file.")


@app.command()
def main(log_to_file: bool = log_to_file_option) -> None:
    """CLI for template-python."""

    # Initialize the logger
    init_logger(log_to_file=log_to_file)
