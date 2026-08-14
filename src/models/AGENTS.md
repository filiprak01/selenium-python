# Models Guidance

- Keep configuration dataclasses and framework-wide constants in this package.
- Keep evidence capability configuration in immutable dataclass models.
- Prefer immutable dataclasses for loaded configuration values.
- Validate configuration at the model boundary and keep secrets out of model defaults.
- Update this `AGENTS.md` when adding new model elements or changing this package's responsibilities.
