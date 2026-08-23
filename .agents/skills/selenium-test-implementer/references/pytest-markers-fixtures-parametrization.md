# Pytest Markers, Fixtures, and Parametrization

## Marker policy source

Read:

```text
config/marker-policy.yaml
```

relative to the skill directory before calculating marks.

Marks are cumulative. A test can and often should have several marks.

Do not hardcode a fixed maximum number of marks.

## Marker resolution

Resolve the final set in this order:

1. all values in policy `required_for_all`;
2. values derived from the testcase `type`;
3. values derived from the testcase `scope`;
4. testcase frontmatter `additional_pytest_marks`;
5. explicit user additions accepted for this implementation;
6. compatible marks preserved from materially equivalent existing automation.

Deduplicate while preserving policy `preferred_order`. Append valid marks not listed in `preferred_order` in their resolved order.

With the current policy:

| Source testcase | Resolved baseline marks |
|---|---|
| Type `Smoke`, Scope `Feature` | `ui`, `regression`, `smoke` |
| Type `Smoke`, Scope `E2E` | `ui`, `regression`, `smoke`, `e2e` |
| Type `Regression`, Scope `Feature` | `ui`, `regression` |
| Type `Regression`, Scope `E2E` | `ui`, `regression`, `e2e` |

Example accepted case metadata:

```yaml
additional_pytest_marks:
  - localization
  - accessibility
```

Effective marks for a Smoke E2E case would be:

```text
ui, regression, smoke, e2e, localization, accessibility
```

Do not repeat baseline or derived values in `additional_pytest_marks`. Normalize duplicates if an older file contains them.

Do not invent marks from feature names or assumptions.

Do not remove unrelated compatible marks from an existing test without an accepted reason.

Write the exact final set to the testcase `automation_marks` field when implementation begins and verify it again before final acceptance.

## Adding a future mark to all generated tests

To require another mark globally:

1. add it to `required_for_all` in `config/marker-policy.yaml`;
2. add a suggested description under policy `descriptions` when useful;
3. verify whether it is already registered in the active pytest configuration;
4. include missing registration in the implementation plan;
5. apply it to every newly generated test and to an existing mapped test only when that test is being updated under an accepted plan.

Do not edit every testcase to add a repository-wide mark.

## Marker placement

Default to function-level marks for explicit one-case traceability:

```python
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.smoke
def test_tc_001_example(...):
    ...
```

Module- or class-level marks may be reused when every test in that scope intentionally shares them.

Testcase-specific marks must remain on the function, method, or parameter row.

For parameter-specific marks, use `pytest.param(..., marks=...)` when only certain rows require the mark.

Use one pytest mark decorator per mark unless established repository style uses a `pytestmark` list.

## Marker registration

The repository contains both root `pytest.ini` and `pyproject.toml`. Use `pytest.ini` as the default active pytest configuration because it has precedence, while still checking README, CI, and commands for an explicit `-c` override. Do not duplicate marker registration across both files.

When markers are missing, register them in the active existing configuration.

Example for `pytest.ini`:

```ini
[pytest]
addopts = --strict-markers
markers =
    ui: Selenium browser user-interface automation
    regression: Maintained regression coverage
    smoke: Critical confidence subset of regression coverage
    e2e: End-to-end workflow crossing meaningful functional boundaries
```

Example for `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--strict-markers"
markers = [
  "ui: Selenium browser user-interface automation",
  "regression: Maintained regression coverage",
  "smoke: Critical confidence subset of regression coverage",
  "e2e: End-to-end workflow crossing meaningful functional boundaries",
]
```

Preserve all existing options and marker descriptions.

Do not add a mark to code before it is registered when strict marker validation applies. Include registration in the implementation plan and wait for acceptance.

## Fixtures

Use fixtures for explicit, reusable, and lifecycle-aware setup such as:

- browser/session provision;
- authenticated user state;
- flow and assertion object wiring;
- test data creation;
- environment configuration;
- cleanup/finalization;
- report/evidence services.

Use the narrowest useful scope:

- function scope for mutable test state and browser isolation unless the existing framework safely manages another scope;
- module or session scope only for immutable or deliberately shared expensive resources;
- feature-local `tests/ui/<feature_package>/conftest.py` for fixtures that do not belong globally.

Do not create a fixture solely to rename a one-line local constant.

## Parametrization

Use `@pytest.mark.parametrize` when:

- the business workflow is identical;
- only input values and corresponding expected values vary;
- fixture/lifecycle requirements are compatible;
- the effective mark set is compatible, or row-specific marks can be applied clearly;
- the combined test remains readable and failures remain attributable.

Do not parameterize together:

- different business outcomes;
- different navigation paths;
- different cleanup strategies;
- Smoke and non-Smoke cases when that would blur selection;
- Feature and E2E cases when their scopes differ;
- cases requiring materially different assertions or user roles.

Prefer stable IDs:

```python
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    ("phone_number", "expected_message"),
    [
        pytest.param("123", "Invalid phone number", id="TC-014-too-short"),
        pytest.param("ABC", "Invalid phone number", id="TC-015-non-numeric"),
    ],
)
def test_profile_phone_validation(...):
    ...
```

When implementing one new case into an existing parameterized test, add the smallest compatible parameter row rather than creating a duplicate function.

Do not mutate dictionaries or lists passed as parameters unless each invocation receives an isolated copy.

## Test data

Use semantic fixtures, builders, or factories rather than secrets and hardcoded environment-specific records.

Prefer unique generated data for create/update flows.

Ensure cleanup is deterministic and safe even when the assertion fails.

## User-run commands

Discover the repository's actual runner from `pyproject.toml`, `pytest.ini`, README, CI, and AGENTS instructions.

Provide the narrowest command first.

Generic fallback only when no repository runner exists:

```text
pytest <test-node-id>
```

Useful selection examples when compatible with repository configuration:

```text
pytest tests/ui/<feature_package> -m ui
pytest tests/ui -m "ui and smoke"
pytest tests/ui -m "ui and regression"
pytest tests/ui -m "ui and regression and e2e"
```

The user runs commands and returns output when repository rules prohibit Codex from doing so.

When implementing the final not-yet-automated accepted case for a feature, request a feature-level run after the targeted node. Request the complete UI regression run when repository policy defines it as the acceptance gate. Distinguish unrelated pre-existing suite failures from failures caused by the new implementation.
