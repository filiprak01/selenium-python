# selenium-python

Repository for a Selenium-based UI testing framework supported by Codex.

## Stack

- Python 3.12
- Selenium
- Chrome as the first supported browser
- pytest
- Allure
- Poetry
- Ruff
- python-dotenv
- YAML configuration
- GitHub Actions

## Setup

Check Python before creating the Poetry environment:

```bash
python --version
py -3.12 --version
```

Create or select a Poetry environment:

```bash
poetry env use 3.12
```

Install dependencies after `pyproject.toml` is created:

```bash
poetry install
```

Local secrets should be provided through environment variables. Start from `.env.example` and ask the team for the real values. CI/CD secrets will be provided through GitHub Secrets.

Configuration files will use YAML and live under `config/`. Paths should be project-root-relative and resolved by the framework.

Chrome is the first planned browser. Selenium Chrome setup will be implemented in the framework WebDriver factory and Chrome options modules, with browser behavior configured through YAML.

## Test Commands

Run all tests:

```bash
poetry run pytest
```

Run smoke tests:

```bash
poetry run pytest tests/smoke
```

Run by marker:

```bash
poetry run pytest -m smoke
poetry run pytest -m regression
```

Run tests with Allure result output:

```bash
poetry run pytest --alluredir=allure-results
```

Serve the Allure report locally:

```bash
allure serve allure-results
```

Local runs are planned to be headed by default. GitHub Actions runs are planned to be headless by default.

## Quality Commands

Run Ruff checks:

```bash
poetry run ruff check .
```

Format with Ruff:

```bash
poetry run ruff format .
```

Run pre-commit checks after pre-commit is configured:

```bash
poetry run pre-commit run --all-files
```

## Project Plan

See [framework-plan.md](plans/framework-plan.md) for the implementation plan and open decisions.

See [AGENTS.md](AGENTS.md) for Codex development rules.
