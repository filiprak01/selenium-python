# UI Replay and Locator Discovery

## Purpose

Validate that the accepted manual scenario can actually be performed and identify stable UI access points before automation is written.

## Reuse the existing browser setup

Locate and reuse:

- configured URL aliases;
- environment selection;
- browser mode;
- browser client or MCP capability;
- authentication/session bootstrap;
- test accounts and data aliases;
- feature-flag configuration.

Do not hardcode URLs or create another browser client.

Use a safe local, development, test, or staging environment. Treat production as read-only unless the user explicitly authorizes a safe action.

## Replay procedure

Start from the global preconditions and replay every step from the beginning.

For every step record internally:

- expected starting state;
- action requested by the case;
- data required;
- expected UI result;
- observed UI result;
- additional prerequisite discovered;
- candidate page/component owner;
- candidate locator and uniqueness;
- whether the step is safe and repeatable.

Do not skip intermediate navigation because it seems obvious. The purpose is to discover missing states such as:

```text
A Save button appears only after a field changes.
A Continue button remains disabled until a checkbox is selected.
A menu item is available only after opening a parent menu.
A result row exists only after a filter is applied.
A modal action requires scrolling or another confirmation.
```

## Discrepancy classification

### MANUAL_CASE_ISSUE

Use when the accepted case itself is incomplete, internally inconsistent, or factually wrong, for example:

- missing navigation or state-transition step;
- action performed before the control can exist;
- invalid test data for the stated path;
- expected result describes a different page or message;
- required precondition is absent;
- action order cannot be completed.

Propose an exact testcase revision.

### PRODUCT_DEFECT

Use when the accepted behavior appears valid but the product does not provide it, for example:

- required button is absent;
- expected successful action produces an error;
- validation contradicts an explicit requirement;
- navigation ends on the wrong destination;
- state is not persisted when the case says it must be.

Do not rewrite the testcase to match the defect. Provide observed evidence and stop for user direction.

### ENVIRONMENT_BLOCKER

Use when the behavior cannot be judged because of:

- application unavailability;
- missing credentials or test account;
- missing test data;
- permission mismatch;
- disabled feature flag;
- service outage;
- environment-specific configuration.

Report what is needed to continue.

### AUTOMATION_BLOCKER

Use when the scenario is valid but reliable automation is currently prevented by, for example:

- CAPTCHA;
- unsupported two-factor flow without a test bypass;
- no stable way to identify a required element;
- browser-native interaction unsupported by the framework;
- an external irreversible action.

Recommend the smallest safe framework or product testability change.

### AMBIGUITY

Use when multiple outcomes are plausible and neither requirements, repository evidence, nor observed UI determines the correct one.

Do not guess.

## Locator policy

Reuse a verified existing locator first.

For a new locator, prefer in this order when stable in the application:

1. explicit stable test attribute such as `data-testid`, `data-test`, or repository equivalent;
2. unique, predictable HTML `id`;
3. stable accessible attribute, label relationship, or semantic name;
4. stable `name` attribute;
5. concise, scoped CSS selector based on durable attributes;
6. concise, scoped XPath only when necessary.

Avoid:

- absolute XPath;
- numeric DOM indexes unless the index is the behavior under test;
- generated class names;
- deeply nested selectors tied to layout;
- text-only selectors in localized applications unless visible text is the tested behavior;
- selectors that match more than one actionable element in the relevant state.

Verify each locator in the state where it is used, including conditional visibility.

## Locator ownership

Define locator tuples/constants in the relevant module under `src/locators/`.

The corresponding object under `src/pages/` or `src/pages/components/` must import and use those locators while exposing low-level UI interactions and state queries.

Do not place raw locators in:

- test functions;
- flow/business-action modules;
- assertion modules;
- `conftest.py`;
- testcase Markdown;
- client or WebDriver factories.

Flows and assertions call page/component services; they do not import locator modules directly.

## Synchronization

Reuse the repository's explicit wait utilities.

Wait for the state required by the business action or assertion, such as:

- visible;
- enabled/clickable;
- value updated;
- text present;
- navigation completed;
- modal opened or closed;
- loading indicator removed.

Do not add arbitrary sleeps.

Do not introduce a mixture of implicit and explicit waits when the framework avoids it.

## Safe data and cleanup

Use disposable or generated data when the scenario changes state.

Identify how the test returns the environment to a reusable state. Prefer fixture-driven cleanup or repository data APIs already intended for test setup/teardown.

Do not automate irreversible production data changes.

## Evidence during validation

When the browser capability supports screenshots, capture evidence for material discrepancies without exposing secrets. Evidence from discovery supports the report but does not replace assertion-level evidence in the implemented test.
