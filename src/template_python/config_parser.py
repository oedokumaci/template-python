"""This module parses and validates the config files in config directory."""

import yaml
from pydantic import BaseModel, validator

from template_python.path import CONFIG_DIR


class YAMLConfig(BaseModel):
    """Parses and validates the contents of config.yaml file.
    Inherits from pydantic BaseModel.
    """

    log_file_name: str

    @validator("log_file_name")
    def log_file_name_must_be_valid(cls, v: str) -> str:
        """Validator to ensure the log_file_name is valid.

        Args:
            v (str): log_file_name value.

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


def parse_and_validate_configs() -> YAMLConfig:
    """Parses and validates the contents of config files in config directory.

    Returns:
        YAMLConfig: The validated YAMLConfig object.
    """

    with open(CONFIG_DIR / "config.yaml") as yaml_file:
        yaml_config: dict[str, str] = yaml.safe_load(yaml_file)
    return YAMLConfig(**yaml_config)


YAML_CONFIG = parse_and_validate_configs()
