# UI Validation Report — <TC-###>

**Source testcase:** `<relative path>`

**Environment:** <safe environment alias>

**Browser mode/client:** <existing configured mode and client>

**Validation result:** <VALID | CHANGES REQUIRED | BLOCKED | POTENTIAL PRODUCT DEFECT>

**Existing automation relationship:** <ALREADY_IMPLEMENTED | PARTIALLY_IMPLEMENTED | UPDATE_REQUIRED | NEW_AUTOMATION | CONFLICTING_AUTOMATION>

## Replay results

| Step | Expected state/action/result | Observed behavior | Status | Classification |
|---:|---|---|---|---|
| 1 | <concise expected behavior> | <concise observed behavior> | <PASS / ISSUE / BLOCKED> | <None or issue type> |

## Material issues

### <Issue number> — <Short title>

- **Classification:** <MANUAL_CASE_ISSUE | PRODUCT_DEFECT | ENVIRONMENT_BLOCKER | AUTOMATION_BLOCKER | AMBIGUITY>
- **Affected step:** <number or Preconditions>
- **Expected:** <expected behavior>
- **Observed:** <observed behavior>
- **Impact:** <why the case cannot be safely implemented as written>
- **Recommendation:** <exact next action>

## Locator readiness

- Existing locators reusable: <paths or None>
- New stable locators identified: <page/component and concise description or None>
- Locator blockers: <None or concise details>

## Decision

[ACCEPT CASE CHANGES] — apply the exact proposed testcase revision and replay it

[KEEP CASE / REPORT DEFECT] — keep the testcase unchanged and treat observed behavior as a potential product defect

[DISCUSS: <comment>] — revise the diagnosis or proposed changes

[CANCEL] — stop this implementation
