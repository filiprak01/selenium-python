# UI Coverage Rules

## Coverage model

Use separate fields for suite type and workflow scope.

### Type

Allowed values:

```text
Smoke
Regression
```

#### Smoke

Use for the smallest set of critical checks proving the feature is available and its primary user outcome works.

A Smoke case should normally cover:

- the primary path;
- a release-blocking capability;
- a high-impact E2E journey;
- a basic availability or navigation path only when it is independently valuable.

Do not classify every successful case as Smoke.

#### Regression

Use for:

- alternate successful paths;
- negative behavior;
- validation;
- boundary values;
- state transitions;
- recovery behavior;
- role or permission variations;
- persistence and navigation behavior;
- meaningful edge cases.

### Scope

Allowed values:

```text
Feature
E2E
```

#### Feature

The case validates one coherent feature or page behavior, even when several controls are used.

#### E2E

The case validates a meaningful user journey across multiple functional boundaries, pages, or persisted stages.

Multiple clicks alone do not make a case E2E.

A case may be both:

```text
Type: Smoke
Scope: E2E
```

or:

```text
Type: Regression
Scope: E2E
```

### Case kind

Allowed values:

```text
Happy path
Negative
Validation
Boundary
State and recovery
```

Edge cases normally use:

```text
Type: Regression
Case kind: Validation | Boundary | State and recovery
```

Do not create `Edge case` as a separate Type.

### Priority

Allowed values:

```text
Critical
High
Medium
Low
```

Base priority on user impact, business risk, and likelihood of regression.

## Candidate discovery

Consider:

- primary successful flow;
- required and optional fields;
- valid alternatives;
- invalid inputs;
- empty inputs;
- minimum and maximum boundaries;
- supported and unsupported formats;
- special characters and Unicode when relevant;
- duplicate submissions;
- repeated actions;
- disabled and enabled states;
- conditional controls;
- refresh, back navigation, and return to the page;
- saved or persisted state;
- role and permission differences;
- session expiry when relevant;
- error recovery;
- multi-page user journeys;
- integration handoffs visible in the UI.

Do not invent irrelevant cases to increase count.

## E2E detection

Suggest E2E coverage only when the feature participates in a meaningful journey.

Examples:

```text
Sign in
→ search for an item
→ select it
→ complete an action
→ observe confirmation
```

```text
Create a record
→ find it in a list
→ open details
→ update it
→ verify the updated state
```

Do not duplicate a feature case as an E2E case unless the larger journey adds distinct risk.

## Test design quality

Each test case must:

- validate one coherent risk or outcome;
- use an explicit starting state;
- use representative, concrete data or semantic placeholders;
- describe one meaningful user action per step;
- use UI-visible expected results;
- be understandable without reading automation code;
- be implementable later in Selenium without embedding Selenium details.

Avoid vague data such as:

```text
valid data
some user
correct value
```

Prefer:

```text
email: user@example.test
quantity: 5
country: Poland
<ACTIVE_TEST_USER>
<EXISTING_PRODUCT>
```

Use `N/A` when a step needs no data.

## Preconditions

Use global Preconditions for conditions applying to the whole case.

Examples:

```text
The application is available.
An active test user exists.
The user is logged out.
The user has Customer permissions.
```

Use the step `Precondition` column for the exact state required before that step.

Do not repeat every global precondition in every row.

## Actions

Use user-oriented UI language.

Good:

```text
Open the Login page.
Enter the email in the Email field.
Select Poland from the Country list.
Click Save.
```

Bad:

```text
Locate the element by XPath.
Invoke WebElement.click().
Call the backend.
```

## Expected results

Expected results must be observable through the UI.

Good:

```text
The Save button becomes enabled.
The validation message appears below the Email field.
The new item appears in the results table.
The Dashboard page is displayed.
```

Avoid internal-only outcomes:

```text
A database row is created.
The API returns HTTP 200.
The service receives the request.
```

An internal outcome may be mentioned only when the user explicitly requests hybrid UI/API verification. This skill is UI-only by default.

## Ordering

Present candidates in this order unless risk justifies a different priority:

1. critical Smoke / Feature;
2. critical Smoke / E2E;
3. high-value Regression / Feature;
4. high-value Regression / E2E;
5. remaining negative, validation, boundary, and recovery cases.

## Duplicate control

Do not create separate cases when differences are only:

- wording;
- equivalent sample data;
- reordered non-material setup;
- different selectors;
- different implementation details.

Create separate cases when they cover materially different:

- user outcomes;
- validation rules;
- states;
- permissions;
- boundaries;
- recovery paths;
- business risks.
