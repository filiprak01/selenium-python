# Assertions Guidance

Keep reusable, wait-backed page assertions here. Assertions should accept page
locators rather than embedding selectors, and should raise clear `AssertionError`
messages for user-visible failures.

When adding new elements, update this `AGENTS.md` and the parent framework guidance.
