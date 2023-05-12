"""Module for utility functions."""

import logging
import sys
from pathlib import Path
from time import time
from typing import Callable, ParamSpec, TypeVar

from template_python.path import LOGS_DIR

# Define TypeVars and ParamSpecs
R = TypeVar("R")
P = ParamSpec("P")


# Define function to initialize the logger
def init_logger(file_name: str) -> None:
    """Initialize the logger.

    Args:
        file_name (str): The name of the log file.
    """
    # Set the log file path and delete the file if it already exists
    log_file: Path = LOGS_DIR / file_name
    log_file.unlink(missing_ok=True)
    log_file.touch()

    # Set the log formatter and handler levels
    log_formatter = logging.Formatter("%(asctime)s:%(levelname)s: %(message)s")
    log_formatter.datefmt = "%Y-%m-%d %H:%M:%S"

    log_handler = logging.FileHandler(str(log_file))
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)

    std_log_handler = logging.StreamHandler(sys.stdout)
    std_log_handler.setFormatter(log_formatter)
    std_log_handler.setLevel(logging.DEBUG)

    # Add handlers to the logger and set logging level
    logger = logging.getLogger()
    logger.addHandler(std_log_handler)
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)

    # Set library logging level to error
    for key in logging.Logger.manager.loggerDict:
        logging.getLogger(key).setLevel(logging.ERROR)

    # Print path to log file
    logging.info(f"Path to log file: {log_file.resolve()}")


# Define function to check if a log file already exists and ask user whether to overwrite it
def check_log_file_name(log_file_name: str) -> None:
    """Check if the given log_file_name exists and ask the user whether to overwrite it.

    Args:
        log_file_name (str): The name of the log file.
    """
    user_input = (
        input(f"{log_file_name=!r} already exists, overwrite? y/n (n): ") or "n"
    )
    if user_input != "y":
        raise SystemExit(
            "exiting not to overwrite, please use a different log_file_name"
        )
    print("")


# Define a decorator function to print the execution time of a function
def timer_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that prints the time it took to execute a function.

    Args:
        func (Callable[P, R]): The function to be decorated.

    Returns:
        Callable[P, R]: The decorated function.
    """

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        """Wrapper function that prints the time it took to execute a function.

        Args:
            *args (P.args): Positional arguments for the function.
            **kwargs (P.kwargs): Keyword arguments for the function.

        Returns:
            R: The result of the function.
        """
        # Get the start time and execute the function
        t1: float = time()
        result: R = func(*args, **kwargs)

        # Get the end time and calculate the elapsed time
        t2: float = time()
        elapsed_time = t2 - t1

        # Log the execution time and return the result of the function
        logging.info(
            f"Method {func.__name__!r} of module {func.__module__!r} executed in {elapsed_time:.4f} seconds"
        )
        return result

    return wrapper
