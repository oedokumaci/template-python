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
    subprocess.run(["git", "config", "user.name", new_user_name], check=True)
    subprocess.run(["git", "config", "user.email", new_user_email], check=True)

    # Rename README.md
    if (CURRENT_PROJECT_PATH / "README.md").exists():
        (CURRENT_PROJECT_PATH / "README.md").unlink()
        (CURRENT_PROJECT_PATH / "README_main.md").rename(
            CURRENT_PROJECT_PATH / "README.md"
        )

    # Run pdm install
    try:
        subprocess.run(["pdm", "--version"], check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["pip3", "install", "pdm"], check=True)
        except subprocess.CalledProcessError:
            subprocess.run(["pip", "install", "pdm"], check=True)
    subprocess.run(["rm", "requirements.txt"], check=True)
    subprocess.run(["pdm", "init", "--python", "3.10"], check=True)
    subprocess.run(["pdm", "add", "typer"], check=True)
    subprocess.run(["pdm", "add", "pyyaml"], check=True)
    subprocess.run(["pdm", "add", "-dG", "workflow", "pdm"], check=True)
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
        (CURRENT_PROJECT_PATH / ".vscode").mkdir(exist_ok=True)
        file = CURRENT_PROJECT_PATH / ".vscode" / "settings.json"
        file.touch()
        with open(file, "w", encoding="utf-8") as file:
            file.write(
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

    # Add .pdm.toml to .gitignore
    with open(CURRENT_PROJECT_PATH / ".gitignore", "r+", encoding="utf-8") as file:
        contents = file.readlines()
        index_to_add = contents.index(".pdm-python\n")
        contents.insert(index_to_add, ".pdm.toml\n")
        file.seek(0)
        file.writelines(contents)

    # Remove template setup file
    try:
        subprocess.run(["rm", "-rf", f"{Path(__file__).name}"], check=True)
    except subprocess.CalledProcessError:
        pass

    # Git add commit and push
    answer = input("Do you want to git add commit and push? [y/n] (y) ") or "y"
    if answer == "y":
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initialize using template_setup.py"], check=True
        )
        subprocess.run(["git", "push"], check=True)

    # Remove cached files
    try:
        subprocess.run(["rm", "-rf", ".mypy_cache"], check=True)
    except subprocess.CalledProcessError:
        pass
    try:
        subprocess.run(["rm", "-rf", ".pytest_cache"], check=True)
    except subprocess.CalledProcessError:
        pass

    print("Setup complete!")


if __name__ == "__main__":
    raise SystemExit(main())
