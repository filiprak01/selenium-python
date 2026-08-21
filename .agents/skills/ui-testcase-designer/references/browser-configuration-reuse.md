# Existing Browser Configuration Reuse

The repository owns the browser configuration used by UI discovery and later automation.

## Current repository sources

Inspect and reuse these paths when present:

```text
config/default.yaml
src/clients/ui_client.py
src/clients/client_pool.py
src/config/loader.py
src/models/configuration.py
src/models/constants.py
src/webdriver/factory.py
src/webdriver/chrome_options.py
tests/conftest.py
src/project.py
```

Read applicable scoped `AGENTS.md` files before using or proposing changes to any path.

## Required behavior

Before exploring a page:

1. locate the existing browser/client configuration;
2. identify configured environment names and URL aliases;
3. identify the normal/default safe environment;
4. identify supported execution modes such as headless, headed, local, remote, or grid;
5. identify existing authentication, session, cookie, fixture, or bootstrap behavior;
6. identify the browser capability exposed to Codex;
7. reuse these elements without duplicating them.

## Source-of-truth rules

- `config/default.yaml` and the existing loader/models own URL and mode resolution.
- Existing clients and WebDriver factory own browser startup and lifecycle.
- The skill must not hardcode `localhost`, test, staging, or production URLs when the resolver can provide them.
- The skill must not create another browser client or driver factory.
- The skill must not rewrite browser configuration solely for testcase generation.
- The skill must not copy credentials into prompts, cases, logs, screenshots, or generated configuration.

## Environment selection

Use the environment explicitly requested by the user when it is safe.

When the user does not specify an environment:

1. use the repository's configured default local/test environment when clearly defined;
2. otherwise use the safest non-production environment that can be resolved;
3. never choose production for exploratory writes or state changes;
4. report ambiguity when several environments are equally plausible and selection materially affects behavior.

Prefer the repository's configured headless mode for discovery unless:

- configuration defines another safe default;
- the available browser tool does not support headless operation;
- headed mode is necessary to understand behavior and remains safe.

## Invocation

Use the existing browser capability directly when Codex can access it.

When the application or client must be started through a repository command and repository instructions prohibit Codex from running commands:

- identify the exact existing command from repository documentation or configuration;
- ask the user to run it;
- continue after availability is confirmed;
- do not create a replacement launcher or temporary script.

## Exploration failure

If exploration is blocked by authentication, environment availability, missing data, permissions, feature flags, navigation failure, or browser-client failure:

- state the blocker precisely;
- do not invent observed behavior;
- continue repository analysis when useful;
- label the verification basis accurately;
- do not create temporary browser tooling as a workaround.
