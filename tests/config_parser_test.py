import pytest

from template_python.config_parser import YAMLConfig


def test_valid_yaml_config() -> None:
    """Test if the valid YAML config file is parsed and validated correctly."""
    config = YAMLConfig(log_file_name="test.log")
    assert config.log_file_name == "test.log"


def test_invalid_yaml_config() -> None:
    """Test if an invalid YAML config file raises a ValueError."""
    with pytest.raises(ValueError):
        YAMLConfig(log_file_name="test")
