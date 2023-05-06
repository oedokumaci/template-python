"""Module for paths used in the project."""

from pathlib import Path

ROOT_DIR: Path = Path(__file__).parents[2].resolve().expanduser()

CONFIG_DIR: Path = ROOT_DIR / "config"
LOGS_DIR: Path = ROOT_DIR / "logs"
OUTPUTS_DIR: Path = ROOT_DIR / "outputs"
