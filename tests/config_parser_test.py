import pytest

from template_python.config_parser import YAMLConfig


def test_yaml_config_instance(yaml_config_instance: YAMLConfig) -> None:
    assert yaml_config_instance is not None
    assert isinstance(yaml_config_instance, YAMLConfig)
    assert yaml_config_instance.log_file_name.endswith((".log", ".txt"))


# Test cases for log_file_name validation
@pytest.mark.parametrize(
    "log_file_name, expected",
    [
        ("valid_extension_test.log", "valid_extension_test.log"),
        ("invalid_extension_test", ValueError),
        ("invalid_extension_test.csv", ValueError),
    ],
)
def test_log_file_name_validation(
    yaml_config_instance: YAMLConfig, log_file_name: str, expected: str | ValueError
) -> None:
    """Test if the YAML config file is parsed and validated correctly."""
    yaml_config_instance.log_file_name = log_file_name

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            YAMLConfig(**yaml_config_instance.dict())
    else:
        config = YAMLConfig(**yaml_config_instance.dict())
        assert config.log_file_name == expected
