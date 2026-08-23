# GitHub Automation Context

This directory contains repository automation configuration. Workflows should install the
Poetry project, run Selenium tests headlessly, generate a static Allure report, and preserve
both the report and raw results as downloadable artifacts.

Selenium CI runs only when a pull request targeting `main` is opened, on the daily
04:00 UTC schedule, or through manual dispatch. Do not add push triggers without explicit
user approval.

When adding or changing automation elements, update this file and the nearest relevant `AGENTS.md` file.
