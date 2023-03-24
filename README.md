<div align="center">

This is a template Python repository to start a fresh project with a default setup.

![Tests](https://github.com/oedokumaci/template-python/actions/workflows/tests.yml/badge.svg)
![Quality](https://github.com/oedokumaci/template-python/actions/workflows/quality.yml/badge.svg)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

The set up includes:

- [PDM](https://pdm.fming.dev/latest/) for dependency management
- [GitHub Actions](https://github.com/features/actions) and [pre-commit](https://pre-commit.com/) for linting, formatting, CI/CD
  - [Black](https://black.readthedocs.io/en/stable/#) for code formatting
  - [Mypy](https://mypy.readthedocs.io/en/stable/) for static type checking
  - [Pytest](https://docs.pytest.org/) for testing
- [MIT](https://en.wikipedia.org/wiki/MIT_License) license


# Getting Started

1. Click on the `Use this template` button to create a new repository from this template.
2. Name your repository and click `Create repository from template`. If the repository name is more than one word, make sure to use hyphens instead of spaces or underscores.
3. Clone the repository to your local machine.
4. Cd into the repository directory.
5. Run template_setup.py with
```bash
python template_setup.py
```

### Running the setup script will:
 - Rename file contents, names, and directories that contains template repository name with the new repository name
 - Rename user name in `pyproject.toml` and `README_main.md`
 - Rename user email in `pyproject.toml`
 - Remove README.md and rename `README_main.md` to `README.md`
 - Add `template_setup.py` to `.gitignore`
 - Install dependencies with [PDM](https://pdm.fming.dev/latest/)
 - Install [pre-commit](https://pre-commit.com/) hooks to local `.git` folder
