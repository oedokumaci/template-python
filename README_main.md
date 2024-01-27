<div align="center">

<!-- Provide information on your repository here. -->

template-python

<!-- <img src=./style/repo.png width="800"> -->

&nbsp;

![Tests](https://github.com/oedokumaci/template-python/actions/workflows/tests.yml/badge.svg)
![Quality](https://github.com/oedokumaci/template-python/actions/workflows/quality.yml/badge.svg)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

&nbsp;

# Table of Contents

- [Table of Contents](#table-of-contents)
- [User Guide](#user-guide)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Using Docker](#using-docker)
    - [Download Zip File](#download-zip-file)
    - [Using Git](#using-git)
  - [Usage](#usage)
    - [Configuration](#configuration)
    - [Quick Start](#quick-start)
    - [Detailed Usage](#detailed-usage)
- [Developer Guide](#developer-guide)
  - [Makefile](#makefile)
  - [Setup](#setup)
  - [Development](#development)
    - [Pre-commit Hooks](#pre-commit-hooks)

&nbsp;

# User Guide

## Requirements

- Python >= 3.10
- OS: Ubuntu, MacOS, Windows

## Installation

There are three easy ways to install the package.

### Using Docker

The easiest way to run the project is to use Docker. First, install [Docker](https://docs.docker.com/get-docker/). Then, run the following command in the project directory.
```bash
docker build -t template-python .
```
This will build the Docker image. After the image is built, the following are some examples of how to run the project.

```bash
docker run --rm -it -v "PATH_TO_YOUR_CONFIG.yaml:/usr/src/app/config/config.yaml" -e environment_variable=ENVIRONMENT_VARIABLE template-python
```

These commands will run the project with the specified config file and cli arguments. The output can be seen in the terminal. The `-v` option mounts the specified config file to the container. The `-e` option sets the environment variable to the specified value. The `--rm` option removes the container after it exits. You can also not use the `--rm` option to keep the container after it exits and see the logs. The `-it` option is for interactive mode.


### Download Zip File

Pip installing the package from PyPI is not yet available. Instead, download [from this link](https://github.com/oedokumaci/template-python/archive/refs/heads/main.zip) and unzip. You will also need to change the folder name from template-python-main to template-python (or cd into template-python-main in step 2 below). 

### Using Git

If you have git installed, simply run 
```bash
git clone https://github.com/oedokumaci/template-python
```
to install the package locally. After downloading, here are the steps to install the dependencies in a virtual environment using [PDM]:

1. `pip install pdm`
2. `cd template-python`
3. `pdm install --prod`
   
## Usage

### Configuration

First edit the `./config/config.yaml` to your liking. Example config files can be found at `./config/`.

### Quick Start

After configuring the `./config/config.yaml`, simply run the following command in the project directory.
```bash
pdm run python -m template_python
```

### Detailed Usage
For a list of all the CLI arguments and options, run
```bash
pdm run python -m template_python --help
```

&nbsp;

# Developer Guide

## Makefile
There is a Makefile in the project directory. You can run `make help` to see the available commands as below. The Makefile is also used in the CI/CD pipeline.

<img src=./style/make.png width="600">

## Setup

This project is [PDM]-managed, which is compatible with [PEP 621](https://www.python.org/dev/peps/pep-0621) (also compatible with the <i>rejected</i> [PEP 582](https://www.python.org/dev/peps/pep-0582)). If you are a developer, first `pip install pdm` and then `git clone` the project. Next you can `pdm install` in the project directory, which will install all the dependencies in a [virtual environment](https://pdm.fming.dev/latest/usage/venv/).

## Development

### Pre-commit Hooks

The project also uses pre-commit hooks. Because the project uses [PDM], you **do not** need to `pip install pre-commit`. Instead, run directly
```bash
pdm run pre-commit install
```
in the project directory to install hooks to your local `.git`. Alternatively, you can also activate the virtual environment and run
```bash
pre-commit install
```

[PDM]: https://pdm.fming.dev
