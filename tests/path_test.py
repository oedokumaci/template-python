from pathlib import Path


def test_path_variable(path: Path) -> None:
    """A test function that checks that each path variable exists, is a Path object, exists on the file system, and is a directory.

    Args:
        path (Path): The value of the path variable being tested.

    Returns:
        None: The function does not return a value.
    """
    # Check that the path variable exists
    assert path is not None

    # Check that the path variable is a Path object
    assert isinstance(path, Path)

    # Check that the path exists on the file system
    assert path.exists()

    # Check that the path is a directory
    assert path.is_dir()
