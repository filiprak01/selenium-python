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

Install the locked dependencies:

```bash
poetry install
```

Local secrets should be provided through environment variables. Start from `.env.example` and ask the team for the real values. CI/CD secrets will be provided through GitHub Secrets.

The single test environment is configured in `config/default.yaml`. Paths are project-root-relative and resolved by the framework.

The source root is `src/`, with framework responsibilities kept in direct child directories: `assertions/`, `clients/`, `config/`, `flows/`, `locators/`, `logging/`, `models/`, `pages/`, and `webdriver/`; project-root-relative paths are defined in `src/project.py`. Framework capabilities are verified through browser tests against the configured test URL, starting with the Sauce Demo home-page smoke test. Broader application coverage will be added incrementally.

The first page-load check waits up to 5 seconds for the Sauce Demo logo and polls once per second. Each named UI step logs its START/PASS/FAIL status in English. Screenshots are captured only through explicit screenshot steps by default, such as `UIClient.capture_screenshot_step(...)`, and are saved under `screenshots/`; failed browser tests additionally attach the execution log, page source, browser logs, and a failure screenshot.

Per-step screenshots are configurable in `config/default.yaml`. The default is `screenshot_after_steps: false` so local, CI, and pipeline runs stay lighter. Testers can set it to `true` when they need screenshot documentation after every named Allure UI step.

At the start of every pytest session, the framework removes generated files from `allure-results/`, `allure-report/`, `screenshots/`, `logs/`, and `data/downloads/`. Static input data under `data/uploads/` and `data/fixtures/` is preserved.

Chrome is the first planned browser. Selenium Chrome setup will be implemented in the framework WebDriver factory and Chrome options modules, with browser behavior configured through YAML.

## Test Commands

Run all tests:

```bash
poetry run pytest
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

For a clean Allure results directory on each run, use:

```bash
poetry run pytest --clean-alluredir --alluredir=allure-results
```

Run the smoke test and refresh Allure results:

```bash
poetry run pytest tests/smoke --clean-alluredir --alluredir=allure-results
```

Serve a fresh Allure report from the current result files:

```powershell
allure.cmd serve allure-results
```

If PowerShell blocks scripts, run Allure through `cmd`:

```powershell
cmd /c "allure serve allure-results"
```

Do not open an old `allure-report/` directory after a new run. `allure-results/` contains raw test results for `allure serve`; `allure-report/` is a generated static report for `allure open`.

Generate a static Allure report directory:

```powershell
Remove-Item -LiteralPath .\allure-report -Recurse -Force -ErrorAction SilentlyContinue
cmd /c "allure generate allure-results -o allure-report"
cmd /c "allure open allure-report"
```

Local runs are headed by default. GitHub Actions runs use headless mode by default.

Use `--headless` to run browser tests without a visible Chrome window:

```bash
poetry run pytest --headless
```

Generated downloads are cleaned at the start of each test session. Committed upload files and static fixtures remain under `data/uploads/` and `data/fixtures/`.

## Quality Commands

Run Ruff checks:

```bash
poetry run ruff check .
```

Format with Ruff:

```bash
poetry run ruff format .
```

Run pre-commit checks:

```bash
poetry run pre-commit run --all-files
```

## Project Plan

See [framework-plan.md](plans/framework-plan.md) for the implementation plan and open decisions.

See [AGENTS.md](AGENTS.md) for Codex development rules.
