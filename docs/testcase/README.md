# UI Test Cases

Accepted UI test cases are stored by feature:

```text
docs/testcase/<feature-slug>/
```

Each feature directory contains:

```text
README.md
TC-001-<test-case-slug>.md
TC-002-<test-case-slug>.md
...
```

## Classification

- `Type`: `Smoke` or `Regression`
- `Scope`: `Feature` or `E2E`
- `Case kind`: `Happy path`, `Negative`, `Validation`, `Boundary`, or `State and recovery`
- `Priority`: `Critical`, `High`, `Medium`, or `Low`

Edge cases normally belong to `Type: Regression`.

## Additional pytest marks

A case may define testcase-specific automation marks:

```yaml
additional_pytest_marks:
  - localization
  - accessibility
```

This list stores additions only. The implementer derives repository-required and classification marks from:

```text
.agents/skills/selenium-test-implementer/config/marker-policy.yaml
```

With the current policy it applies:

- `ui` and `regression` to every generated UI test;
- `smoke` to a Smoke case;
- `e2e` to an E2E case;
- any other policy-wide, testcase-specific, explicitly accepted, or compatible existing marks.

Older cases without `additional_pytest_marks` are treated as having an empty list.

## Automation handoff

Each accepted case records:

```yaml
additional_pytest_marks: []
automation_status: not_implemented
automation_test: null
automation_marks: []
automation_last_verified: null
automation_environment: null
automation_notes: null
```

Allowed automation states:

```text
not_implemented
pending_verification
implemented
blocked
update_required
```

`automation_test` stores the final pytest node ID.

`automation_marks` stores the exact deduplicated marks applied to that automated node. It is not an override and must be recalculated when the marker policy or implementation changes.

## Skills

Design cases one at a time:

```text
$ui-testcase-designer
```

Implement one accepted case:

```text
$selenium-test-implementer

Test case:
docs/testcase/<feature-slug>/TC-###-<testcase-slug>.md
```

Only explicitly accepted cases may be saved here. Automation must not silently change accepted test intent.
