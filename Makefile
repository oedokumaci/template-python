.PHONY: help setup update-dev update-user vscode-settings run docker-build docker-run docker docker-logs docker-stop docker-kill docker-show docker-prune project-help test pre-commit purge-logs clean

help:  ## Show this help message for each Makefile recipe
ifeq ($(OS),Windows_NT)
	@findstr /R /C:"^[a-zA-Z0-9 -]\+:.*##" $(MAKEFILE_LIST) | awk -F ':.*##' '{printf "\033[1;32m%-15s\033[0m %s\n", $$1, $$2}' | sort
else
	@awk -F ':.*##' '/^[^ ]+:[^:]+##/ {printf "\033[1;32m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort
endif

setup:  ## Setup project
	pdm install
	pdm run pre-commit install
	make test

update-dev:  ## Update project dependencies for development
	pdm update
	pdm run pre-commit autoupdate
	make test

update-user:  ## Download latest project version and dependencies for user
	git pull
	pdm sync
	make test

vscode-settings:  ## Generate VSCode settings file
	@mkdir -p .vscode
ifeq ($(OS),Windows_NT)
	@echo { > .vscode/settings.json
	@echo "    \"flake8.args\": [\"--max-line-length=88\", \"--select=C,E,F,W,B\", \"--extend-ignore=B009,E203,E501,W503\"]," >> .vscode/settings.json
	@echo "    \"python.autoComplete.extraPaths\": [\".venv/Lib/site-packages\"]," >> .vscode/settings.json
	@echo "    \"python.analysis.extraPaths\": [\".venv/Lib/site-packages\"]," >> .vscode/settings.json
	@echo "    \"python.testing.pytestPath\": \".venv/Scripts/pytest\"" >> .vscode/settings.json
	@echo } >> .vscode/settings.json
else
	@echo '{' > .vscode/settings.json
	@echo '    "flake8.args": ["--max-line-length=88", "--select=C,E,F,W,B", "--extend-ignore=B009,E203,E501,W503"],' >> .vscode/settings.json
	@echo '    "python.autoComplete.extraPaths": [".venv/lib/python3.10/site-packages"],' >> .vscode/settings.json
	@echo '    "python.analysis.extraPaths": [".venv/lib/python3.10/site-packages"],' >> .vscode/settings.json
	@echo '    "python.testing.pytestPath": ".venv/bin/pytest"' >> .vscode/settings.json
	@echo '}' >> .vscode/settings.json
endif

run:  ## Run project
	pdm run python -m template_python

docker-build: ## Build Docker image for the project
	sudo docker build -t template-python .

docker-run: ## Run Docker container from the image in detached mode
	sudo docker run --rm -it \
	-v $(PWD)/data:/usr/src/app/data \
	-v $(PWD)/logs:/usr/src/app/logs \
	-v $(PWD)/outputs:/usr/src/app/outputs \
	--name template-python-app \
	template-python

docker: clean docker-build docker-run ## Clean, build and run Docker container

docker-logs: ## Show Docker container logs
	sudo docker logs -f template-python-app

docker-stop: ## Stop Docker container
	sudo docker stop template-python-app

docker-kill: ## Kill Docker container
	sudo docker kill template-python-app

docker-show: ## Show Docker containers
	sudo docker ps -a

docker-prune: ## Prune Docker system
	sudo docker system prune -a

project-help:  ## Show project help
	pdm run python -m template_python --help

test:  ## Run tests
	pdm run pytest tests -v

pre-commit: clean  ## Run pre-commit
	pdm run pre-commit run --all-files

purge-logs:  ## Prompt user to purge logs that end with .log
ifeq ($(OS),Windows_NT)
	@for /r %%i in (logs\*.log) do @echo %%i
	@echo "Purge logs? [y/N]"
	@set /p choice=
	@if /I "$(choice)"=="y" del /q logs\*.log
else
	@find logs -name "*.log" -print
	@echo "Purge logs? [y/N]"
	@read -r choice; if [ "$$choice" = "y" ]; then rm -f logs/*.log; fi
endif

clean:  ## Clean cached files
ifeq ($(OS),Windows_NT)
	del /q logs\pytest_test.log || :
	rmdir /s /q .mypy_cache || :
	rmdir /s /q .pytest_cache || :
	rmdir /s /q src\template_python\__pycache__ || :
	rmdir /s /q tests\__pycache__ || :
else
	rm -f logs/pytest_test.log
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf src/template_python/__pycache__
	rm -rf tests/__pycache__
endif
