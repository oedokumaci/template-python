import pytest

from template_python.config_parser import YAMLConfig


@pytest.mark.parametrize(
    "log_file_name, expected",
    [
        ("valid_extension_test.log", "valid_extension_test.log"),
        ("invalid_extension_test", ValueError),
        ("invalid_extension_test.csv", ValueError),
    ],
)
def test_parse_yaml_config(log_file_name: str, expected: str | ValueError) -> None:
    """Test if the YAML config file is parsed and validated correctly."""
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            YAMLConfig(log_file_name=log_file_name)
    else:
        config = YAMLConfig(log_file_name=log_file_name)
        assert config.log_file_name == expected
