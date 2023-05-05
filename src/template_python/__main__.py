"""Entry-point module, in case of using `python -m template_python`."""

import typer

from template_python.cli import main

if __name__ == "__main__":
    typer.run(main)
