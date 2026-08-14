# Codex Development Rules

## Project Purpose

This repository contains a Python Selenium UI testing framework using pytest, Allure, Poetry, GitHub Actions, YAML configuration, and the Page Object Model.

Codex should treat this project as a test automation framework.

## Core Rules

- Use Python and follow the planned `src/` source layout.
- Target Python 3.12 unless the project plan changes.
- Use Poetry for dependency management.
- Use pytest for test execution and fixtures.
- Use Selenium for browser automation.
- Use Chrome as the first supported browser until the project plan changes.
- Use Allure for reporting and evidence attachments.
- Use Ruff for formatting and linting.
- Keep tests in `tests/`.
- Keep framework source directly under `src/`.
- Keep framework assertions in `src/assertions/`.
- Keep clients in `src/clients/`.
- Keep config loading code in `src/config/`.
- Keep business behavior helpers in `src/flows/`.
- Keep locators in `src/locators/`.
- Keep framework logging in `src/logging/`.
- Keep config models and timeout constants in `src/models/`.
- Keep page objects in `src/pages/`.
- Keep WebDriver infrastructure in `src/webdriver/`.
- Keep project-root-relative path definitions in `src/project.py`.
- Keep configuration files in `config/`.
- Keep upload, download, and fixture files in `data/`.

## Git Rules

- Do not work directly on `main`.
- Before implementation work, create or switch to a feature branch named `feature/<descriptive-name>`.
- Do not push changes after code implementation unless the user explicitly asks for a push.
- Keep unrelated user changes intact and do not revert them.

## Planning Rules

- Before implementing code changes, create or update a short plan and ask the user to approve it.
- The plan should explain what will change, where it will change, and why.
- The plan should include scalability concerns detected during review and a proposed implementation path for the user to consider.
- Do not implement until the user approves the plan.
- Documentation-only planning changes can be made when the user explicitly asks to update planning documents.

## Delivery Rules

- After implementation, summarize changed files and what changed in each file.
- Provide a diff-view-oriented summary so the user can review the changes clearly.
- Mention verification commands that were run and whether they passed.

## Dependency Rules

- Before implementation work that touches dependencies or framework integration, check for current package versions and relevant updates.
- Prefer official package documentation, release notes, or Poetry package metadata when checking dependency updates.
- Include notable package/version findings in the implementation plan before making dependency changes.

## Scalability Rules

- Prefer scalable framework structure over the simplest short-term implementation.
- Keep extension points clear for future browsers, environments, clients, flows, and generated tests.
- When a scalability issue is detected, document the concern and propose an implementation plan for user consideration.
- Avoid abstractions that do not serve an expected framework extension point.

## Typing Rules

- Always add explicit return types to functions and methods.
- Use `-> None` for functions and methods that do not return a value.
- Keep type annotations readable and useful for framework users and future generated code.

## Page Object Model Rules

- Tests should avoid direct Selenium calls.
- Page objects should expose user-level actions and page-specific behavior.
- Page objects should use locators from the separate locator package.
- Page objects should use explicit waits where needed.
- Page objects may expose indirect assertion helpers backed by assertion functions.
- Prefer stable selectors such as `data-testid` when available.
- Keep reusable components separate from full-page objects when the same component appears on multiple pages.

## Flow Rules

- Use `flows/` for reusable business behavior and UI manipulation.
- Flows may coordinate multiple pages.
- Flows should keep tests readable and behavior-oriented.
- Do not hide page-specific behavior in flows when it belongs in a page object.

## Client Rules

- `UIClient` is the high-level entry point for UI tests.
- `UIClient` should own or receive WebDriver/session details.
- `UIClient` should expose access to page objects and flows.
- Keep test files away from WebDriver construction details.
- Prepare for a future client pool when multiple clients, users, browsers, or sessions are needed.

## Test Rules

- Test names should describe behavior.
- Tests should be small enough to diagnose failures quickly.
- Use pytest fixtures for browser, config, clients, and reusable setup.
- Use pytest markers for meaningful grouping.
- Register pytest markers in `pytest.ini`.
- Keep `smoke` and `regression` markers available from the beginning.
- Validate framework capabilities through browser tests against the configured test URL.
- Start with the Sauce Demo home-page smoke test; add broader application test cases incrementally.
- Add Allure labels and steps for important user flows.
- Capture screenshots, page source, and useful browser evidence on failure.
- Capture a screenshot after every named Allure UI step and persist it under the configured screenshot path.
- Log every UI step in English with START, PASS, and FAIL states; attach execution logs to failed Allure results.
- Local tests should run headed by default.
- CI tests should run headless by default.

## Configuration Rules

- Do not hardcode application URLs, credentials, browser choices, paths, or timeouts in tests.
- Store URLs and non-secret configuration in YAML files under `config/`.
- Load configuration into dataclass models.
- Use `python-dotenv` for local `.env` loading.
- Store timeout constants in source models/constants.
- Use `pathlib.Path` and project-root-relative paths from `project.py`.
- Include OS-aware path behavior through configuration where needed.
- Keep secrets out of Git.
- Load local secrets from environment variables.
- Load CI/CD secrets from GitHub Secrets.

## Ruff Rules

- Keep Ruff enabled for formatting and linting.
- Run Ruff after any Python code change.
- Run Ruff for the Python files changed in the implementation.
- Fix Ruff issues detected in changed files before reporting completion.
- Configure Ruff to enforce missing return type annotations through the `ANN` rule family where practical.
- Use pre-commit to run Ruff before commits once pre-commit is configured.
- Run Ruff on Python files such as `.py` and `.pyi`.
- Include `.ipynb` only if notebooks become part of the framework.
- Do not use Ruff for shell scripts. If `.sh` scripts are added, use ShellCheck or shfmt through pre-commit.
- Keep pytest `assert` statements allowed.
- Prefer readable UI automation code over compact clever code.
- Avoid hard sleeps; prefer explicit waits.
- Avoid broad utility dumping. Add clear modules for new framework behavior.

## Generated Code Rules

- Generated code should match the repository structure and naming conventions.
- Generated tests should use `UIClient`, page objects, flows, and assertion helpers.
- Generated tests should not use raw Selenium directly unless framework code is being created.
- Generated locators should be reviewed for selector stability.
- Generated files should include only useful comments.
- Generated code should be runnable with Poetry, pytest, Ruff, and Allure.

## CI/CD Rules

- Use GitHub Actions for CI/CD.
- Run CI browser tests in headless mode.
- Use GitHub Secrets for sensitive values.
- Upload Allure result artifacts where practical.
- Do not add Selenium Grid or remote WebDriver support in the initial implementation.

## Review Checklist

- Does the test describe behavior instead of implementation details?
- Are locators stable and easy to maintain?
- Is Selenium usage hidden inside page objects, clients, flows, or framework utilities?
- Are configuration values loaded from config instead of hardcoded?
- Are paths resolved from project-root-relative helpers?
- Are secrets loaded from environment variables or GitHub Secrets?
- Is failure evidence available in Allure?
- Can the test be run through Poetry and pytest?
- Does Ruff pass?
