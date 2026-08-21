---
name: ui-testcase-designer
description: Design Selenium-oriented UI test cases from a feature prompt. Use when the user wants repository-aware UI coverage analysis, reuse of an existing browser client and environment configuration, safe live UI exploration, duplicate detection, and one-by-one review of smoke, regression, edge-case, and E2E cases before accepted Markdown files are written. Do not generate automation code.
---

# UI Test Case Designer

## Goal

Create maintainable UI test-case documentation for an implemented or described feature.

The workflow must:

1. understand the feature;
2. inspect existing manual test cases;
3. inspect existing Selenium or other UI automation for coverage evidence;
4. discover and reuse the repository's existing browser client, URLs, environments, and execution modes;
5. explore the running UI in a safe browser session when available;
6. identify Smoke, Regression, edge-case, and meaningful E2E coverage;
7. remove duplicates and prefer updates to overlapping or outdated cases;
8. present exactly one proposed test case;
9. wait for the user's decision;
10. save only explicitly accepted cases;
11. create an automation-ready handoff for `$selenium-test-implementer`.

This skill designs test cases only. It must not create, edit, or delete Selenium automation.

## Required supporting files

Before proposing the first test case, read:

- `references/repository-discovery.md`
- `references/browser-configuration-reuse.md`
- `references/coverage-rules.md`
- `references/review-protocol.md`
- `assets/proposal-template.md`
- `assets/accepted-testcase-template.md`
- `assets/feature-readme-template.md`

Resolve these paths relative to this skill directory.

## Non-negotiable rules

- Respect every applicable `AGENTS.md` or `AGENTS.override.md`.
- Never work directly on the main branch when repository instructions forbid it.
- Never create automation code as part of this skill.
- Never create a temporary Selenium, shell, Python, or JavaScript script for UI exploration.
- Reuse the configured browser client and its existing URLs and modes.
- Use configured browser or MCP tools for exploration. Prefer headless mode when supported and configured.
- Never duplicate or hardcode environment URLs already owned by repository configuration.
- Never install dependencies without explicit user approval.
- Never perform destructive or irreversible UI actions.
- Never expose or persist passwords, tokens, or other secrets.
- Never output a batch of candidate cases.
- Present exactly one unresolved proposal per response.
- Never save a proposed case before explicit `ACCEPT`.
- Never change an existing case before explicit `ACCEPT`.
- A rejected proposal must not consume a permanent test-case ID.
- Do not re-propose a rejected case with superficial wording changes.
- Do not treat E2E as an alternative to Smoke or Regression.
- Do not use `Edge case` as the test type. Edge cases normally use `Type: Regression` and an appropriate `Case kind`.
- Every accepted case must start with `automation_status: not_implemented` and `automation_marks: []` unless equivalent automation is already verified and mapped.
- Record testcase-specific extra pytest marks in `additional_pytest_marks`; do not duplicate automatically derived `ui`, `regression`, `smoke`, or `e2e` marks there.
- Do not invent additional pytest marks. Include them only when the user requests them or repository evidence makes them explicit.

## Storage contract

Accepted cases belong under:

```text
docs/testcase/<feature-slug>/
```

Use this structure:

```text
docs/testcase/<feature-slug>/
├── README.md
├── TC-001-<test-case-slug>.md
├── TC-002-<test-case-slug>.md
└── ...
```

Use lowercase kebab-case for `<feature-slug>` and `<test-case-slug>`.

Assign the next available sequential ID only after acceptance.

## Classification contract

Every case must include:

- `Type`: `Smoke` or `Regression`
- `Scope`: `Feature` or `E2E`
- `Case kind`: `Happy path`, `Negative`, `Validation`, `Boundary`, or `State and recovery`
- `Priority`: `Critical`, `High`, `Medium`, or `Low`

Examples:

```text
Type: Smoke
Scope: Feature
Case kind: Happy path
```

```text
Type: Regression
Scope: E2E
Case kind: State and recovery
```

## Automation handoff contract

Every accepted case must include these frontmatter fields:

```yaml
additional_pytest_marks: []
automation_status: not_implemented
automation_test: null
automation_marks: []
automation_last_verified: null
automation_environment: null
automation_notes: null
```

Allowed automation states are:

```text
not_implemented
pending_verification
implemented
blocked
update_required
```

The testcase designer normally writes `not_implemented`. It may write `implemented` only when repository discovery proves that materially equivalent automation already exists, the mapping is unambiguous, and the user accepts that mapping.

Do not generate implementation paths speculatively.

`additional_pytest_marks` contains only testcase-specific additions. `automation_marks` starts empty and is later populated by the automation skill with the exact applied set. The automation skill derives repository-required and classification marks from its marker policy. Older accepted cases without either field remain valid.

## Workflow

### 1. Build a feature model

From the prompt and repository evidence, identify internally:

- feature name and slug;
- user goal and actor;
- entry point and pages involved;
- visible controls and fields;
- input rules and validation;
- state transitions;
- successful and unsuccessful outcomes;
- permissions and relevant user states;
- integration boundaries;
- possible larger user journeys.

Do not print a long feature analysis unless the user asks for it.

### 2. Discover existing coverage

Follow `references/repository-discovery.md`.

Search existing documentation before proposing anything.

For each candidate scenario, classify its relationship to current coverage as:

- `NEW`
- `EXISTING`
- `OVERLAPPING`
- `OUTDATED`

Do not propose a duplicate of an `EXISTING` case.

For `OVERLAPPING` or `OUTDATED`, propose a change to the existing file instead of creating a duplicate.

### 3. Discover and reuse browser configuration

Follow `references/browser-configuration-reuse.md`.

When a runnable UI exists, use the repository's existing client, URL resolution, authentication/session bootstrap, and execution mode. Do not create a second browser setup.

### 4. Explore the UI when available

Use a configured browser tool when:

- the application is running or a safe URL can be resolved from repository configuration;
- the environment is local, development, test, or staging;
- the action is safe and reversible;
- repository permissions allow it.

Inspect visible controls, states, validation, navigation, defaults, disabled states, conditional content, and observable results.

Do not create browser automation code.

When live exploration cannot be performed, continue with repository and prompt evidence and label the verification basis accurately. Do not pretend the UI was inspected.

### 5. Build the candidate queue internally

Derive meaningful candidate scenarios using `references/coverage-rules.md`.

Keep the queue internal. Do not print it.

Default review order:

1. Smoke / Feature
2. Smoke / E2E
3. Regression / Feature
4. Regression / E2E
5. remaining edge cases within Regression

Within each group, prioritize business impact and failure risk.

### 6. Present one proposal

Render exactly one case using `assets/proposal-template.md`.

The steps table must contain:

- step number;
- step precondition;
- one user action;
- explicit test data or `N/A`;
- one or more observable UI results.

Then stop and wait for:

- `ACCEPT`
- `REJECT`
- `DISCUSS: <comment>`

Do not present the next proposal in the same response.

### 7. Process the decision

Follow `references/review-protocol.md`.

On `ACCEPT`:

1. assign the next available ID, unless updating an existing case;
2. render the accepted file using `assets/accepted-testcase-template.md`;
3. initialize or preserve `additional_pytest_marks`, `automation_marks`, and the remaining automation handoff fields;
4. save or update the case;
5. create or update the feature `README.md` using `assets/feature-readme-template.md`;
6. confirm the saved path briefly;
7. present exactly one next proposal, or the completion summary when no candidates remain.

On `REJECT`:

1. do not write a case file;
2. retain the rejection only in current conversation state;
3. move to the next distinct candidate;
4. present exactly one next proposal, or the completion summary.

On `DISCUSS` or any requested edit:

1. do not save;
2. discuss only the current case;
3. revise the same case;
4. present the revised case again;
5. wait for a new decision.

## Completion

When all meaningful candidates have been resolved, report:

```text
Feature: <feature name>
Accepted: <count>
Updated existing cases: <count>
Rejected: <count>
Smoke: <count>
Regression: <count>
E2E scope: <count>
Unverified behavior: <short note or None>
```

Do not generate automation after completion.
