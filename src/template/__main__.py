"""Entry-point module, in case of using `python -m template`."""

import typer

from template.cli import main

typer.run(main)
