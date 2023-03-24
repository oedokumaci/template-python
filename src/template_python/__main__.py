"""Entry-point module, in case of using `python -m template_python`."""

import typer

from template_python.cli import main

typer.run(main)
