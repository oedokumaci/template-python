"""Command line application module."""

import logging

import typer

from template_python.config import YAML_CONFIG
from template_python.utils import init_logger

app = typer.Typer()

# Define command line arguments and options
log_to_file_option = typer.Option(True, help="Whether to enable saving logs to a file.")


@app.command()
def main(log_to_file: bool = log_to_file_option) -> None:
    """CLI for template-python."""

    # Initialize the logger
    init_logger(log_to_file=log_to_file)

    # Log the config, each key-value pair on a separate line
    if YAML_CONFIG:
        logging.info("Config:")
        for key, value in YAML_CONFIG.model_dump().items():
            logging.info(f"{key}: {value}")
    else:
        logging.info("Config file is empty.")
