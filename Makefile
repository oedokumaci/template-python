.PHONY: setup run help clean

setup:  # Setup the project
	pdm install
	pdm run pre-commit install

run:  # Run the project
	pdm run python -m template_python

help:  # Show project help
	pdm run python -m template_python --help

ifeq ($(OS),Windows_NT)
clean:  # Clean the project
	if exists .mypy_cache rmdir /s /q .mypy_cache
	if exists .pytest_cache rmdir /s /q .pytest_cache
	if exists src\template_python\__pycache__ rmdir /s /q src\template_python\__pycache__
	if exists tests\__pycache__ rmdir /s /q tests\__pycache__
else
clean:  # Clean the project
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf src/template_python/__pycache__
	rm -rf tests/__pycache__
