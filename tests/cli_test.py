from typer.testing import Result


def test_main_with_default_values(main_with_default_values: Result) -> None:
    """Test the main function with default values.

    Args:
        main_with_default_values (Result): The result of invoking the main function with default values.

    Returns:
        None
    """
    result = main_with_default_values
    assert result.exit_code == 0


def test_main_with_existing_log_file(
    main_with_existing_log_file: tuple[Result, str],
) -> None:
    """Test the main function with existing log file.

    Args:
        main_with_existing_log_file (tuple[Result, str]): A tuple containing the result of invoking the main
        function with an existing log file, and the option used to invoke the main function.

    Returns:
        None
    """
    result, option = main_with_existing_log_file
    if "--no-override" == option:
        # Test without override
        assert result.exit_code != 0
    else:
        # Test with override
        assert result.exit_code == 0


def test_main_with_help_option(main_with_help_option: Result) -> None:
    """Test the main function with help option.

    Args:
        main_with_help_option (Result): The result of invoking the main function with the help option.

    Returns:
        None
    """
    result = main_with_help_option
    assert "Usage: " in result.stdout
