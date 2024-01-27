"""This module parses and validates the config files in config directory."""

from __future__ import annotations

from pathlib import Path
from typing import TypedDict

import yaml
from pydantic import BaseModel
from rich import print as rprint

from template_python.path import CONFIG_DIR


class Config(BaseModel):
    """Class that defines the structure and validation rules for the package config.

    Inherits from pydantic BaseModel.
    """

    # Define the fields for the config file


class ConfigDict(TypedDict):
    """Type definition for the Config dictionary."""


def parse_and_validate_configs(
    file_path_or_config_dict: Path | ConfigDict = CONFIG_DIR / "config.yaml",
) -> Config | None:
    """Parse and validate the contents of the config file or dictionary.

    Args:
        file_path_or_config_dict (Path | ConfigDict, optional): The path to the config file or a dictionary containing the config. Defaults to CONFIG_DIR / "config.yaml".

    Returns:
        Config: The validated Config object.
    """

    if isinstance(file_path_or_config_dict, Path):
        # Read the contents of the yaml file into a dictionary
        with open(file_path_or_config_dict) as yaml_file:
            config: ConfigDict = yaml.safe_load(yaml_file)
    elif isinstance(file_path_or_config_dict, dict):
        config = file_path_or_config_dict
    else:
        raise TypeError(
            f"file_path_or_config_dict must be of type Path or ConfigDict, not {type(file_path_or_config_dict)}"
        )

    # Create a Config object from the dictionary
    if config:
        return Config(**config)
    else:
        return None


if __name__ == "__main__":
    # Parse and validate the config files at import time
    CONFIG = parse_and_validate_configs()
    rprint(CONFIG)
