"""This script is to setup the new project."""

import argparse
import os
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve().expanduser()

USER_REPLACE_PATHS = ["README_main.md"]
SRC_PATHS = [str(path) for path in (ROOT_DIR / "src").rglob("*.py")]
TESTS_PATHS = [str(path) for path in (ROOT_DIR / "tests").rglob("*.py")]

FILE_PATHS = USER_REPLACE_PATHS + SRC_PATHS + TESTS_PATHS + ["Makefile"]
DIR_PATHS = [str(ROOT_DIR / "src" / "template_python")]

OS = "windows-based" if os.name == "nt" else "unix-based"
PYTHON_VER = "3.10"


def rename_files(
    old_word: str, new_word: str, files: list[str], dirs: list[str]
) -> None:
    """Renames files and directories.

    Args:
        old_word (str)
        new_word (str)
        files (list[str])
        dirs (list[str])
    """
    file_paths = [ROOT_DIR / path for path in files]
    dir_paths = [ROOT_DIR / path for path in dirs]

    for path in file_paths:
        with open(path, encoding="utf-8") as f:
            contents = f.read()
        new_contents = contents.replace(old_word, new_word)

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_contents)

        new_path = path.with_name(path.name.replace(old_word, new_word))
        path.rename(new_path)

    for path in dir_paths:
        new_path = path.with_name(path.name.replace(old_word, new_word))
        path.rename(new_path)


def configure_git(user_name: str, user_email: str) -> None:
    """Configures the local git settings.

    Args:
        user_name (str)
        user_email (str)
    """
    subprocess.run(["git", "config", "user.name", user_name], check=True)
    subprocess.run(["git", "config", "user.email", user_email], check=True)


def generate_vscode_settings() -> None:
    """Generates the .vscode/settings.json file."""
    answer = input("Do you want to generate .vscode/settings.json? [y/n] (y) ") or "y"
    if answer == "y":
        (ROOT_DIR / ".vscode").mkdir(exist_ok=True)
        file = ROOT_DIR / ".vscode" / "settings.json"
        file.touch()
        settings = f"""
{{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": ["--max-line-length=88", "--select=C,E,F,W,B", "--extend-ignore=B009,E203,E501,W503"],
    "python.autoComplete.extraPaths": [".venv/lib/python{PYTHON_VER}/site-packages"],
    "python.analysis.extraPaths": [".venv/lib/python{PYTHON_VER}/site-packages"],
    "python.testing.pytestPath": ".venv/bin/pytest"
}}
"""
        with open(file, "w", encoding="utf-8") as f:
            f.write(settings)


def remove_pdm_files() -> None:
    """Removes the PDM-related files from the project."""
    files = ["pdm.lock", "pyproject.toml", "requirements.txt"]
    for file in files:
        try:
            if OS == "windows-based":
                subprocess.run(["del", file], check=True)
            else:
                subprocess.run(["rm", file], check=True)
        except subprocess.CalledProcessError:
            pass


def add_dependencies_using_pdm() -> None:
    """Adds project dependencies using PDM."""
    try:
        subprocess.run(["pdm", "--version"], check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["pip3", "install", "pdm"], check=True)
        except subprocess.CalledProcessError:
            subprocess.run(["pip", "install", "pdm"], check=True)
    subprocess.run(["pdm", "self", "update"], check=True)
    subprocess.run(["pdm", "init", "--python", PYTHON_VER], check=True)
    subprocess.run(["pdm", "add", "pdm"], check=True)
    subprocess.run(["pdm", "add", "typer"], check=True)
    subprocess.run(["pdm", "add", "pyyaml"], check=True)
    subprocess.run(["pdm", "add", "pydantic"], check=True)
    subprocess.run(["pdm", "add", "-dG", "workflow", "pre-commit"], check=True)
    subprocess.run(["pdm", "add", "-dG", "workflow", "mypy"], check=True)
    subprocess.run(["pdm", "add", "-dG", "workflow", "types-PyYAML"], check=True)
    subprocess.run(["pdm", "add", "-dG", "test", "pytest"], check=True)
    subprocess.run(["pdm", "run", "pre-commit", "install"], check=True)
    try:
        subprocess.run(
            ["pdm", "run", "pre-commit", "run", "--all-files", "pdm-export"], check=True
        )
    except subprocess.CalledProcessError:
        print("Pdm-export expected to fail during setup, this is normal. Continuing...")
    subprocess.run(["pdm", "fix"], check=True)


def remove_cached_files() -> None:
    """Removes the cached files."""
    try:
        if OS == "windows-based":
            subprocess.run(["rmdir", "/s", "/q", ".mypy_cache"], check=True)
        else:
            subprocess.run(["rm", "-rf", ".mypy_cache"], check=True)
    except subprocess.CalledProcessError:
        pass
    try:
        if OS == "windows-based":
            subprocess.run(["rmdir", "/s", "/q", ".pytest_cache"], check=True)
        else:
            subprocess.run(["rm", "-rf", ".pytest_cache"], check=True)
    except subprocess.CalledProcessError:
        pass


def main() -> int:
    """Main function that sets up the project."""
    parser = argparse.ArgumentParser(
        description="Does the magic to set up your project."
    )
    parser.add_argument(
        "--user-name", type=str, default="oedokumaci", help="GitHub username"
    )
    parser.add_argument(
        "--user-email",
        type=str,
        default="oral.ersoy.dokumaci@gmail.com",
        help="GitHub email",
    )
    args = parser.parse_args()

    print("Setting up the project...")
    print("Prompt default values will be in parentheses, press enter to accept them.")
    print(f"Detected {OS=}")

    # Rename file contents, names, and directories
    print("Renaming files and directories...")
    rename_files("template-python", ROOT_DIR.name, FILE_PATHS, [])
    rename_files(
        "template_python",
        ROOT_DIR.name.replace("-", "_"),
        FILE_PATHS,
        DIR_PATHS,
    )
    print("Files and directories renamed.")

    # Rename user-specific files
    rename_files("oedokumaci", args.user_name, USER_REPLACE_PATHS, [])
    rename_files(
        "oral.ersoy.dokumaci@gmail.com", args.user_email, USER_REPLACE_PATHS, []
    )

    # Configure the local Git settings
    print("Configuring local Git settings...")
    configure_git(args.user_name, args.user_email)
    print("Local Git settings configured.")

    # Rename README.md
    if (ROOT_DIR / "README.md").exists():
        (ROOT_DIR / "README.md").unlink()
    (ROOT_DIR / "README_main.md").rename(ROOT_DIR / "README.md")

    # Remove PDM-related files
    remove_pdm_files()

    # Run pdm init
    add_dependencies_using_pdm()

    # Generate .vscode/settings.json
    generate_vscode_settings()

    # Remove template setup file
    try:
        if OS == "windows-based":
            subprocess.run(["del", f"{Path(__file__).name}"], check=True)
        else:
            subprocess.run(["rm", f"{Path(__file__).name}"], check=True)
    except subprocess.CalledProcessError:
        pass

    # Git add commit and push
    answer = input("Do you want to git add commit and push? [y/n] (y) ") or "y"
    if answer == "y":
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initialize via template_setup.py"], check=True
        )
        subprocess.run(["git", "push"], check=True)

    # Remove cached files
    remove_cached_files()

    print("Setup complete!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
