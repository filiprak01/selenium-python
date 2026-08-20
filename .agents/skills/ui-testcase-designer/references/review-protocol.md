# One-by-One Review Protocol

This protocol is a state machine. Exactly one proposal may be unresolved at a time.

## Proposal state

A proposal is not a repository test case.

Before acceptance:

- do not assign a permanent ID;
- do not create its Markdown file;
- do not add it to the feature README;
- keep it only in the active conversation.

## Allowed decisions

Display exactly these choices after every proposal:

```text
[ACCEPT] — approve and save this case
[REJECT] — discard this case
[DISCUSS: <comment>] — revise, clarify, split, merge, or question this case
```

Then stop.

## ACCEPT

Treat a response as acceptance only when approval is clear.

On acceptance:

1. Re-check that an equivalent file was not added since discovery.
2. For a new case, calculate the next available sequential `TC-###` ID.
3. For an existing-case update, retain its current ID and path.
4. Save the accepted case using `assets/accepted-testcase-template.md`.
5. Create or update the feature `README.md`.
6. Confirm the saved or updated path in one line.
7. Present exactly one next proposal, or the completion summary.

Do not ask again before saving the exact proposal the user accepted.

## Requested edits

Any requested content change means the case is not yet accepted.

Examples:

```text
Accept but change step 3.
Looks good, but add another expected result.
Use different data and save it.
```

Treat these as `DISCUSS`.

Revise the same case, show it again, and wait for explicit acceptance of the revised version.

## REJECT

On rejection:

1. Do not create or modify a test-case file.
2. Do not consume an ID.
3. Remember the rejected scenario for this conversation.
4. Do not re-propose a semantically equivalent case.
5. Present exactly one distinct next proposal, or the completion summary.

A rejection reason may improve later proposals but must not be persisted unless the user explicitly requests it.

## DISCUSS

Discussion applies only to the current case.

The user may:

- change Type, Scope, Case kind, or Priority;
- add, remove, or reorder steps;
- change data;
- change expected results;
- split the case;
- merge it with existing coverage;
- question whether it is needed;
- clarify business behavior.

After discussion:

1. revise the same case;
2. do not save;
3. show the complete revised case;
4. display the three decisions;
5. stop.

When a split is requested, keep the highest-priority resulting case as the current proposal and queue the other internally.

## Existing-case changes

For `OVERLAPPING` or `OUTDATED` coverage, add this block before the proposal:

```text
Change type: UPDATE EXISTING TEST CASE
Existing file: <relative path>
Reason: <concise reason>
```

Do not modify that file until `ACCEPT`.

## Batch handling

Batch review is disabled.

Even when several candidates exist:

- do not print a list of full cases;
- do not print multiple proposals;
- do not save several unreviewed cases;
- do not infer approval for later cases from approval of the current case.

## Completion

When no unresolved candidates remain, provide a concise coverage summary and stop.

Do not transition into automation generation.
