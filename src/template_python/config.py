"""This module parses and validates the config files in config directory."""
from __future__ import annotations

from typing import TypedDict

import yaml
from pydantic import BaseModel, validator

from template_python.path import CONFIG_DIR


class YAMLConfig(BaseModel):
    """Class that defines the structure and validation rules for the config.yaml file.

    Inherits from pydantic BaseModel.
    """

    # Define the fields for the config file
    log_file_name: str

    # Define a validator to ensure the log_file_name is valid
    @validator("log_file_name")
    def log_file_name_must_be_valid(cls, v: str) -> str:
        """Validator to ensure the log_file_name is valid.

        Args:
            v (str): The log_file_name value.

        Raises:
            ValueError: If log_file_name starts with /.
            ValueError: If log_file_name is not a .log or .txt file.

        Returns:
            str: The validated log_file_name.
        """
        if v.startswith("/"):
            raise ValueError(
                f"log_file_name should not start with /, {v!r} starts with /"
            )
        if not v.endswith(".log") and not v.endswith(".txt"):
            raise ValueError(
                f"log_file_name should be a .log or .txt file, {v!r} is not"
            )
        return v


class YAMLConfigDict(TypedDict):
    log_file_name: str


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
