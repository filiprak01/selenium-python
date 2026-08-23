# UI Assertion Screenshot Evidence

## Requirement

Every logical assertion that verifies a UI element or visible UI state must create screenshot evidence.

This applies to assertions such as:

- element is visible or hidden;
- text or validation message is displayed;
- control is enabled or disabled;
- value is displayed or persisted;
- modal, notification, table row, page, or navigation outcome is visible;
- selected state is reflected in the UI.

Non-UI assertions, such as pure data transformation checks, do not require screenshots unless repository policy says otherwise.

## Ownership

Screenshot creation belongs in the assertion/evidence layer, not in the test function.

The test should call a business assertion and provide or derive a stable evidence ID.

Reuse the repository's existing screenshot helper, reporting integration, or attachment facility.

If no reusable mechanism exists, the implementation plan may add one shared evidence service and fixture. Do not create a separate screenshot helper for every feature.

## Capture behavior

For each logical UI assertion:

1. wait for the state that should be evaluated;
2. capture a screenshot showing the current state;
3. perform the assertion with a clear failure message;
4. if an exception or assertion failure occurs before a useful screenshot was captured, capture a failure screenshot and re-raise.

An automatic screenshot-on-test-failure hook is useful but does not replace per-assertion evidence.

## Screenshot scope

Prefer an element screenshot when it clearly captures the asserted element and the framework supports it.

Use a viewport/full-page screenshot when:

- the assertion concerns navigation, layout, multiple elements, a modal, or a notification;
- the element screenshot would omit necessary context;
- the repository evidence helper captures only viewport images.

## Naming

Use stable, filesystem-safe names containing:

- testcase ID;
- assertion purpose;
- optional parameter ID;
- sequence or timestamp when required by the existing reporter.

Example:

```text
TC-001__profile-is-updated.png
TC-014__invalid-phone-message__too-short.png
```

Do not use secrets, personal data, or raw test values in filenames.

## Storage and reporting

Reuse the repository's existing paths and report integration:

```text
screenshots/
allure-results/
```

Use the existing screenshot helper and Allure attachment behavior when present. Do not create a parallel `artifacts/screenshots/` tree.

If the current helpers do not support assertion-level evidence, propose one shared extension in the implementation plan. Keep storage configurable and route it through the existing `screenshots/` directory and reporting integration rather than duplicating path logic across assertion modules.

## Sensitive content

Do not capture passwords, tokens, payment data, or other secrets.

Before taking evidence:

- ensure password fields remain masked;
- avoid screenshots containing unrelated sensitive user data;
- crop to the asserted element when safer;
- use test accounts and synthetic data.

When safe evidence cannot be captured, report the limitation rather than storing sensitive output.

## Assertion design

Assertion methods should expose business meaning, for example:

```text
profile_is_updated
required_field_message_is_visible
order_confirmation_is_displayed
```

Avoid assertion APIs that expose selector or driver details to the test.

A composite business assertion may contain several logical UI assertions. Each logically independent checked UI state must have sufficient evidence, either through separate screenshots or one screenshot that clearly proves all of them.
