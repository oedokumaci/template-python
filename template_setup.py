import subprocess
from pathlib import Path

CURRENT_PROJECT_PATH = Path(__file__).parent

FILE_PATHS = (
    ["pyproject.toml", "README_main.md"]
    + [str(path) for path in (CURRENT_PROJECT_PATH / "src").rglob("*.py")]
    + [str(path) for path in (CURRENT_PROJECT_PATH / "tests").rglob("*.py")]
)
DIR_PATHS = [str(CURRENT_PROJECT_PATH / "src" / "template")]

USER_REPLACE_PATHS = ["pyproject.toml", "README_main.md"]


def rename_files(
    old_word: str, new_word: str, file_paths: list[str], dir_paths: list[str]
) -> None:
    file_paths = [CURRENT_PROJECT_PATH / path for path in file_paths]
    dir_paths = [CURRENT_PROJECT_PATH / path for path in dir_paths]
    for path in file_paths:
        with open(path, encoding="utf-8") as f:
            contents = f.read()
        new_contents = contents.replace(old_word, new_word)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_contents)
        new_path = path.with_name(path.name.replace(old_word, new_word))
        path.rename(new_path)
    for path in dir_paths:
        new_path = path.with_name(
            path.name.replace(old_word, new_word.replace("_", "-"))
        )
        path.rename(new_path)


if __name__ == "__main__":
    # Rename file contents, names, and directories
    rename_files("template", CURRENT_PROJECT_PATH.name, FILE_PATHS, DIR_PATHS)
    while True:
        new_user_name = input("Enter Github username: ")
        new_user_email = input("Enter Github email: ")
        answer = (
            input(
                f"Is the information correct? (y/n) {new_user_name} {new_user_email} "
            )
            or "y"
        )
        if answer == "y":
            break
    rename_files("oedokumaci", new_user_name, USER_REPLACE_PATHS, [])
    rename_files(
        "oral.ersoy.dokumaci@gmail.com", new_user_email, USER_REPLACE_PATHS, []
    )

    # Rename README.md
    if (CURRENT_PROJECT_PATH / "README.md").exists():
        (CURRENT_PROJECT_PATH / "README.md").unlink()
        (CURRENT_PROJECT_PATH / "README_main.md").rename(
            CURRENT_PROJECT_PATH / "README.md"
        )

    # Add this file to .gitignore
    with open(CURRENT_PROJECT_PATH / ".gitignore", "a", encoding="utf-8") as f:
        f.write("\n" + "# Template setup file" + "\n" + Path(__file__).name + "\n")

    # Run pdm install
    try:
        subprocess.run(["pdm", "--version"])
    except FileNotFoundError:
        try:
            subprocess.run(["pip3", "install", "pdm"])
        except FileNotFoundError:
            subprocess.run(["pip", "install", "pdm"])
    # make __pypackages__ directory
    (CURRENT_PROJECT_PATH / "__pypackages__").mkdir(exist_ok=True)
    subprocess.run(["pdm", "lock", "-v"])
    subprocess.run(["pdm", "install"])
    subprocess.run(["pdm", "run", "pre-commit", "install"])
