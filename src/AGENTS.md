# Source Package Guidance

This directory is the source root for the importable framework. Keep framework code in
the direct child directories `assertions/`, `clients/`, `config/`, `flows/`, `locators/`,
`logging/`, `models/`, `pages/`, and `webdriver/`, with project path definitions in
`project.py`.

Preserve clear boundaries between clients, pages, locators, assertions, and WebDriver
infrastructure so future browsers, environments, clients, and generated tests can be
added without reorganizing the source root.

When adding new elements, update this `AGENTS.md` and the nearest focused `AGENTS.md`
so future contributors have current structure and ownership guidance.
