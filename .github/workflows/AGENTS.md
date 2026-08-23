# Workflow Context

GitHub Actions workflows run the framework in CI. Browser tests must use headless mode in CI
and publish generated Allure HTML reports and raw results as downloadable artifacts.

The Selenium workflow follows these execution conventions:

- pull-request runs trigger only when a pull request targeting `main` is opened;
- pull-request runs select changed test modules and use smoke coverage as the fallback for
  shared framework or configuration changes;
- the daily 04:00 UTC run executes only tests marked `smoke`;
- manual runs allow `smoke`, `regression`, `e2e`, or all tests;
- documentation-only pull requests may complete without running Selenium tests.

When adding a workflow or changing its execution conventions, update this file and the nearest relevant `AGENTS.md` file.
