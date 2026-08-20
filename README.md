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

Current scope: this repository runs Selenium UI tests only. If API, visual, performance, or other test types are added later, document their commands in separate sections so the Selenium runbook stays clear.

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

## Current Run Commands

Run all tests:

```bash
poetry run pytest
```

Run the current smoke suite:

```bash
poetry run pytest tests/smoke
```

Run the current Sauce Demo smoke test directly:

```bash
poetry run pytest tests/smoke/test_sauce_demo_home_page.py
```

Run browser tests in headless mode:

```bash
poetry run pytest --headless
```

Run the smoke marker:

```bash
poetry run pytest -m smoke
```

Run the UI marker:

```bash
poetry run pytest -m ui
```

Run all tests except tests marked as slow:

```bash
poetry run pytest -m "not slow"
```

Run tests matching a name expression:

```bash
poetry run pytest -k sauce_demo
```

Collect tests without running them:

```bash
poetry run pytest --collect-only
```

Run tests with verbose output:

```bash
poetry run pytest -v
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

Run the smoke test headlessly and refresh Allure results:

```bash
poetry run pytest tests/smoke --headless --clean-alluredir --alluredir=allure-results
```

The `regression` and `slow` markers are registered in `pytest.ini` for future expansion. They should be used once matching tests exist.

## Allure Commands

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

Generated downloads are cleaned at the start of each test session. Committed upload files and static fixtures remain under `data/uploads/` and `data/fixtures/`.

## GitHub Actions

The Selenium workflow runs only in these cases:

- when a pull request targeting `main` is opened;
- every day at 04:00 UTC, using the `smoke` marker;
- when started manually with the `smoke`, `regression`, `e2e`, or `all` selection.

Pull-request runs execute changed test modules. Changes to shared framework or test
configuration run the smoke suite as a fallback. Documentation-only pull requests do
not start Selenium.

Every executed CI test run uses headless Chrome and creates a downloadable
`selenium-allure-<event>-<run-number>` artifact. The artifact contains the generated
`allure-report/`, raw `allure-results/`, and available screenshots and logs. Download and
extract the artifact, then open the generated report with:

```powershell
cmd /c "allure open allure-report"
```

The pull-request workflow runs only on the initial opened event. Later commits, pushes,
synchronization events, and reopened pull requests do not trigger another run.

## Poetry Commands

Show installed project dependencies:

```bash
poetry show
```

Show the dependency tree:

```bash
poetry show --tree
```

Check the Poetry project configuration:

```bash
poetry check
```

## Quality Commands

Run Ruff checks:

```bash
poetry run ruff check .
```

Run Ruff checks on selected files:

```bash
poetry run ruff check src tests
```

Format with Ruff:

```bash
poetry run ruff format .
```

Check formatting without changing files:

```bash
poetry run ruff format --check .
```

Install the Git pre-commit hook:

```bash
poetry run pre-commit install
```

After installation, every `git commit` runs the configured checks before the
commit is created.

Run pre-commit checks against staged files:

```bash
poetry run pre-commit run
```

The hook runs Ruff checks and formatting against changed Python files, then
collects the pytest suite to verify test discovery, imports, syntax during
collection, and pytest configuration without executing tests.

Run pre-commit checks against all files:

```bash
poetry run pre-commit run --all-files
```

Run the Ruff pre-commit hooks only:

```bash
poetry run pre-commit run ruff-check --all-files
poetry run pre-commit run ruff-format --all-files
```

## AI Council Reference

The planned AI Council workflow is documented in [ai-council-plan.md](plans/ai-council-plan.md). It defines the planned subagents, question gate, user challenge loop, approval gate, and implementation-worker flow.

Example planning prompt:

```text
Use AI Council to review this idea. Do not implement. Ask me blocking and decision questions before producing the final plan.
Task: <task>
```

Example implementation prompt:

```text
Use AI Council for this implementation. First run council review, collect questions and disagreements, ask me for answers, then ask for final approval. Only after approval, use implementation_worker for the approved code changes.
Task: <task>
```

Example challenge prompt:

```text
Council challenge: <decision or assumption> is wrong because <context>. Re-run the relevant council agents and update the plan.
```

## Project Plan

See [framework-plan.md](plans/framework-plan.md) for the implementation plan and open decisions.

See [ai-council-plan.md](plans/ai-council-plan.md) for the planned AI Council workflow.

See [AGENTS.md](AGENTS.md) for Codex development rules.
