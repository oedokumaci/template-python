from typing import Type

import pytest

from template_python.config import YAMLConfig


def test_yaml_config_instance(yaml_config_instance: YAMLConfig) -> None:
    """Test if a YAMLConfig instance is created correctly.

    Args:
        yaml_config_instance (YAMLConfig): A YAMLConfig instance to test.

    Returns:
        None
    """
    assert yaml_config_instance is not None
    assert isinstance(yaml_config_instance, YAMLConfig)
    assert yaml_config_instance.log_file_name.endswith((".log", ".txt"))


@pytest.mark.parametrize(
    "log_file_name, expected",
    [
        ("valid_extension_test.log", "valid_extension_test.log"),
        ("invalid_extension_test", ValueError),
        ("invalid_extension_test.csv", ValueError),
    ],
)
def test_log_file_name_validation(
    yaml_config_instance: YAMLConfig,
    log_file_name: str,
    expected: str | Type[Exception],
) -> None:
    """Test if log_file_name is validated correctly.

    Args:
        yaml_config_instance (YAMLConfig): A YAMLConfig instance to test.
        log_file_name (str): The log file name to validate.
        expected (str | Type[Exception]): The expected result of the validation.

    Returns:
        None
    """
    yaml_config_instance.log_file_name = log_file_name

    if not isinstance(expected, str):
        with pytest.raises(expected):
            YAMLConfig(**yaml_config_instance.dict())
    else:
        config = YAMLConfig(**yaml_config_instance.dict())
        assert config.log_file_name == expected
