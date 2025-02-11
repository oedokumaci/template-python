"""Module for utility functions."""

import logging
from collections.abc import Callable
from datetime import datetime
from functools import wraps
from pathlib import Path
from time import time

from rich.logging import RichHandler

from template_python.path import LOGS_DIR


# Define function to initialize the logger
def init_logger(
    input_log_file_name: str | None = None, log_to_file: bool = True
) -> None:
    """Initialize the logger.

    Args:
        input_log_file_name (str | None): The name of the log file. Defaults to None.
        log_to_file (bool, optional): Whether to log to file. Defaults to True.
    """
    if log_to_file:
        # Set the log file path and create it if it does not exist
        if input_log_file_name:
            log_file_name: str = input_log_file_name
        else:
            log_file_name = f"logs_{datetime.now().strftime('%Y-%m-%d')}.log"
        log_file: Path = LOGS_DIR / log_file_name
        log_file.touch(exist_ok=True)

        # Set the log formatter and handler levels for the log file
        log_formatter = logging.Formatter("%(asctime)s:%(levelname)s: %(message)s")
        log_formatter.datefmt = "%Y-%m-%d %H:%M:%S"
        log_handler = logging.FileHandler(str(log_file))
        log_handler.setFormatter(log_formatter)
        log_handler.setLevel(logging.INFO)

    # Set the log formatter and handler levels for the standard output
    std_log_formatter = logging.Formatter("%(message)s")
    std_log_formatter.datefmt = "%H:%M:%S"
    std_log_handler = RichHandler()
    std_log_handler.setFormatter(std_log_formatter)

    # Add handlers to the logger and set the logging level
    logger = logging.getLogger()
    if log_to_file:
        logger.addHandler(log_handler)
    logger.addHandler(std_log_handler)
    logger.setLevel(logging.DEBUG)

    # Set library logging level to error
    for key in logging.Logger.manager.loggerDict:
        logging.getLogger(key).setLevel(logging.ERROR)

    if log_to_file:
        # Log the path to log file
        logging.info(f"Path to log file: {log_file.resolve()}")


# Define a decorator function to print the execution time of a function
def timer_decorator[**P, T](func: Callable[P, T]) -> Callable[P, T]:  # noqa: F821
    """Decorator that prints the time it took to execute a function.

    Args:
        func (Callable[P, R]): The function to be decorated.

    Returns:
        Callable[P, T]: The decorated function.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:  # noqa: F821
        """Wrapper function that prints the time it took to execute a function.

        Args:
            *args (P.args): Positional arguments for the function.
            **kwargs (P.kwargs): Keyword arguments for the function.

        Returns:
            T: The result of the function.
        """
        # Get the start time and execute the function
        t1: float = time()
        result: T = func(*args, **kwargs)

        # Get the end time and calculate the elapsed time
        t2: float = time()
        elapsed_time: float = t2 - t1

        # Log the execution time and return the result of the function
        logging.info(
            f"{func.__qualname__!r} of module {func.__module__!r} executed in {elapsed_time:.4f} seconds"
        )
        return result

    return wrapper
