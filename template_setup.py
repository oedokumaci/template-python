"""This module is to setup the new project."""

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent

USER_REPLACE_PATHS = ["README_main.md"]
SRC_PATHS = [str(path) for path in (ROOT_DIR / "src").rglob("*.py")]
TESTS_PATHS = [str(path) for path in (ROOT_DIR / "tests").rglob("*.py")]

FILE_PATHS = USER_REPLACE_PATHS + SRC_PATHS + TESTS_PATHS
DIR_PATHS = [str(ROOT_DIR / "src" / "template_python")]

OS = "windows-based" if sys.platform.startswith("win") else "unix-based"
PYTHON_VER = "3.10"


def rename_files(
    old_word: str, new_word: str, file_paths: list[str], dir_paths: list[str]
) -> None:
    """Renames files and directories.

    Args:
        old_word (str)
        new_word (str)
        file_paths (list[str])
        dir_paths (list[str])
    """
    file_paths = [ROOT_DIR / path for path in file_paths]
    dir_paths = [ROOT_DIR / path for path in dir_paths]

    for path in file_paths:
        with open(path, encoding="utf-8") as file:
            contents = file.read()
        new_contents = contents.replace(old_word, new_word)

        with open(path, "w", encoding="utf-8") as file:
            file.write(new_contents)

        new_path = path.with_name(path.name.replace(old_word, new_word))
        path.rename(new_path)

    for path in dir_paths:
        new_path = path.with_name(path.name.replace(old_word, new_word))
        path.rename(new_path)


def main() -> None:
    """Main function that setups the project."""
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
    while True:
        new_user_name = input("Enter GitHub username (oedokumaci): ") or "oedokumaci"
        new_user_email = (
            input("Enter GitHub email (oral.ersoy.dokumaci@gmail.com): ")
            or "oral.ersoy.dokumaci@gmail.com"
        )
        answer = (
            input(
                f"Is the information correct? [y/n] (y) {new_user_name} {new_user_email} "
            )
            or "y"
        )
        if answer == "y":
            break
    rename_files("oedokumaci", new_user_name, USER_REPLACE_PATHS, [])
    rename_files(
        "oral.ersoy.dokumaci@gmail.com", new_user_email, USER_REPLACE_PATHS, []
    )

    # GitHub configuration
    print("Configuring GitHub project locals...")
    subprocess.run(["git", "config", "user.name", new_user_name], check=True)
    subprocess.run(["git", "config", "user.email", new_user_email], check=True)
    print("GitHub project locals configured.")

    # Rename README.md
    if (ROOT_DIR / "README.md").exists():
        (ROOT_DIR / "README.md").unlink()
    (ROOT_DIR / "README_main.md").rename(ROOT_DIR / "README.md")

    # Remove three pdm files from the project
    files = ["pdm.lock", "pyproject.toml", "requirements.txt"]
    for file in files:
        if OS == "windows-based":
            subprocess.run(["del", file], check=True)
        else:
            subprocess.run(["rm", file], check=True)

    # Run pdm init
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
    subprocess.run(["pdm", "add", "-dG", "test", "pytest"], check=True)
    subprocess.run(["pdm", "run", "pre-commit", "install"], check=True)
    try:
        subprocess.run(
            ["pdm", "run", "pre-commit", "run", "--all-files", "pdm-export"], check=True
        )
    except subprocess.CalledProcessError:
        print("Pdm-export expected to fail during setup, this is normal. Continuing...")
    subprocess.run(["pdm", "fix"], check=True)

    # Generate .vscode/settings.json
    answer = input("Do you want to generate .vscode/settings.json? [y/n] (y) ") or "y"
    if answer == "y":
        (ROOT_DIR / ".vscode").mkdir(exist_ok=True)
        file = ROOT_DIR / ".vscode" / "settings.json"
        file.touch()
        with open(file, "w", encoding="utf-8") as file:
            file.write(
                f"""
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": ["--max-line-length=88", "--select=C,E,F,W,B", "--extend-ignore=B009,E203,E501,W503"],
    "python.autoComplete.extraPaths": [".venv/lib/python{PYTHON_VER}/site-packages"],
    "python.analysis.extraPaths": [".venv/lib/python{PYTHON_VER}/site-packages"],
    "python.testing.pytestPath": ".venv/bin/pytest"
}
                """
            )

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

    print("Setup complete!")


if __name__ == "__main__":
    raise SystemExit(main())
