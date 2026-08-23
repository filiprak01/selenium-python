# Repository Profile

This profile aligns the skill with the current Selenium Python repository.

Treat these paths as repository defaults, but verify that they still exist and read every applicable `AGENTS.md` before proposing changes.

## Existing framework map

```text
config/default.yaml                 # environment URLs and execution configuration
src/clients/                        # UI client and client pool
src/config/                         # configuration loading
src/models/                         # configuration models and constants
src/webdriver/                      # WebDriver factory and browser options
src/locators/                       # locator definitions
src/pages/                          # page objects
src/pages/components/               # reusable UI components
src/flows/                          # business workflows/actions
src/assertions/                     # UI assertion services
src/logging/                        # pytest/framework logging

tests/conftest.py                   # shared test fixtures
tests/ui/                           # default home for newly generated UI automation
tests/smoke/                        # existing smoke-organized tests
tests/regression/                   # existing regression-organized tests

screenshots/                        # screenshot artifacts
allure-results/                     # Allure result artifacts
allure-report/                      # generated Allure report
```

Do not introduce `tests/functionality/`, `tests/features/`, or `src/features/` while this profile applies.

## Generated and vendor paths

Do not use generated, cached, packaged, IDE, or virtual-environment content as source coverage evidence and do not modify it:

```text
.venv/
.idea/
.pytest_cache/
.ruff_cache/
**/__pycache__/
dist/
allure-report/
allure-results/
screenshots/
```

The screenshot and Allure paths may be used only through the repository's evidence/reporting behavior.

## New test placement

Place new automation at:

```text
tests/ui/<feature_package>/test_<workflow_module>.py
```

Examples:

```text
tests/ui/customer_profile/test_profile_update.py
tests/ui/checkout/test_checkout_validation.py
```

Use underscores for Python paths. Keep Markdown testcase paths in kebab-case.

Do not create one file or directory per testcase by default. Group cohesive cases by feature and business workflow.

Search `tests/ui/`, `tests/smoke/`, and `tests/regression/` before creating anything.

When equivalent automation exists in `tests/smoke/` or `tests/regression/`, update or map it in place unless the user accepts a separate migration plan. Do not move existing tests merely to normalize structure during one-case implementation.

The marker set, not the containing folder, determines whether a test belongs to UI, Smoke, Regression, E2E, or another selectable category. This avoids duplicating one test across several folders when it has several marks.

## Layer mapping

Use the current repository layers:

- business actions and scenario composition: `src/flows/`;
- UI assertions and assertion screenshots: `src/assertions/`;
- low-level page interactions: `src/pages/` and `src/pages/components/`;
- locator definitions: `src/locators/`;
- browser/client lifecycle: `src/clients/` and `src/webdriver/`;
- URL/environment/mode resolution: `config/default.yaml`, `src/config/`, and `src/models/`;
- shared fixtures: `tests/conftest.py`;
- feature-local fixtures, only when justified: `tests/ui/<feature_package>/conftest.py`;
- screenshots and Allure evidence: reuse `screenshots/`, `allure-results/`, and existing helpers.

Do not create a parallel abstraction when a current module can be safely extended.

Before editing a layer, read the root `AGENTS.md` and the nearest `AGENTS.md` files governing that path.

## Active pytest configuration

The repository root contains both `pytest.ini` and `pyproject.toml`. Treat root `pytest.ini` as the default active pytest configuration because it has precedence over `pyproject.toml`. Still inspect README, CI, and commands for an explicit `-c` override before editing configuration.

Do not register the same marker in both files.

## Repository marker policy

The default marker policy is stored in the skill at:

```text
.agents/skills/selenium-test-implementer/config/marker-policy.yaml
```

Every newly generated UI test receives all `required_for_all` marks from that file. In the current version these are:

```text
ui
regression
```

Derived marks are then added:

- `smoke` when the source testcase has `type: Smoke`;
- `e2e` when the source testcase has `scope: E2E`.

Merge additional registered marks from:

1. `additional_pytest_marks` in the accepted testcase;
2. explicit user instructions for the current implementation;
3. additional repository-wide mandatory marker rules in `AGENTS.md`;
4. compatible marks already present on equivalent automation.

Do not remove unrelated valid marks from an existing test without an accepted reason.

To add a future mark to every generated UI test, register it in the active pytest configuration and add it once under `required_for_all` in `.agents/skills/selenium-test-implementer/config/marker-policy.yaml`. Repository instructions may add stricter requirements and take precedence.
