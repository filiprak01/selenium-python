# Selenium UI Testing Framework Plan

## Goal

Create an AI-supported Selenium UI testing framework in Python. The framework will use the Page Object Model (POM), Poetry for dependency management, pytest for execution, Allure for reporting, YAML for readable configuration, and GitHub Actions for CI/CD.

The repository should support both human-written and future AI-generated UI tests with clear structure, predictable naming, and strict separation between tests, page objects, locators, flows, clients, configuration, paths, and evidence capture.

## Confirmed Decisions

- `src/` is the source root. Framework code will live in its direct child directories, with `project.py` directly under `src/`.
- Direct framework source directories will be `assertions/`, `clients/`, `config/`, `flows/`, `locators/`, `logging/`, `models/`, `pages/`, and `webdriver/`.
- Tests will live in `tests/`.
- Python target version will be 3.12.
- Selenium will be used for browser automation.
- Chrome will be the first supported browser.
- pytest will be used as the test runner.
- Allure will be used for reporting.
- Poetry will manage dependencies and virtual environments.
- GitHub Actions will be used for CI/CD.
- CI/CD runs will be headless.
- Local runs will be headed by default.
- Secrets will be loaded from environment variables.
- GitHub Actions will use GitHub Secrets for CI/CD secrets.
- Config files will use YAML for human readability.
- Environment URLs and configurable framework values will live in `config/`.
- Configuration will be loaded into Python dataclass models.
- Pydantic can be considered later if stronger validation is needed.
- Timeout constants will live in `src/models/`.
- OS-specific behavior will be represented in configuration where needed.
- Project paths will derive from the repository root instead of hardcoded absolute paths.
- A `project.py` module will define project-root-relative paths such as data, upload, download, fixture, config, report, log, and screenshot paths.
- Business behavior and UI manipulation helpers will live in `flows/`.
- `UIClient` will own UI test session details and provide high-level access to pages, flows, and WebDriver.
- A future client pool will be added when multiple clients/sessions are needed.
- Locators will be stored separately from page objects.
- Page objects can expose indirect assertion helpers, preferably through assertion functions and wait-backed checks.
- Page objects should include built-in waits where needed to avoid brittle tests.
- Ruff will be added for linting and formatting.
- Selenium Grid and remote WebDriver are out of scope for the initial presentation framework.
- Initial browser support will focus on Chrome while keeping browser selection configurable.
- Framework capabilities will be verified through browser tests against the configured test URL, starting with the Sauce Demo home-page smoke test. Broader application test cases will be added incrementally.
- Local `.env` files will be loaded with `python-dotenv`.
- Pre-commit will be added later to run Ruff before commits.
- Work should not happen directly on `main`; implementation branches should use `feature/<descriptive-name>`.
- Agents should prefer scalable framework structure over short-term simplicity.
- Functions and methods should include explicit return types.
- Dependency versions and relevant package updates should be checked before implementation work that touches dependencies or integrations.
- Subfolder `AGENTS.md` files provide focused context for agents working in specific framework areas.

## Proposed Project Structure

```text
.
|-- .github/
|   `-- workflows/
|       `-- ui-tests.yml
|-- .env.example
|-- AGENTS.md
|-- README.md
|-- pyproject.toml
|-- poetry.lock
|-- pytest.ini
|-- plans/
|   `-- framework-plan.md
|-- config/
|   |-- AGENTS.md
|   |-- default.yaml
|   `-- environments/
|       |-- local.yaml
|       |-- staging.yaml
|       `-- production.yaml
|-- data/
|   |-- downloads/
|   |-- uploads/
|   `-- fixtures/
|-- src/
|   |-- AGENTS.md
|   |-- assertions/
|   |   |-- __init__.py
|   |   `-- page_assertions.py
|   |-- clients/
|   |   |-- __init__.py
|   |   |-- client_pool.py
|   |   `-- ui_client.py
|   |-- config/
|   |   |-- __init__.py
|   |   `-- loader.py
|   |-- flows/
|   |   `-- __init__.py
|   |-- locators/
|   |   `-- __init__.py
|   |-- logging/
|   |   |-- __init__.py
|   |   `-- pytest_logging.py
|   |-- models/
|   |   |-- __init__.py
|   |   |-- configuration.py
|   |   `-- constants.py
|   |-- pages/
|   |   |-- __init__.py
|   |   |-- base_page.py
|   |   `-- components/
|   |       `-- __init__.py
|   |-- project.py
|   `-- webdriver/
|       |-- __init__.py
|       |-- chrome_options.py
|       `-- factory.py
`-- tests/
    |-- AGENTS.md
    |-- conftest.py
    |-- smoke/
    |-- regression/
    `-- ui/
```

## Architecture Principles

- Prefer scalable structure over the simplest short-term implementation.
- Keep framework boundaries ready for future browsers, environments, clients, generated tests, and reusable flows.
- When scalability concerns are detected, document the concern and provide an implementation plan for user review before coding.
- Avoid adding abstractions that do not support a realistic framework extension point.

## Framework Layers

### Tests

Tests should describe user-visible behavior and avoid direct Selenium calls.

Responsibilities:

- Arrange test data and configuration.
- Use `UIClient`, page objects, and flows to perform actions.
- Assert behavior through page assertion helpers or dedicated assertion functions.
- Attach useful evidence to Allure reports.

Framework capabilities should be verified through browser tests against the configured test URL. The first application smoke test verifies the Sauce Demo home-page logo; broader application test cases will be added incrementally.

### UI Client

`UIClient` is the main high-level entry point for UI tests.

Responsibilities:

- Own or receive the Selenium WebDriver session.
- Expose access to page objects and flows.
- Keep test code away from low-level WebDriver setup.
- Store test/session details needed by the framework.
- Prepare for a future client pool when multiple UI sessions or roles are needed.

### Page Objects

Page objects represent screens and reusable UI components.

Responsibilities:

- Expose page-specific user actions.
- Use locators from the separate `locators/` package.
- Use explicit waits and stable synchronization.
- Provide indirect assertion helpers such as `assert_loaded()` or `is_error_visible()`.
- Avoid duplicating business flows that belong in `flows/`.

### Locators

Locators are separate from page objects so they can be reviewed, generated, and maintained independently.

Responsibilities:

- Store selectors for pages and components.
- Prefer stable selectors such as `data-testid` when available.
- Keep naming descriptive and behavior-oriented.
- Support both manual locator additions and future discovery-agent generated locators.

The detailed selector strategy will be defined later.

### Flows

`flows/` replaces the earlier broad idea of `utils/page/`.

Flows are reusable behavior and manipulation layers used by tests. They can coordinate multiple pages, prepare UI state, change pages, or execute business actions that are bigger than one page object method.

Examples:

- Login flow.
- Navigation flow.
- File upload flow.
- Role switching flow.
- Test data preparation through the UI.

### Assertions

Assertions should be reusable and readable.

Expected approach:

- Tests can call page assertion helpers.
- Page assertions should use explicit waits where needed.
- Low-level waiting and element checks should be hidden from test files.
- Assertions should produce clear failure messages.

### Config

Configuration files live in `config/` and are parsed into source models under `src/models/`.

Likely configuration values:

- Base URLs.
- Environment name.
- Operating system name or profile.
- Browser type.
- Headless/headed mode default.
- Download directory.
- Upload and fixture directory references.
- Allure evidence settings.
- Optional test behavior flags.

The config file format will be YAML. Timeout constants will live in `src/models/constants.py`.

Secrets must not be stored in config files. Local secrets will be loaded from environment variables, and CI/CD secrets will be provided through GitHub Secrets.

### Project Paths

Path handling should be centralized in `src/project.py`.

Expected responsibilities:

- Detect the repository root.
- Expose project-root-relative paths.
- Use `pathlib.Path` instead of raw string path manipulation.
- Support OS-aware path behavior through config.
- Keep Windows local execution working first.
- Avoid hardcoded absolute paths in tests, page objects, flows, and clients.

Expected paths:

- `PROJECT_ROOT`
- `CONFIG_PATH`
- `DATA_PATH`
- `UPLOADS_PATH`
- `DOWNLOADS_PATH`
- `FIXTURES_PATH`
- `REPORTS_PATH`
- `LOGS_PATH`
- `SCREENSHOTS_PATH`

### Data

The `data/` folder stores files used or produced during testing.

Planned areas:

- `data/uploads/` for committed upload fixtures.
- `data/downloads/` for downloaded files created during test runs.
- `data/fixtures/` for static test fixture files.

Generated downloads should be ignored by Git.

## Pytest Support

Planned pytest support:

- Central fixtures in `tests/conftest.py`.
- Browser/session fixtures for Selenium WebDriver.
- Config fixture loaded once per test session.
- `UIClient` fixture for tests.
- `pytest.ini` with at least `smoke` and `regression` marks registered from the beginning.
- Pytest markers such as `smoke`, `regression`, `ui`, and `slow`.
- Screenshot, page source, and browser log capture on failure.
- Allure attachments for failures and important steps.
- Capability verification through the Sauce Demo home-page smoke test.

pytest command-line options will be finalized during implementation. Likely options are `--env`, `--browser`, `--headless`, `--base-url`, and timeout override support.

## Allure Reporting

Planned Allure support:

- Add `allure-pytest`.
- Generate reports from pytest results.
- Capture screenshots through explicit screenshot steps by default.
- Keep automatic screenshots after every named Allure step configurable and disabled by default for local, CI, and pipeline runs.
- Persist screenshot-step evidence under the configured `screenshots/` directory.
- Clean generated `allure-results/`, `allure-report/`, `screenshots/`, `logs/`, and `data/downloads/` content before each pytest session.
- Attach screenshots on failure.
- Attach page source on failure.
- Attach browser logs where available.
- Write English START/PASS/FAIL execution logs and attach the execution log to failed Allure results.
- Use Allure labels such as feature, story, severity, and suite.
- Wrap important business actions with Allure steps.

## WebDriver Strategy

Initial strategy:

- Local execution uses headed browser mode by default.
- CI/CD execution uses headless browser mode by default.
- Browser selection will be configurable.
- Chrome will be the first supported browser for the presentation repository.
- Local WebDriver support comes first.
- Remote WebDriver and Selenium Grid are not included in the initial implementation.
- The design should avoid blocking future remote execution support.

### Chrome Selenium Setup

Chrome support should be stored and implemented in the following places:

- Dependency declaration: `selenium` in `pyproject.toml`.
- Browser config values: YAML files under `config/`.
- Browser config dataclass: `src/models/configuration.py`.
- WebDriver creation: `src/webdriver/factory.py`.
- Chrome-specific options: `src/webdriver/chrome_options.py`.
- Download path and other local paths: `src/project.py`.

The initial implementation should rely on Selenium's built-in driver management for Chrome where possible, so no ChromeDriver binary should be committed to the repository. If a manual driver path is ever required, it should come from config or environment variables, not from a hardcoded path.

## CI/CD Plan

GitHub Actions will run the UI test workflow.

Planned CI behavior:

- Install Python 3.12 and Poetry.
- Install project dependencies with Poetry.
- Load secrets from GitHub Secrets.
- Run tests in headless mode.
- Store Allure results as workflow artifacts.
- Optionally publish Allure reports later.

Parallel execution with `pytest-xdist` should be considered later, after the base framework is stable.

Flaky test handling should also be considered later, with a preference for better waits and diagnostics before retries.

## Ruff Support

Ruff will be used for formatting and linting.

Recommended starting rules:

- Select core Python correctness and style rules: `E`, `F`, `W`, `I`, `B`, `UP`, `SIM`, `C4`, `ARG`, `PT`, `RUF`, `ANN`.
- Keep import sorting enabled with `I`.
- Enable pytest-focused rules with `PT`.
- Keep line length practical for locator-heavy code, likely `100` or `120`.
- Ignore docstring-enforcement rules at the beginning, especially `D`.
- Keep pytest `assert` statements allowed by ignoring `S101` if security rules are enabled later.
- Enforce explicit return types for functions and methods through the `ANN` rule family where practical.
- Use `-> None` for functions and methods that do not return a value.
- Decide separately whether argument annotations should be strict from the beginning.
- Allow common test constants and readable test data even if stricter magic-value rules are considered later.
- Prefer readable UI test code over clever compact code.

The exact Ruff configuration will be stored in `pyproject.toml`.

## Pre-Commit Plan

Pre-commit should be added after the initial `pyproject.toml` exists.

Planned behavior:

- Run Ruff linting before commits.
- Run Ruff formatting checks before commits.
- Restrict Ruff hooks to Python files such as `.py` and `.pyi`.
- Include `.ipynb` only if notebooks are intentionally added later.
- Do not claim Ruff checks shell scripts, because Ruff is a Python linter/formatter.
- If shell scripts are added, consider ShellCheck and shfmt as separate pre-commit hooks for `.sh` files.

The goal is to keep every code change checked before commit without slowing down documentation-only edits too much.

## Branching Plan

Implementation work should not happen directly on `main`.

Expected branch behavior:

- Check the current branch before implementation work.
- If the workspace is on `main`, create a feature branch first.
- Use branch names in the format `feature/<descriptive-name>`.
- Do not push unless the user explicitly asks for a push.

## Dependency Update Review

Before implementation work that touches dependencies or framework integrations, check the current package state.

Expected checks:

- Review current package versions through Poetry or official package sources.
- Check relevant release notes or documentation for Selenium, pytest, Allure, Ruff, pre-commit, YAML parser, and `python-dotenv` when those packages are being added or changed.
- Include important findings in the implementation plan before changing dependency files.

## Poetry Support

Planned Poetry setup:

- Create `pyproject.toml`.
- Target Python 3.12.
- Add runtime/test dependencies:
  - `selenium`
  - `pytest`
  - `allure-pytest`
  - YAML config parser
  - `python-dotenv`
- Add development dependencies:
  - `ruff`
  - `pre-commit`
  - optional typing tool, to be decided later
- Define useful commands in `README.md`.

## Git Ignore Requirements

The repository should ignore generated artifacts:

- `allure-results/`
- `allure-report/`
- logs
- screenshots
- temporary reports
- downloaded files under `data/downloads/`
- local env files

Intentional upload fixtures under `data/uploads/` should remain commit-ready.

## AI-Supported Development

This project should be prepared for a future code generation skill that can create:

- Page objects.
- Locator files.
- Test files.
- Flows.
- Fixtures.
- Allure annotations.
- Review checklists for generated tests.

Generation rules should be strict enough that Codex or another discovery/generation agent knows:

- Where tests are stored.
- Where page objects are stored.
- Where locators are stored.
- How fixtures are created.
- How config is loaded.
- How project paths are resolved.
- How test data is referenced.
- How page assertions are exposed.
- How Allure evidence is attached.

## Implementation Phases

### Phase 1: Planning and Rules

- Create and refine `plans/framework-plan.md`.
- Create and refine `AGENTS.md`.
- Add planned subfolder `AGENTS.md` files for focused agent context.
- Update `README.md` with setup and command guidance.
- Update `.gitignore` for UI test artifacts.
- Add `.env.example`.
- Add `pytest.ini` with initial markers.

### Phase 2: Project Bootstrap

- Create or switch to a `feature/<descriptive-name>` branch before implementation.
- Check relevant package versions and updates before adding dependencies.
- Initialize Poetry configuration.
- Set Python target to 3.12.
- Add Selenium, pytest, Allure, Ruff, YAML config, and `python-dotenv` dependencies.
- Add the direct framework source directories under `src/` and the `src/project.py` module.
- Add base folders for config, data, and tests.
- Add initial pytest and Ruff configuration.
- Configure Ruff to enforce return type annotations where practical.

### Phase 3: Framework Foundation

- Implement config dataclasses and loader.
- Implement constants model for timeouts.
- Implement `project.py` for repository-root-relative paths.
- Implement WebDriver factory.
- Implement Chrome-specific options.
- Implement `UIClient`.
- Implement `BasePage`.
- Implement separate locator modules.
- Implement wait-backed page assertion helpers.
- Implement configurable element visibility timeout and polling.
- Implement explicit screenshot steps, optional per-step screenshots, execution logging, page source, browser log, and Allure failure hooks.
- Implement generated artifact cleanup before each pytest session starts.

### Phase 4: First Application Smoke Test And Capability Verification

- Add the Sauce Demo home-page object and separate logo locator.
- Navigate to `https://sauce-demo.myshopify.com/` through `UIClient`.
- Verify the page is loaded when `img[alt='Sauce Demo']` is visible within 5 seconds, polling every second.
- Capture a screenshot through an explicit screenshot step after the loaded-state verification.
- Log each step in English with START, PASS, or FAIL status.
- Verify screenshot capability through the running browser test rather than unit or framework tests.
- Add broader application page objects, locators, flows, and test cases incrementally.

### Phase 5: CI/CD

- Add GitHub Actions workflow.
- Run tests headlessly in CI.
- Load secrets from GitHub Secrets.
- Upload Allure results as artifacts.
- Add pre-commit configuration for Ruff after the first code structure is in place.

### Phase 6: AI Generation Readiness

- Add templates or examples for pages, locators, tests, assertions, and flows.
- Add review checklist for generated tests.
- Prepare the future code generation skill.

## Still To Define

1. Exact YAML schema for `default.yaml` and environment overrides.
2. Exact pytest command-line options.
3. Download cleanup strategy.
4. Typing strategy beyond return annotations: lightweight typing, `mypy`, or `pyright`.
5. Selector strategy details.
6. Parallel execution strategy with `pytest-xdist`.
7. Flaky test handling strategy.
8. Broader application coverage after the initial Sauce Demo home-page smoke test.
9. Whether to add `.python-version` for local Python version pinning.
10. Whether shell scripts will be added and need ShellCheck/shfmt pre-commit hooks.
11. Which subfolders should receive dedicated `AGENTS.md` files first.

## Additional Improvements To Consider

- Add GitHub Actions matrix later if multiple browsers or environments are needed.
- Add `pytest-rerunfailures` only if wait and stability improvements are not enough.
- Add Pydantic later if dataclasses do not provide enough validation.
- Add templates for AI-generated page objects, locators, flows, and tests.
