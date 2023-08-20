"""This module parses and validates the config files in config directory."""

from __future__ import annotations

from typing import TypedDict

import yaml
from pydantic import BaseModel

from template_python.path import CONFIG_DIR


class YAMLConfig(BaseModel):
    """Class that defines the structure and validation rules for the config.yaml file.

    Inherits from pydantic BaseModel.
    """

    # Define the fields for the config file


class YAMLConfigDict(TypedDict):
    """Type definition for the YAMLConfig dictionary."""


def parse_and_validate_configs() -> YAMLConfig:
    """Parse and validate the contents of the config.yaml file.

    Returns:
        YAMLConfig: The validated YAMLConfig object.
    """

    with open(CONFIG_DIR / "config.yaml") as yaml_file:
        # Load the contents of the yaml file into a dictionary
        yaml_config: YAMLConfigDict = yaml.safe_load(yaml_file)

    # Create a YAMLConfig object from the dictionary
    return YAMLConfig(**yaml_config)


# Parse and validate the config files at import time
YAML_CONFIG = parse_and_validate_configs()
