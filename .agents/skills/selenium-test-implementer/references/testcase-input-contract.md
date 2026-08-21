# Testcase Input Contract

## One path per invocation

The primary input is one repository-relative Markdown path:

```text
docs/testcase/<feature-slug>/TC-###-<testcase-slug>.md
```

Use the exact file as the source of truth for test intent.

Do not consume every testcase in the feature directory.

## Required source content

The file should contain:

- accepted status;
- case ID;
- feature slug;
- Type;
- Scope;
- Case kind;
- Priority;
- title;
- behavior covered;
- preconditions;
- ordered steps;
- explicit test data or semantic aliases;
- observable expected UI results;
- optional testcase-specific additional pytest marks;
- automation handoff metadata.

Expected frontmatter:

```yaml
---
id: TC-001
feature: customer-profile
type: Smoke
scope: Feature
case_kind: Happy path
priority: Critical
status: accepted
additional_pytest_marks: []
automation_status: not_implemented
automation_test: null
automation_marks: []
automation_last_verified: null
automation_environment: null
automation_notes: null
---
```

Field values are case-insensitive during parsing, but preserve the repository's canonical format when writing.

## Additional pytest marks

`additional_pytest_marks` contains only case-specific marks beyond automatically resolved repository and classification marks.

Example:

```yaml
additional_pytest_marks:
  - localization
  - accessibility
```

Do not require baseline values such as `ui`, `regression`, `smoke`, or `e2e` in this list. The implementer resolves them from the skill-local `config/marker-policy.yaml` and the testcase classification.

An older case without the field is equivalent to:

```yaml
additional_pytest_marks: []
```

Do not accept invalid YAML values, spaces in marker names, arbitrary pytest marker expressions, or unregistered markers without an accepted registration plan.

## Resolved automation marks

`automation_marks` stores the exact deduplicated marks applied to the mapped automated test.

Before automation exists, use:

```yaml
automation_marks: []
```

After implementation, a Smoke E2E case with an additional localization mark may contain:

```yaml
automation_marks:
  - ui
  - regression
  - smoke
  - e2e
  - localization
```

Do not treat this field as an input override. Recompute and verify it against:

1. the skill-local `config/marker-policy.yaml`;
2. the source testcase Type and Scope;
3. `additional_pytest_marks`;
4. explicitly accepted prompt additions;
5. compatible marks preserved on existing automation;
6. active pytest marker registration.

Update `automation_marks` when the mapped automation or marker policy changes.

## Accepted-case check

Proceed when:

- `status: accepted`; or
- the file exists in the accepted testcase directory and follows an older template without an explicit status, with no evidence that it is a draft.

Stop when the file explicitly states draft, proposed, rejected, deprecated, or unaccepted status.

## Automation state handling

Allowed values:

```text
not_implemented
pending_verification
implemented
blocked
update_required
```

Behavior:

- `not_implemented`: normal implementation flow;
- `pending_verification`: inspect current working-tree implementation and continue from verification or repair;
- `implemented`: validate the mapping before deciding whether work is already complete or stale;
- `blocked`: inspect the recorded blocker and do not ignore it;
- `update_required`: inspect mapped automation and plan an update.

Do not trust `automation_test` or `automation_marks` blindly. Confirm that the referenced node exists, materially implements the case, and contains the resolved marks.

Use `automation_notes` for an accepted blocker, a concise update reason, or another automation-specific limitation. Keep it `null` when no note is needed. Never store secrets or verbose run logs there.

## Case ID and traceability

Use the case ID in the test function name when creating a new test:

```text
test_tc_001_successfully_update_profile
```

Record the final pytest node ID in `automation_test`, for example:

```text
tests/ui/customer_profile/test_profile_update.py::test_tc_001_successfully_update_profile
```

For class-based pytest automation, include the class segment:

```text
tests/ui/customer_profile/test_profile_update.py::TestProfileUpdate::test_tc_001_successfully_update_profile
```

For parameterized automation, include a stable parameter ID and record the full selectable node when practical:

```text
tests/ui/customer_profile/test_profile_validation.py::test_profile_validation[TC-004-empty-last-name]
```

When mapping an existing test under `tests/smoke/` or `tests/regression/`, preserve its real node ID rather than moving it to match the new-test default.

## Semantic aliases and secrets

Values such as these are references, not literal data:

```text
<ACTIVE_TEST_USER>
<VALID_CUSTOMER_EMAIL>
<EXISTING_PRODUCT>
```

Resolve them through existing fixtures, test-data providers, configuration, or user-supplied safe data.

Never replace semantic aliases with secrets in the Markdown file or code.

## Source changes

Any behavioral change to preconditions, steps, data meaning, or expected result requires the validation-change review flow.

Pure metadata normalization may be included in the implementation plan, including:

- adding missing automation fields;
- adding `additional_pytest_marks: []` to an older case;
- adding `automation_marks: []` to an older case;
- normalizing casing;
- adding a stable automation node mapping;
- updating resolved marks and automation state after verification.
