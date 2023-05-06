<div align="center">

This is a template Python repository to start a fresh project with a default setup.

![Tests](https://github.com/oedokumaci/template-python/actions/workflows/tests.yml/badge.svg)
![Quality](https://github.com/oedokumaci/template-python/actions/workflows/quality.yml/badge.svg)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

The project setup includes:

- Python >= 3.10
- Ubuntu, MacOS, Windows latest OS versions
- [PDM](https://pdm.fming.dev/latest/) for dependency management
- [GitHub Actions](https://github.com/features/actions) and [pre-commit](https://pre-commit.com/) for linting, formatting, CI/CD
  - [Black](https://black.readthedocs.io/en/stable/#) for code formatting
  - [Mypy](https://mypy.readthedocs.io/en/stable/) for static type checking
  - [Pytest](https://docs.pytest.org/) for testing
- [MIT](https://en.wikipedia.org/wiki/MIT_License) license
- The above badges of this README.md

# Getting Started

1. Install [Python](https://www.python.org/downloads/) 3.10 in your local machine. For MacOS use
```zsh
brew install python@3.10
```
2. Click on the `Use this template` button [at this page](https://github.com/oedokumaci/template-python) to create a new repository from this template (you must be logged in to GitHub to see the button).
3. Name your repository and click `Create repository from template`. If the repository name is more than one word, make sure to use -hyphens- instead of spaces or underscores.
4. Git clone the repository to your local machine.
5. Cd into the repository directory.
6. Run template_setup.py with
```zsh
python template_setup.py [--user-name YOUR_GIT_USER_NAME] [--user-email YOUR_GIT_USER_EMAIL]
```
7. Follow the instructions in the terminal.

### Running the setup script will:
 - Rename file contents, names, and directories that contains template repository name with the new repository name
 - Rename user name and user email in and `README_main.md`
 - Configure GitHub user name and user email locally
 - Remove `pdm.lock`, `pyproject.toml`, and `requirements.txt`
 - Remove `README.md` and rename `README_main.md` to `README.md`
 - If not installed pip install [PDM](https://pdm.fming.dev/latest/) in your local machine
 - Update PDM to the latest version
 - [PDM](https://pdm.fming.dev/latest/) init with Python 3.10. Select the default options (hit `Enter`) when prompted except:
   - Select `y` to make project installable
 - Install dependencies with [PDM](https://pdm.fming.dev/latest/)
 - Install [pre-commit](https://pre-commit.com/) hooks to local `.git` folder
 - Prompt user an option include `.vscode/settings.json`
 - Remove `template_setup.py`
 - Prompt user an option to git add commit and push
 - Remove `.mypy_cache` and `.pytest_cache` folders
