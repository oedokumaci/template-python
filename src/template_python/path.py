from pathlib import Path

ROOT_DIR = Path(__file__).parents[2]

CONFIG_DIR: Path = ROOT_DIR / "config"
LOGS_DIR: Path = ROOT_DIR / "logs"
OUTPUTS_DIR: Path = ROOT_DIR / "outputs"
