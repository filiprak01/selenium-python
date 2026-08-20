# Repository and UI Discovery

Use this procedure before proposing the first test case.

## 1. Read repository instructions

Locate and obey all applicable:

```text
AGENTS.md
AGENTS.override.md
```

Start at the repository root and include more specific instructions down to the current working directory.

Repository instructions override this reference when they are more restrictive.

## 2. Identify the repository structure

Determine:

- repository root;
- application technology;
- UI module locations;
- test module locations;
- documentation conventions;
- application start instructions;
- environment configuration;
- browser or MCP tools currently available.

Do not add a new dependency merely to perform discovery.

## 3. Search manual test cases

Search this location first:

```text
docs/testcase/
```

Also inspect an existing legacy location such as `docs/testcases/` when the repository already uses it, but save newly accepted cases only to the configured canonical location.

Search by:

- feature name;
- page name;
- route;
- visible labels;
- component names;
- business action;
- validation message;
- related user journey;
- synonyms for the same behavior.

Inspect file contents, not only filenames.

## 4. Search existing UI automation

Inspect existing automation only as coverage evidence.

Common locations and patterns include:

```text
src/test/
tests/
test/
e2e/
ui-tests/
automation/
**/*Test.java
**/*Tests.java
**/*IT.java
**/pages/
**/pageobjects/
**/page_objects/
**/fixtures/
**/testdata/
```

Also inspect:

- Selenium page objects;
- test classes and suite definitions;
- tags, groups, and categories;
- test-data builders and fixtures;
- navigation helpers;
- configuration files;
- CI definitions that select smoke, regression, or E2E suites.

Do not edit automation.

Documented coverage and automated coverage are different facts. A scenario may be:

- documented but not automated;
- automated but not documented;
- both;
- neither.

## 5. Inspect the implementation

When useful, inspect:

- routes;
- UI components;
- form definitions;
- validators;
- visible error messages;
- feature flags;
- permissions;
- state-management code;
- API contracts only to understand UI behavior;
- page objects and selectors only to locate controls.

Do not turn selector or implementation details into manual test steps.

## 6. Explore the running UI safely

Use an available configured browser tool or MCP integration.

Prefer headless mode where the tool supports it.

Never create a temporary Selenium, shell, JavaScript, or Python script solely for exploration.

Explore only when the environment and permissions are safe.

Prefer:

```text
local
development
test
staging
```

Treat production as read-only unless the user explicitly authorizes a safe test action.

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
- entering disposable values without submitting;
- triggering client-side validation;
- observing enabled and disabled states;
- navigating back and forward;
- checking modal and notification behavior.

Use credential aliases such as:

```text
<ACTIVE_TEST_USER_EMAIL>
<ACTIVE_TEST_USER_PASSWORD>
```

Never copy secret values into test-case files.

## 7. Record the verification basis

Each proposal must state one of:

```text
Live UI + repository
Repository only
Prompt + repository
Prompt only
```

When UI exploration failed or was unavailable, state the reason briefly and do not claim verification.

## 8. Detect duplicates and changes

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

A changed title or different sample data does not make a case new when the behavior and risk are equivalent.
