---
name: selenium-test-implementer
description: Implement one accepted Markdown UI test case as Selenium pytest automation. Use when the user supplies an exact path under docs/testcase/.../TC-*.md and wants repository-aware duplicate detection, live UI replay, testcase discrepancy review, locator discovery, a user-approved implementation plan, cumulative ui/regression/smoke/e2e and additional pytest marks, business-level flow methods, separate assertion modules, screenshot evidence for UI assertions, and case-to-code traceability. Do not design batches of new cases or silently rewrite accepted behavior.
---

# Selenium Test Implementer

## Goal

Take exactly one accepted UI testcase Markdown file and implement or update its Selenium automation using the repository's existing pytest framework.

Validation comes before implementation.

The workflow must:

1. receive one testcase path;
2. parse and validate the accepted testcase;
3. inspect repository instructions, the repository profile, and framework conventions;
4. search for materially equivalent existing automation;
5. discover and reuse the existing browser client, URL configuration, modes, fixtures, pages, locators, flows, assertions, and screenshot support;
6. replay the manual scenario in the safe running UI;
7. report missing, incorrect, ambiguous, or impossible steps before writing automation;
8. distinguish testcase defects from product defects and environment blockers;
9. propose exact testcase changes when appropriate and wait for user acceptance;
10. replay the revised case after accepted changes;
11. discover and verify stable locators;
12. calculate the complete cumulative pytest marker set;
13. present an implementation plan and wait for user acceptance;
14. implement or update the test using the current repository architecture;
15. ask the user to run the discovered pytest command;
16. analyze the user's result and iterate when necessary;
17. update testcase automation metadata only after the implementation state is known.

This skill implements one case per invocation. It does not generate new coverage queues.

## Required input

The prompt must identify one testcase file, for example:

```text
Test case:
docs/testcase/customer-profile/TC-001-successfully-update-profile.md
```

The path is the primary parameter.

Optional input may add testcase-specific registered markers:

```text
Additional marks:
- accessibility
- localization
```

Prompt-supplied marks are additions. They never replace required repository marks or source-derived marks.

Do not accept a feature directory as a substitute for a testcase file unless the user explicitly asks for a future batch workflow. Do not batch-implement all files in a directory as part of this skill.

## Required supporting files

Before making changes, read:

- `config/marker-policy.yaml`
- `references/repository-profile.md`
- `references/testcase-input-contract.md`
- `references/repository-and-coverage-discovery.md`
- `references/ui-replay-and-locator-discovery.md`
- `references/automation-architecture.md`
- `references/pytest-markers-fixtures-parametrization.md`
- `references/ui-assertion-evidence.md`
- `references/review-protocol.md`
- `assets/validation-report-template.md`
- `assets/testcase-change-proposal-template.md`
- `assets/implementation-plan-template.md`
- `assets/implementation-review-template.md`

Resolve these paths relative to this skill directory.

## Non-negotiable rules

- Respect every applicable `AGENTS.md` and `AGENTS.override.md`.
- Never work directly on `main` when repository instructions forbid it.
- Never commit without the permission required by repository instructions.
- Never push repository changes.
- Work on exactly one source testcase per invocation.
- Do not write automation until the scenario is validated or the user explicitly accepts a documented limitation.
- Do not silently modify the source testcase.
- Do not change a correct testcase merely to match a product defect.
- Do not invent missing requirements.
- Reuse the existing browser client, URLs, environments, modes, authentication, and session bootstrap.
- Do not create a second browser client or duplicate URL configuration.
- Do not create temporary Selenium, shell, Python, or JavaScript discovery scripts.
- Do not install dependencies without explicit user approval.
- Never expose or persist passwords, tokens, session cookies, or secrets.
- Never perform destructive or irreversible production actions.
- Do not execute pytest, shell, Python, or repository scripts when repository instructions require the user to run them.
- Ask the user to run the exact discovered command and provide the output.
- Do not duplicate an existing automated scenario.
- Do not put raw locators, `WebDriver` calls, waits, screenshots, or direct assertions in test functions.
- Store locators in `src/locators/` and expose them through existing page/component objects.
- Put business actions and workflow composition in `src/flows/`.
- Put UI assertions in `src/assertions/`.
- Every logical UI assertion must create screenshot evidence according to `references/ui-assertion-evidence.md`.
- Every new UI test must receive every `required_for_all` mark from `config/marker-policy.yaml`; the current policy includes `ui` and `regression`.
- Validate every additional mark against active pytest marker registration before using it.
- Do not silently remove compatible existing marks when updating automation.
- Do not introduce broad framework refactors unrelated to the source case.
- Do not mark automation as `implemented` before the user-run test passes and the user accepts the result.

## Source-case state

The source file must represent an accepted case.

Expected frontmatter includes:

```yaml
status: accepted
automation_status: not_implemented
additional_pytest_marks: []
automation_marks: []
```

`additional_pytest_marks` and `automation_marks` are optional for older accepted cases. Missing them means no testcase-specific additions and no recorded resolved automation marks.

Older accepted files without automation fields may be upgraded as part of an accepted implementation plan. Missing automation metadata alone is not a reason to reject the case.

Allowed automation states:

```text
not_implemented
pending_verification
implemented
blocked
update_required
```

## Automation classification and marker merge

Pytest marks are cumulative, not mutually exclusive.

Read `config/marker-policy.yaml` and resolve marks from:

1. every value in `required_for_all`;
2. Type-derived marks;
3. Scope-derived marks;
4. each valid value from `additional_pytest_marks`;
5. each explicitly requested valid mark accepted for this implementation;
6. compatible marks already present on equivalent automation.

With the current policy:

```text
Smoke + Feature      -> ui, regression, smoke
Smoke + E2E          -> ui, regression, smoke, e2e
Regression + Feature -> ui, regression
Regression + E2E     -> ui, regression, e2e
```

A case may contain more marks, for example:

```text
ui, regression, e2e, localization, critical_path
```

There is no fixed maximum. Normalize duplicates, follow policy `preferred_order`, preserve repository naming, and do not invent marker semantics.

Before implementation:

1. inspect the active pytest configuration;
2. verify that every effective marker is registered when strict markers are used;
3. include missing marker registration in the implementation plan;
4. wait for plan acceptance before editing pytest configuration;
5. record the exact final set in testcase frontmatter `automation_marks`.

Place case-specific marks on the test function or parameter row. Module/class-level marks may be reused only when every contained test intentionally shares them.

If more restrictive repository instructions define additional mandatory marks, report the merge in the implementation plan and follow the accepted repository rule. To change the generator default for all future tests, update `required_for_all` in `config/marker-policy.yaml` rather than editing every testcase.

## Target test structure

For this repository, create new automation under:

```text
tests/ui/<feature_package>/test_<workflow_module>.py
```

Derive `<feature_package>` from the Markdown feature slug by replacing hyphens with underscores. Example: `customer-profile` becomes `customer_profile`.

Create one test function or pytest test method per manual testcase:

```text
test_tc_001_<testcase-slug>
```

Follow an established pytest class convention when the repository already uses one. Do not introduce a class solely to wrap one test.

Do not create a directory or file for every testcase by default.

Group cases in the same test module when they belong to the same cohesive business workflow and use compatible setup. Split modules when workflows, actors, states, or lifecycle requirements are materially different.

Search existing automation in:

```text
tests/ui/
tests/smoke/
tests/regression/
```

If equivalent automation already exists outside `tests/ui/`, update or map it in place unless the user accepts a migration. Do not duplicate or move it merely to normalize directories.

Use the current repository layers described in `references/repository-profile.md`. Do not create `tests/functionality/` or `src/features/` while this profile applies.

## Workflow

### Phase 1 — Parse the source testcase

Follow `references/testcase-input-contract.md`.

Extract:

- source path;
- case ID;
- feature slug;
- title;
- type;
- scope;
- case kind;
- priority;
- preconditions;
- steps;
- test data;
- expected UI results;
- testcase-specific additional pytest marks;
- prompt-supplied additional marks;
- current automation state, mapping, and recorded `automation_marks`.

Stop with a concise input error only when the file does not exist, is not a testcase file, is explicitly unaccepted, or cannot be parsed safely.

### Phase 2 — Discover framework and existing coverage

Follow `references/repository-and-coverage-discovery.md`.

Determine whether the source case is:

- `ALREADY_IMPLEMENTED`
- `PARTIALLY_IMPLEMENTED`
- `UPDATE_REQUIRED`
- `NEW_AUTOMATION`
- `CONFLICTING_AUTOMATION`

Search semantically, not only by filename or case ID.

If equivalent automation already exists, do not create a duplicate. Validate it against the source case and propose mapping or an update.

### Phase 3 — Replay and validate the manual scenario

Follow `references/ui-replay-and-locator-discovery.md`.

Use the existing configured browser capability and safe environment.

Replay every precondition and step in order. For each step compare:

- stated precondition;
- stated action;
- expected UI result;
- observed UI state;
- prerequisite actions actually required;
- candidate locator availability and stability.

Classify discrepancies as:

- `MANUAL_CASE_ISSUE`
- `PRODUCT_DEFECT`
- `ENVIRONMENT_BLOCKER`
- `AUTOMATION_BLOCKER`
- `AMBIGUITY`

Examples of `MANUAL_CASE_ISSUE` include:

- a required navigation step is missing;
- a button becomes visible only after data is entered but the case omits that state transition;
- an expected message, label, or destination is incorrect;
- the test data cannot satisfy the stated preconditions;
- the action order is impossible in the actual UI.

A missing control is not automatically a testcase issue. Determine whether the accepted requirement says it should exist. When the UI appears broken, classify it as a potential product defect and do not rewrite the expected result merely to make automation pass.

### Phase 4 — Resolve validation issues

When any material issue exists, render `assets/validation-report-template.md` and, when a testcase change is appropriate, include `assets/testcase-change-proposal-template.md`.

Show the complete set of material issues for this one source case. Then stop.

Allowed decisions are defined in `references/review-protocol.md`.

On accepted testcase changes:

1. update the source testcase and its feature `README.md` where needed;
2. preserve the case ID;
3. keep `status: accepted` because the user accepted the exact revision;
4. replay the complete revised scenario from the beginning;
5. do not proceed until the revised scenario is valid or a remaining limitation is explicitly resolved.

### Phase 5 — Verify locators and design the implementation

After the scenario is valid:

1. reuse existing locators from `src/locators/` where suitable;
2. verify locator uniqueness in the relevant UI state;
3. select stable new locators only when necessary;
4. keep locators out of tests, flows, and assertions;
5. identify existing or required page/component methods;
6. identify existing or required flow methods in `src/flows/`;
7. identify existing or required assertion methods in `src/assertions/`;
8. identify fixtures, test data, cleanup, and parametrization;
9. determine the correct existing test to update or the cohesive `tests/ui/` module to create;
10. determine screenshot evidence behavior for every UI assertion;
11. calculate the exact cumulative pytest marker set and registration changes from `config/marker-policy.yaml`;
12. determine the exact value to write to `automation_marks`;
13. determine traceability mapping.

Render `assets/implementation-plan-template.md` and stop for user approval before editing automation.

### Phase 6 — Implement after plan acceptance

After `ACCEPT PLAN`:

- create or update the Selenium test;
- create or update locator modules only for required stable selectors;
- create or update page/component objects only for required low-level interactions;
- create or update flow modules/classes for business actions;
- create or update assertion modules/classes for UI checks and screenshot evidence;
- add or reuse fixtures in `tests/conftest.py` or the narrowest suitable local `conftest.py`;
- add parametrization only when it preserves a single coherent behavior;
- add every required and accepted pytest mark;
- add or update marker registration when missing and included in the accepted plan;
- keep tests independent and deterministic;
- add cleanup for created or modified data when required;
- update the source testcase to `automation_status: pending_verification`, write the proposed test node ID, and write the exact applied `automation_marks`;
- update the feature README automation columns;
- perform a static consistency review without running prohibited commands.

Do not commit or push.

### Phase 7 — User-run verification

Identify the repository's normal runner from existing configuration and documentation.

Provide:

1. the narrowest command for the implemented test or parameter;
2. a feature-level command when discoverable;
3. the UI smoke command when relevant and discoverable;
4. the full UI regression command when discoverable.

Inspect sibling accepted cases in `docs/testcase/<feature-slug>/`. If the current case would make every accepted case in that feature automated, explicitly request the feature-level run after the targeted run. Request the full UI regression run as well when repository policy requires it for completion.

Ask the user to run the required command or commands and provide the complete output.

Do not claim the test passed before receiving the result.

### Phase 8 — Analyze results

When the user provides output, classify failures as:

- implementation defect;
- locator/synchronization defect;
- testcase mismatch;
- product defect;
- environment/test-data blocker;
- unrelated existing-suite failure.

Do not hide or automatically rewrite product failures.

For required changes, explain the issue and proposed files, then follow the repository's approval rules before editing.

When the targeted test passes, render `assets/implementation-review-template.md` and wait for:

- `ACCEPT AUTOMATION`
- `DISCUSS: <comment>`

### Phase 9 — Finalize accepted automation

On `ACCEPT AUTOMATION` after a passing user-run result:

1. set `automation_status: implemented`;
2. set `automation_test` to the exact pytest node ID or stable repository test reference;
3. set `automation_last_verified` to the verified date;
4. set `automation_environment` to the environment used;
5. clear or update `automation_notes` so it reflects only a current accepted limitation;
6. preserve `additional_pytest_marks` as testcase-specific metadata;
7. verify and persist the exact final set in `automation_marks`;
8. update the visible Automation section in the source case;
9. update the feature README automation columns;
10. report changed files, mapping, complete marks, screenshot evidence, and verification command;
11. stop without starting another testcase.

## Completion boundary

This skill ends after one testcase is accepted as automated, mapped to existing automation, blocked with an accepted reason, or cancelled.

A later invocation must be used for the next testcase.
