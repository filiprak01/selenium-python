# Repository and UI Discovery

Use this procedure before proposing the first test case.

## 1. Read repository instructions

Locate and obey all applicable:

```text
AGENTS.md
AGENTS.override.md
```

Start at the repository root and read more specific instructions governing each path that may be inspected or changed.

For this repository, scoped `AGENTS.md` files may exist under configuration, source-layer, test, data, and workflow directories. Repository instructions override this reference when they are more restrictive.

## 2. Identify the current repository structure

Prioritize these established paths when present:

```text
config/default.yaml
src/clients/
src/config/
src/models/
src/webdriver/
src/locators/
src/pages/
src/pages/components/
src/flows/
src/assertions/
src/logging/
tests/conftest.py
tests/ui/
tests/smoke/
tests/regression/
.github/workflows/ui-tests.yml
pytest.ini
pyproject.toml
```

Determine:

- repository root;
- application and framework conventions;
- manual testcase location;
- UI automation locations;
- configured URLs and environment aliases;
- browser modes and driver/client entry points;
- authentication and session bootstrap;
- fixture, page, locator, flow, assertion, and screenshot conventions;
- active pytest configuration and marker selection in CI;
- application start instructions and available browser/MCP tools.

Do not add a dependency or create a new client merely to perform discovery.

## 3. Exclude generated and dependency content

Do not use these as sources for duplicate or framework discovery except when explicitly inspecting artifacts:

```text
.venv/
.pytest_cache/
.ruff_cache/
**/__pycache__/
dist/
allure-report/
allure-results/
logs/
screenshots/
```

Installed packages, bytecode, cache node IDs, screenshots, and generated reports are not repository-owned test implementations.

## 4. Search manual test cases

Search this location first:

```text
docs/testcase/
```

Also inspect an existing legacy location such as `docs/testcases/` when the repository already uses it, but save newly accepted cases only to the configured canonical location.

Search by:

- feature name and synonyms;
- page or route;
- visible labels;
- component names;
- business action;
- validation message;
- related user journey;
- test data class;
- expected result.

Inspect file contents, not only filenames.

## 5. Search existing UI automation

Inspect all current test locations:

```text
tests/ui/
tests/smoke/
tests/regression/
```

Use existing automation only as coverage evidence during testcase design. Do not edit it in this skill.

Also inspect supporting code when needed:

```text
src/locators/
src/pages/
src/pages/components/
src/flows/
src/assertions/
tests/conftest.py
```

Check:

- business behavior, not only names;
- pytest marks and parameter rows;
- page and component ownership;
- reusable flows;
- assertion behavior;
- data/fixture requirements;
- CI selections.

Documented coverage and automated coverage are different facts. A scenario may be:

- documented but not automated;
- automated but not documented;
- both;
- neither.

## 6. Inspect implementation evidence

When useful, inspect:

- configured routes and URLs;
- visible UI component behavior;
- form definitions and validators;
- visible error messages;
- feature flags and permissions;
- state-management behavior;
- API contracts only to understand observable UI behavior;
- locator/page/flow/assertion code only to find the correct UI path and existing coverage.

Do not turn selectors or implementation details into manual test steps.

## 7. Explore the running UI safely

Reuse the configured UI client, environment resolution, WebDriver setup, and browser capability. Follow `browser-configuration-reuse.md`.

Prefer a safe environment:

```text
local
development
test
staging
```

Prefer configured headless mode when available.

Never create a temporary Selenium, shell, JavaScript, or Python script solely for exploration.

Do not:

- delete data;
- submit payments;
- send real messages;
- change real account settings;
- create irreversible records;
- accept legal terms;
- expose credentials;
- bypass authentication controls.

Safe observations may include:

- opening pages;
- inspecting visible content;
- focusing controls;
- opening non-destructive menus;
- entering disposable values without committing an unsafe action;
- triggering client-side validation;
- observing enabled and disabled states;
- navigating back and forward;
- checking modal and notification behavior.

Use semantic credential aliases. Never copy secrets into test-case files.

## 8. Record the verification basis

Each proposal must state one of:

```text
Live UI + repository
Repository only
Prompt + repository
Prompt only
```

When UI exploration failed or was unavailable, state the reason briefly and do not claim verification.

## 9. Detect duplicates and changes

Compare a candidate with existing cases using:

- user intent;
- starting state;
- actions;
- test data class;
- expected UI outcome;
- covered business risk.

Classify the relationship:

### NEW

No materially equivalent case exists.

### EXISTING

An equivalent case already covers the scenario. Do not propose another case.

### OVERLAPPING

An existing case covers part of the scenario. Propose an update or extension to that file.

### OUTDATED

An existing case conflicts with current verified behavior. Propose an update to that file.

A changed title, directory, pytest mark, or sample value does not make a behaviorally equivalent case new.
