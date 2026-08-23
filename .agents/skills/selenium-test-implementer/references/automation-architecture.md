# Automation Architecture

## Primary principle

The test function expresses the business scenario. Technical UI mechanics stay below it.

This repository already separates clients, configuration, WebDriver, locators, pages, flows, assertions, and tests. Reuse those layers.

## Layer responsibilities

### Test module — `tests/ui/`

Owns:

- cumulative pytest marks;
- fixture injection;
- parameter selection;
- a short sequence of business-level flow calls and business-level assertion calls;
- testcase ID traceability.

Must not contain:

- selectors;
- direct `WebDriver` calls;
- direct waits;
- direct screenshot calls;
- raw element manipulation;
- low-level navigation details;
- direct UI assertions.

Illustrative shape only; adapt names and style to the repository:

```python
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.smoke
def test_tc_001_successfully_update_profile(
    profile_flow,
    profile_assertions,
    profile_data,
):
    profile_flow.update_profile(profile_data)
    profile_assertions.profile_is_updated(
        profile_data,
        evidence_id="TC-001-profile-is-updated",
    )
```

### Flow/business-action layer — `src/flows/`

Owns user-oriented operations and workflow composition, for example:

```text
open_profile
update_profile
submit_order
search_for_customer
complete_checkout
```

A flow method may call several page/component methods to express one business action.

It must not own expected-result assertions. It may raise clear interaction errors when a required action cannot be completed.

### Assertion layer — `src/assertions/`

Owns expected UI outcomes, waits for assertion state, actual-value extraction, screenshot evidence, and assertion messages.

Examples:

```text
profile_is_updated
validation_message_is_displayed
order_confirmation_is_visible
search_results_contain_customer
```

Reuse `page_assertions.py` when the assertion is genuinely generic. Create a feature-specific assertion module only when that improves cohesion and reuse.

Do not scatter assertions across tests, flows, or page objects.

### Page/component layer — `src/pages/`

Owns:

- low-level UI interactions;
- state queries;
- page/component-specific waits;
- navigation behavior local to that page/component.

Page objects may verify that the correct page/component loaded as a structural guard, but business assertions belong in the assertion layer.

### Locator layer — `src/locators/`

Owns selectors separately from page behavior.

Do not embed raw selectors in tests, flows, assertions, fixtures, or ad hoc helper code.

### Browser and configuration layers

Reuse:

```text
src/clients/
src/webdriver/
src/config/
src/models/
config/default.yaml
```

Do not create a second browser client, driver factory, URL resolver, or execution-mode configuration.

### Fixtures and conftest

`tests/conftest.py` owns shared setup, lifecycle, dependency wiring, browser sessions, environment configuration, reusable data provisioning, authentication state, and cleanup.

Use `tests/ui/<feature_package>/conftest.py` only for truly feature-local fixtures.

Do not place business workflows in `conftest.py` merely to hide them from tests.

## Repository-aligned directory structure

Use:

```text
tests/
├── conftest.py
├── ui/
│   └── <feature_package>/
│       ├── conftest.py                 # only when feature-local fixtures are justified
│       └── test_<workflow_module>.py
├── smoke/                              # search/update existing tests, no automatic migration
└── regression/                         # search/update existing tests, no automatic migration

src/
├── assertions/
├── clients/
├── config/
├── flows/
├── locators/
├── models/
├── pages/
│   └── components/
└── webdriver/
```

Do not create `tests/functionality/`, `tests/features/`, or `src/features/` while the repository profile applies.

Use Python identifiers and automation paths with underscores. Keep testcase/document paths in kebab-case. Derive `customer_profile` from `customer-profile`.

## Test grouping strategy

Do not create one Python file per testcase by default.

Put cases in the same module when they share:

- the same feature boundary;
- the same primary workflow;
- compatible actor and state;
- compatible fixtures and cleanup;
- common flow and assertion services.

Split modules when cases involve materially different:

- user journeys;
- actors or permissions;
- setup/cleanup lifecycle;
- page groups;
- external boundaries;
- parameter models.

A test function remains the one-to-one unit mapped to a manual testcase, except when a well-designed parameterized test intentionally maps several equivalent cases.

## Naming

New test function or method:

```text
test_<case-id-lower>_<testcase-slug-with-underscores>
```

Example:

```text
test_tc_014_rejects_invalid_phone_number
```

Flow method names should describe user intent, not widgets.

Preferred:

```text
profile_flow.update_contact_details(data)
```

Avoid:

```text
profile_flow.click_first_name_and_type_then_click_save(data)
```

## Reuse and abstraction threshold

Reuse existing abstractions first.

Create a new shared abstraction when it is:

- required to keep test code business-oriented;
- clearly reusable by the source case and nearby coverage; or
- necessary to centralize a locator, wait, assertion evidence, or lifecycle concern.

Do not create a generic framework abstraction for a single trivial line unless it enforces an explicit project rule.

## Test independence

Each test must be runnable alone.

Do not depend on test ordering or state created by a previous test.

Use fixtures and cleanup to establish and remove state.

Do not share mutable test data between tests unless the framework explicitly isolates copies.
