# AGENTS.md

## Scope

These instructions apply to the entire repository unless a more specific
`AGENTS.md` provides stricter directory-specific rules.

The following restrictions are non-negotiable:

- Do not modify code on `main`.
- Do not commit without explicit user approval.
- Do not push under any circumstances.
- Do not execute shell scripts, Python scripts, or test suites.
- Do not modify code before the implementation plan is explicitly approved.

## Communication

- Keep responses concise.
- Include only information relevant to the current task.
- Use simple, direct statements.
- Do not repeat the request or add unnecessary background.
- Clearly distinguish completed work, validation results, unverified work,
  assumptions, and blockers.
- Report a blocker as soon as it is discovered.

## Mandatory Planning and Approval

Before modifying code, tests, configuration, or documentation:

1. Inspect the relevant repository files using read-only operations.
2. Produce a concise implementation plan containing:
   - the objective;
   - the expected files or components to change;
   - the proposed implementation approach;
   - the validation approach;
   - known assumptions, risks, and open decisions.
3. Ask the user for explicit approval.
4. Do not begin modifications until approval is provided.

Silence, an unrelated response, or a general acknowledgment is not approval.

The user may reject the plan or request changes. Revise the plan and request
approval again when required.

If the approved approach changes materially during implementation, stop,
explain the reason, present the revised plan, and request approval again.

## Git Branch Workflow

Read-only inspection may be performed before branch preparation. Repository
modifications may begin only after the plan is approved and a dedicated
development branch is active.

Before starting modifications:

1. Check the current branch and working-tree status.
2. If uncommitted or untracked user changes are present, stop and report them.
   Do not stash, discard, overwrite, or relocate them.
3. If the current branch is `main`, propose a new development branch and wait
   for the user to approve its name.
4. Create the approved branch directly from the current `main`:

   ```text
   git switch -c feature/<short-description>
   ```

5. If the current branch is not `main`, continue on it only when the user
   explicitly approves using that branch for the task.
6. On the approved development branch, update from `origin/main` using a
   fast-forward-only pull:

   ```text
   git pull --ff-only origin main
   ```

New development branches must use this naming pattern:

```text
feature/<short-description>
```

Do not edit, stage, or commit task changes on `main`.

If the development branch cannot be updated from `origin/main` with a
fast-forward-only pull, stop and report the state. Do not merge, rebase, reset,
or force the update automatically.

## Conflict Handling

Never resolve a Git conflict automatically.

For every conflicting file, report:

- the file path;
- the current branch behavior or content;
- the incoming behavior or content;
- the important differences;
- the likely impact of each option;
- a recommendation, when one can be made safely;
- the exact decision required from the user.

Do not select a version, remove conflict markers, or continue the conflicted
operation until the user decides what to keep.

Apply the same rule when requirements, existing implementation, tests, or
documentation contradict one another.

## Command and Script Restrictions

Direct commands may be used only for:

- repository and file inspection;
- file search;
- the Git workflow defined in this file;
- direct Ruff validation as defined below.

Do not execute:

- `.sh`, `.bash`, `.zsh`, or other shell script files;
- `.py` files;
- `sh`, `bash`, `zsh`, PowerShell, or similar interpreters to run scripts;
- `python`, `python3`, `py`, or `python -m`;
- `poetry run`, `uv run`, `pipenv run`, `tox`, `nox`, or similar wrappers that
  execute project code;
- `pytest` or any other test runner;
- `make`, task runners, or project commands that execute scripts;
- command wrappers intended to bypass these restrictions.

When a prohibited command is required:

1. Provide the exact command to the user.
2. Ask the user to run it.
3. Ask for the complete output or logs.
4. Analyze only the results actually provided.

Do not claim that an unexecuted command succeeded.

## Implementation Rules

- Make the smallest coherent change that satisfies the approved plan.
- Inspect existing implementations and patterns before creating new ones.
- Prefer extending an existing abstraction over creating a duplicate.
- Do not perform unrelated refactoring.
- Do not change public behavior outside the approved scope.
- Do not add or update dependencies without explicit user approval.
- Do not modify generated files unless the task explicitly requires it.
- Do not disable, delete, skip, or weaken tests to hide a failure.
- Do not add blanket lint suppressions merely to silence findings.
- Do not expose, print, store, or commit credentials or secrets.
- Preserve user-authored changes that are unrelated to the task.

Do not run destructive Git operations, including:

- `git reset --hard`;
- `git clean`;
- forced checkout or restore of user changes;
- automatic stash operations;
- force push;
- history rewriting.

## Ruff Validation

After code changes are complete:

1. Identify every changed Python file.
2. Run Ruff directly against explicit changed-file paths:

   ```text
   ruff check <changed-python-files>
   ```

3. Fix every reported issue in the changed files.
4. Repeat the check until Ruff exits successfully.
5. Report the final Ruff command and result.

Do not use a broad automatic-fix command without user approval.

If no Python files changed, report that Ruff validation was not applicable.

If Ruff is unavailable or cannot run in the current environment, provide the
exact command to the user and ask for the complete output.

If resolving a Ruff issue would require a material change outside the approved
plan, stop and request approval for a revised plan.

## Test Validation

Do not run `pytest` or any other test suite.

After implementation:

1. Identify the tests affected by the changes.
2. Provide the narrowest reliable `pytest` command covering those tests.
3. Ask the user to run the command and provide the complete result.
4. Analyze failures using the supplied output.
5. Fix failures that are within the approved scope.
6. Request approval for a revised plan if a fix requires a material scope
   change.

Never report tests as passing unless the user has provided output confirming
that result.

## Commit Rules

Before any attempt to stage or commit changes, ask the user for explicit
permission. Codex may stage and create the specific proposed commit only after
the user grants that permission.

Before requesting commit approval, provide:

- a concise summary of the completed changes;
- the list of files intended for the commit;
- the Ruff validation result;
- the test command and known test result;
- any remaining risks or unverified behavior;
- the proposed commit message.

Do not stage or commit before approval.

One approval applies to one specific commit containing the described diff and
using the proposed message. Ask again when the diff or commit purpose changes
after approval.

After approval:

- stage only files belonging to the approved task;
- use a concise imperative commit subject;
- include a body when needed to explain what changed and why;
- do not amend, squash, or rewrite the commit without separate approval.

## Push Rules

Codex must never execute `git push` or otherwise push changes to a remote.

This prohibition is absolute and applies even when the user asks for or
explicitly approves a push. Only the user may perform the push.

After an approved commit, provide the exact command for the user to run:

```text
git push -u origin <branch-name>
```

The user is solely responsible for pushing.

## Pull Request Summary

When the user states that they are opening a pull request:

1. Review the complete branch diff against `main`.
2. Summarize all work performed on the branch.
3. Produce a Markdown-friendly pull request description.
4. Include the exact `pytest` command covering the changed or affected tests.
5. Mark a check as completed only when supported by an actual result.

Use this structure:

```markdown
## Summary

<What the pull request changes and why.>

## Changes

- <Change 1>
- <Change 2>

## Validation

- Ruff: <command and result>
- Tests: <result, or "Not run by the agent">

## Test Command

```text
pytest <affected-tests>
```

## UI test-case design

- Use `$ui-testcase-designer` for repository-aware UI test-case design.
- Store accepted UI test cases under `docs/testcase/<feature-slug>/`.
- Inspect existing manual cases and existing UI automation before proposing new coverage.
- Reuse the repository's configured browser client, URLs, environments, and modes.
- Explore only a safe local, development, test, or staging UI with configured browser tools.
- Present exactly one test case at a time.
- Save or update a testcase only after explicit `ACCEPT`.
- Treat requested edits as `DISCUSS`; show the revised case before saving it.
- Do not generate or modify Selenium automation during testcase design.
- Do not create temporary shell, Python, JavaScript, or Selenium scripts for UI exploration.
- Store testcase-specific extra pytest marks in `additional_pytest_marks`; do not duplicate derived `ui`, `regression`, `smoke`, or `e2e` marks there.

## Selenium testcase implementation

- Use `$selenium-test-implementer` with one accepted testcase path under `docs/testcase/<feature-slug>/TC-*.md`.
- Validate the complete manual scenario in the safe running UI before implementing it.
- Report testcase issues, potential product defects, environment blockers, and automation blockers instead of silently changing behavior.
- Apply testcase revisions only after `ACCEPT CASE CHANGES`, then replay the revised scenario.
- Search `tests/ui/`, `tests/smoke/`, and `tests/regression/` before creating a test; update or map equivalent coverage instead of duplicating it.
- Place new UI tests under `tests/ui/<feature_package>/test_<workflow_module>.py`.
- Preserve the current framework layers: locators in `src/locators`, low-level interactions in `src/pages`, business workflows in `src/flows`, and UI assertions in `src/assertions`.
- Present and obtain `ACCEPT PLAN` before editing automation.
- Keep test functions business-oriented; do not put selectors, direct WebDriver calls, waits, screenshots, or direct UI assertions in tests.
- Repository-wide required marks for every generated UI test are `ui` and `regression`.
- Smoke cases additionally receive `smoke`; E2E cases additionally receive `e2e`.
- Resolve generated-test marks from `.agents/skills/selenium-test-implementer/config/marker-policy.yaml`; to require another mark on all future generated tests, append it to `required_for_all` and register it in the active pytest configuration.
- Merge testcase-specific and explicitly requested additional registered marks; preserve compatible existing marks, normalize duplicates, and record the final set in testcase `automation_marks`.
- Register missing marks only through an accepted implementation plan.
- Create screenshot evidence for every logical UI assertion through the assertion/evidence layer.
- Ask the user to run the discovered pytest command and provide output; do not claim a pass without that result.
- Finalize testcase status as implemented only after a passing result and `ACCEPT AUTOMATION`.
- Never commit without required permission and never push changes.


## Risks and Notes

- <Known risk, assumption, limitation, or "None identified">

## Checklist

- [ ] The implementation matches the approved plan.
- [ ] Ruff passes for all changed Python files.
- [ ] The affected tests pass.
- [ ] The diff contains no unrelated changes.
- [ ] No secrets or generated artifacts were added accidentally.
- [ ] The branch is ready for user review.
```

Do not invent validation results or claim that checks passed without evidence.

## Completion Report

At the end of implementation, report only:

- what changed;
- which files changed;
- the Ruff command and result;
- the test command the user must run;
- test results provided by the user, if any;
- remaining risks, assumptions, or blockers;
- commit status;
- confirmation that no push was performed.

A task is not fully verified until the required user-run tests have passed.
