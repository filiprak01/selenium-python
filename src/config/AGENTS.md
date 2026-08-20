# Loader Guidance

- Keep YAML parsing and local `.env` loading in this package.
- Return typed configuration models rather than raw mappings to callers.
- Keep configuration file paths project-relative through `project.py`.
- Update this `AGENTS.md` when adding new loader elements or changing this package's responsibilities.
