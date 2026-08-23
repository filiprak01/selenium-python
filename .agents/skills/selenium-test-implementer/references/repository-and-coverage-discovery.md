# Repository and Existing-Coverage Discovery

Perform discovery before live replay and before writing code.

Read `references/repository-profile.md` first.

## 1. Repository instructions

Locate and obey every applicable:

```text
AGENTS.md
AGENTS.override.md
```

The repository contains scoped AGENTS files in framework and test directories. Read the root file and every scoped file governing a file that may be changed.

Determine branch, planning, command execution, commit, and push restrictions.

## 2. Existing framework

Inspect the established paths before proposing new files:

```text
config/default.yaml
src/clients/
src/config/
src/models/
src/webdriver/
src/locators/
src/pages/
src/pages/components/
src/flows/
src/assertions/
src/logging/
tests/conftest.py
tests/ui/
tests/smoke/
tests/regression/
screenshots/
allure-results/
```

Identify:

- active pytest configuration and registered marks;
- repository-wide mandatory marks;
- Selenium/browser fixtures;
- UI client and driver lifecycle;
- URL/environment resolver;
- headless/headed/local/remote modes;
- authentication/session bootstrap;
- locator modules;
- page and component objects;
- flow/business-action modules;
- assertion modules;
- wait utilities;
- screenshot/evidence utilities;
- test-data factories and fixtures;
- cleanup utilities;
- Allure/report integrations;
- test naming and import conventions;
- CI marker selections.

Do not introduce a parallel framework when equivalent facilities already exist.

## 3. Search for existing automation

Search all of:

```text
tests/ui/
tests/smoke/
tests/regression/
```

Use:

- exact testcase ID;
- testcase title and slug;
- feature slug;
- business action;
- page names;
- significant test data class;
- expected message or outcome;
- relevant locator/page/flow/assertion method names;
- automation path already recorded in the testcase;
- equivalent parameter rows.

Inspect behavior, not only names or directory placement.

A test under `tests/smoke/` may also be regression and UI coverage through marks. Directory names are not the sole source of classification.

## 4. Coverage relationship

Classify the source case as one of:

### ALREADY_IMPLEMENTED

An existing test materially covers the same:

- initial state;
- business action;
- relevant data class;
- outcome;
- risk.

Do not create another test. Validate the existing test, its complete marks, and propose traceability metadata if missing.

### PARTIALLY_IMPLEMENTED

Existing automation covers only part of the case or an existing parameterized test can accept another data row.

Prefer extending the existing cohesive implementation.

### UPDATE_REQUIRED

Mapped or semantically equivalent automation exists but no longer matches the accepted testcase, current UI, marker policy, or evidence policy.

Plan a focused update.

### NEW_AUTOMATION

No equivalent implementation exists.

Create the test under:

```text
tests/ui/<feature_package>/test_<workflow_module>.py
```

### CONFLICTING_AUTOMATION

Existing automation asserts behavior that conflicts with the accepted case or verified UI.

Report the conflict before editing.

## 5. Avoid duplication

Different sample data does not make a scenario new when the behavior and outcome are equivalent.

Do not create:

- another test for the same accepted case;
- a second locator module for the same page without a clear boundary;
- a second page object for the same page;
- a second UI client or URL resolver;
- a duplicate login fixture;
- a duplicate screenshot helper;
- a new assertion helper when an equivalent one exists;
- `src/features/` when `src/flows/` already owns business actions;
- `tests/functionality/` while `tests/ui/` is the selected target.

## 6. Existing-test update policy

When equivalent automation exists in `tests/smoke/` or `tests/regression/`:

- prefer updating it in place;
- add missing required marks only through the accepted implementation plan;
- preserve compatible existing marks;
- do not move the file merely to normalize directories;
- propose migration separately only when there is a demonstrated maintainability benefit.

## 7. Scope of changes

Only include files necessary to implement or update the source case and shared support clearly required by it.

Do not use one testcase as a reason to:

- migrate the whole framework;
- rename unrelated modules;
- replace the UI client;
- rewrite all page objects;
- reorganize every test;
- move all smoke/regression files into `tests/ui/`;
- change CI globally without demonstrated need.

When a framework gap affects future cases, include it as a clearly separated optional recommendation in the plan.
