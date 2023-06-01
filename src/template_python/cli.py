"""Command line application module."""

import typer

from template_python.path import LOGS_DIR
from template_python.utils import init_logger

app = typer.Typer()

# Define command line arguments and options
log_option = typer.Option(True, help="Whether to enable logging.")


@app.command()
def main(log: bool = log_option) -> None:
    """CLI for template-python."""

    if log:
        # Check if log file exists, if so ask to overwrite
        log_file_name: str = typer.prompt("Enter log file name", default="logs.log")
        log_file = LOGS_DIR / log_file_name
        if log_file.exists():
            overwrite = typer.confirm("Log file already exists, overwrite?")
            if not overwrite:
                typer.echo("Exiting...")
                raise typer.Exit()
        # Initialize logger
        init_logger(log_file_name)

    # Print log file path
    typer.echo("All done!")
    typer.echo(f"Logs are saved to {log_file.resolve()}")
