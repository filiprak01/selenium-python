# Selenium Implementation Plan — <TC-###>

**Source testcase:** `<relative path>`

**Validated environment:** <environment alias>

**Automation relationship:** <ALREADY_IMPLEMENTED | PARTIALLY_IMPLEMENTED | UPDATE_REQUIRED | NEW_AUTOMATION>

**Target pytest node:** `<planned node ID>`

**Marker policy:** `.agents/skills/selenium-test-implementer/config/marker-policy.yaml` (version <value>)

**Active pytest configuration:** `<pytest.ini | pyproject.toml | other discovered path>`

## Effective pytest marks

| Source | Marks |
|---|---|
| Policy `required_for_all` | <for example `ui`, `regression`> |
| Type-derived | <for example `smoke` or None> |
| Scope-derived | <for example `e2e` or None> |
| Testcase-specific | <values from `additional_pytest_marks` or None> |
| Prompt-supplied | <values or None> |
| Preserved existing | <compatible existing values or None> |
| **Final deduplicated set** | `<complete ordered mark list>` |

**Registration status:** <All registered | Missing marks and exact active-config change>

**Testcase `automation_marks` after implementation:** `<complete ordered mark list>`

## Planned file changes

| Action | File | Purpose |
|---|---|---|
| <Create / Update / Reuse> | `<relative path>` | <concise reason> |

## Layer mapping

- **Test module:** <business-only test function or existing parameter row under tests/ui, tests/smoke, or tests/regression>
- **Flow layer (`src/flows`):** <existing/new methods>
- **Assertion layer (`src/assertions`):** <existing/new methods and expected UI checks>
- **Page/component layer (`src/pages`):** <existing/new low-level interactions and state queries>
- **Locator layer (`src/locators`):** <existing/new selector constants or classes>
- **Fixtures/conftest:** <reuse tests/conftest.py or minimal local additions>
- **Client/config/webdriver:** <reused paths; normally no changes>
- **Test data:** <fixture/factory/semantic aliases>
- **Cleanup:** <how state remains independent>

## Locator plan

| Element/state | Locator owner | Existing/new locator | Stability evidence |
|---|---|---|---|
| <element> | <src/locators module> | <reuse or new strategy without exposing secrets> | <unique and verified state> |

## Parametrization

<Not applicable, add compatible row to an existing parametrized test, or create parametrization with rationale, stable row IDs, and row-specific marks when needed.>

## Assertion evidence

| Business assertion | Screenshot evidence | Existing helper/path |
|---|---|---|
| <assertion> | <element or viewport screenshot name> | <helper and artifact behavior> |

## Framework/config changes

<None, or the exact marker registration, evidence, fixture, or reusable framework update required. Separate required changes from optional recommendations.>

## User-run verification

- Targeted command: `<discovered command>`
- Feature command: `<command or N/A>`
- UI smoke command: `<command or N/A>`
- Full UI regression command: `<command or N/A>`
- Current case completes all accepted cases for feature: <Yes or No>
- Required completion run: <Targeted only | Targeted + feature | Targeted + feature + UI smoke | Targeted + feature + full UI regression>

## Decision

[ACCEPT PLAN] — implement the exact plan

[DISCUSS: <comment>] — change architecture, files, marks, data, locators, or scope

[CANCEL] — stop without implementing
