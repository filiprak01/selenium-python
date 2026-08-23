# Selenium Implementation Review Protocol

This workflow uses explicit decision gates.

## Gate 1 — UI validation discrepancy

When the manual scenario has a material issue, display:

```text
[ACCEPT CASE CHANGES] — apply the exact proposed testcase revision and replay it
[KEEP CASE / REPORT DEFECT] — keep the testcase unchanged and treat observed behavior as a potential product defect
[DISCUSS: <comment>] — revise the diagnosis or proposed changes
[CANCEL] — stop this implementation
```

Then stop.

### ACCEPT CASE CHANGES

- Apply only the exact accepted revision.
- Preserve the testcase ID.
- Update the feature README when title, type, scope, case kind, priority, or mapping changes.
- Replay the full testcase from the beginning.
- Do not implement until replay succeeds or remaining limitations are explicitly resolved.

### KEEP CASE / REPORT DEFECT

- Do not rewrite expected behavior.
- Keep or set automation state to `blocked` when implementation cannot produce a passing valid test.
- Record a concise blocker in the case only when the user asks or accepts that change.
- Do not create an intentionally failing test unless the user explicitly requests that project policy.

### DISCUSS

- Discuss only the current source case and validation evidence.
- Revise the report or patch.
- Show the complete revised proposal and gate again.

## Gate 2 — Implementation plan

After successful UI validation, display:

```text
[ACCEPT PLAN] — implement the exact plan
[DISCUSS: <comment>] — change architecture, files, marks, data, locators, or scope
[CANCEL] — stop without implementing
```

Then stop.

Requested changes mean the plan is not accepted. Show the complete revised plan again.

## Gate 3 — User-run verification

After implementation, do not ask for final acceptance until the user provides the targeted test result.

Provide the exact command and request complete output.

When output fails, diagnose it and propose a focused correction. Follow repository approval rules before editing.

## Gate 4 — Final automation review

After a passing user-run result, display:

```text
[ACCEPT AUTOMATION] — finalize testcase mapping and implemented status
[DISCUSS: <comment>] — request code, architecture, assertion, evidence, or naming changes
```

Then stop.

### ACCEPT AUTOMATION

- Update automation metadata and feature README.
- Report the final node ID, marks, evidence behavior, and verified command.
- Do not start another testcase.

### DISCUSS

- Keep automation as `pending_verification` until requested changes are implemented, rerun, and accepted.
- Do not infer acceptance from praise combined with a requested edit.

## Existing automation mapping

When equivalent automation already exists, still use the plan gate before changing testcase metadata or existing code.

If no code change is required, the plan should state that only mapping and verification are proposed.
