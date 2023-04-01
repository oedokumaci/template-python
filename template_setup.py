"""This module is to setup the new project."""

import subprocess
from pathlib import Path

CURRENT_PROJECT_PATH = Path(__file__).parent

USER_REPLACE_PATHS = ["pyproject.toml", "README_main.md"]
SRC_PATHS = [str(path) for path in (CURRENT_PROJECT_PATH / "src").rglob("*.py")]
TESTS_PATHS = [str(path) for path in (CURRENT_PROJECT_PATH / "tests").rglob("*.py")]

FILE_PATHS = USER_REPLACE_PATHS + SRC_PATHS + TESTS_PATHS
DIR_PATHS = [str(CURRENT_PROJECT_PATH / "src" / "template_python")]


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
    file_paths = [CURRENT_PROJECT_PATH / path for path in file_paths]
    dir_paths = [CURRENT_PROJECT_PATH / path for path in dir_paths]

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
    # Rename file contents, names, and directories
    rename_files("template-python", CURRENT_PROJECT_PATH.name, FILE_PATHS, [])
    rename_files(
        "template_python",
        CURRENT_PROJECT_PATH.name.replace("-", "_"),
        FILE_PATHS,
        DIR_PATHS,
    )
    print("Setting up the project...")
    print("Prompt default values are in parentheses, press enter to accept them.")
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
    subprocess.check_call(["git", "config", "user.name", new_user_name])
    subprocess.check_call(["git", "config", "user.email", new_user_email])

    # Rename README.md
    if (CURRENT_PROJECT_PATH / "README.md").exists():
        (CURRENT_PROJECT_PATH / "README.md").unlink()
        (CURRENT_PROJECT_PATH / "README_main.md").rename(
            CURRENT_PROJECT_PATH / "README.md"
        )

    # Add this file to .gitignore
    with open(CURRENT_PROJECT_PATH / ".gitignore", "a", encoding="utf-8") as f:
        f.write("\n" + "# Template setup file" + "\n" + Path(__file__).name + "\n")

    subprocess.check_call(["git", "rm", "--cached", Path(__file__).name])

    # Run pdm install
    try:
        subprocess.check_call(["pdm", "--version"])
    except subprocess.CalledProcessError:
        try:
            subprocess.check_call(["pip3", "install", "pdm"])
        except subprocess.CalledProcessError:
            subprocess.check_call(["pip", "install", "pdm"])
    subprocess.check_call(["rm", "requirements.txt"])
    subprocess.check_call(["pdm", "self", "update"])
    subprocess.check_call(["pdm", "init", "--python", "3.10"])
    subprocess.check_call(["pdm", "add", "typer"])
    subprocess.check_call(["pdm", "add", "pyyaml"])
    subprocess.check_call(["pdm", "add", "-dG", "workflow", "pdm"])
    subprocess.check_call(["pdm", "add", "-dG", "workflow", "pre-commit"])
    subprocess.check_call(["pdm", "add", "-dG", "test", "pytest"])
    subprocess.check_call(["pdm", "run", "pre-commit", "install"])
    try:
        subprocess.check_call(
            ["pdm", "run", "pre-commit", "run", "--all-files", "pdm-export"]
        )
    except subprocess.CalledProcessError:
        print("Pdm-export expected to fail, this is normal. Continuing...")

    # Generate .vscode/settings.json
    answer = input("Do you want to generate .vscode/settings.json? [y/n] (y) ") or "y"
    if answer == "y":
        (CURRENT_PROJECT_PATH / ".vscode").mkdir(exist_ok=True)
        file = CURRENT_PROJECT_PATH / ".vscode" / "settings.json"
        file.touch()
        with open(file, "w", encoding="utf-8") as f:
            f.write(
                """
{
    "python.linting.pylintEnabled": false,
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": ["--max-line-length=88", "--select=C,E,F,W,B", "--extend-ignore=B009,E203,E501,W503"],
    "python.autoComplete.extraPaths": ["__pypackages__/3.10/lib"],
    "python.analysis.extraPaths": ["__pypackages__/3.10/lib"],
    "python.testing.pytestPath": "__pypackages__/3.10/bin/pytest"
}
                """
            )

    # Git add commit and push
    answer = input("Do you want to git add commit and push? [y/n] (y) ") or "y"
    if answer == "y":
        subprocess.check_call(["git", "add", "."])
        subprocess.check_call(
            ["git", "commit", "-m", "Initialize using template_setup.py"]
        )
        subprocess.check_call(["git", "push"])


if __name__ == "__main__":
    raise SystemExit(main())
